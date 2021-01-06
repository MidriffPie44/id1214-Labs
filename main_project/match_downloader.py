import csv
import requests
import json
import time

file = 'data.csv'


def load_data():
    match_ids = []  # stores all match id so that duplicates are avoided
    data = [['match_id', 'r1', 'r2', 'r3', 'r4', 'r5', 'd1', 'd2', 'd3', 'd4', 'd5', 'duration', 'rank', 'r_win']]
    with open(file) as f:
        reader = csv.reader(f)
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]
            data.append(match)

            match_ids.append(int(match[0]))
    return data, match_ids


def fetch_data(max_id=0):
    if max_id != 0:
        less_than = '?less_than_match_id={0}'.format(max_id)
    else:
        less_than = ''
    r = requests.get("https://api.opendota.com/api/publicMatches"+less_than)
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
        match_ids.append(int(match['match_id']))


def save_data(data):
    with open(file, 'w', newline="") as data_file:
        wr = csv.writer(data_file)
        wr.writerows(data)


try:
    count = 0
    data, match_ids = load_data()
    print('starting with {0} data points'.format(len(data)))
    inbetween_time = time.time()
    max_id = 0
    while 1:
        count += 1
        start_time = time.time()
        old_data_len = len(data)
        fetched_data = fetch_data(max_id)[::-1]
        max_id = int(fetched_data[0]['match_id'])
        append_data(data, fetched_data, match_ids)
        if count % 100 == 0:
            save_data(data)
        new_data = len(data)-old_data_len
        current_time = time.strftime("%H:%M")
        time_taken = time.time()-inbetween_time
        print(current_time, max_id, count, 'Total data:', len(data), 'New:', new_data, 'Time:', time_taken)
        inbetween_time = time.time()
        time.sleep(20)

except Exception as e:
    save_data(data)
    print("caught error", e)
    current_time = time.strftime("%H:%M")
    print(current_time, 'saved with number of data points', len(data))

except KeyboardInterrupt:
    save_data(data)
    print("Keyboard Interrupt")
    current_time = time.strftime("%H:%M")
    print(current_time, 'saved with {0} data points'.format(len(data)))

