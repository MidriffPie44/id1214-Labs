import csv
import requests
import json
import time


def load_data():
    match_ids = []  # stores all match id so that duplicates are avoided
    data = [['match_id', 'r1', 'r2', 'r3', 'r4', 'r5', 'd1', 'd2', 'd3', 'd4', 'd5', 'duration', 'rank', 'r_win']]
    with open('data.csv') as f:
        reader = csv.reader(f)
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]
            data.append(match)

            match_ids.append(int(match[0]))
    return data, match_ids


def fetch_data():
    r = requests.get(" https://api.opendota.com/api/publicMatches")
    fetched_data = r.json()
    return fetched_data


def append_data(data, fetched_data, match_ids):
    data_point = [0] * 14
    for match in fetched_data:
        if int(match['duration']) < 15*60:  # games that are too short don't count
            continue
        if int(match['game_mode']) not in [1, 2, 3, 4, 5, 12, 16, 22]:  # other game-modes than 5 vs 5 don't count
            continue
        if int(match['lobby_type']) not in [0, 2, 5, 6, 7]:  # other drafting than normal drafting doesn't count
            continue
        if int(match['match_id']) in match_ids:
            continue

        radiant_team = match['radiant_team'].split(',')
        dire_team = match['dire_team'].split(',')

        data_point[0] = match['match_id']
        data_point[1] = radiant_team[0]
        data_point[2] = radiant_team[1]
        data_point[3] = radiant_team[2]
        data_point[4] = radiant_team[3]
        data_point[5] = radiant_team[4]
        data_point[6] = dire_team[0]
        data_point[7] = dire_team[1]
        data_point[8] = dire_team[2]
        data_point[9] = dire_team[3]
        data_point[10] = dire_team[4]
        data_point[11] = match['duration']
        data_point[12] = match['avg_rank_tier']
        data_point[13] = int(match['radiant_win'])
        data.append(data_point.copy())


def save_data(data):
    with open('data.csv', 'w', newline="") as data_file:
        wr = csv.writer(data_file)
        wr.writerows(data)


try:
    data, match_ids = load_data()
    print('starting with {0} data points'.format(len(data)))
    while 1:
        fetched_data = fetch_data()[::-1]
        append_data(data, fetched_data, match_ids)
        print('appending data, total data points:', len(data))
        time.sleep(60)

except Exception as e:
    print("caught error", e)
    print('saved with number of data points', len(data))
    save_data(data)

except KeyboardInterrupt:
    save_data(data)
    print("Keyboard Interrupt")
    print('saved with {0} data points'.format(len(data)))

