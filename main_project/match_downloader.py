import csv
import requests
import time


def load_data(file_name):
    match_ids = []  # stores all match id so that duplicates are avoided
    data = [['match_id', 'r1', 'r2', 'r3', 'r4', 'r5', 'd1', 'd2', 'd3', 'd4', 'd5', 'duration', 'rank', 'r_win']]
    with open(file_name) as f:
        reader = csv.reader(f)
        for match in list(reader)[1:]:
            match = [int(data_point) for data_point in match]
            data.append(match)

            match_ids.append(int(match[0]))
    return data, match_ids


def fetch_data(max_id=0):
    if max_id != 0:
        less_than = '?less_than_match_id={0}'.format(max_id)
    else:  # if match id is zero then just fetch latest matches
        less_than = ''
    r = requests.get("https://api.opendota.com/api/publicMatches"+less_than)
    fetched_data = r.json()
    return fetched_data


def append_data(data, fetched_data, match_ids):
    """
    This reformat the fetched data so that its easier to store. It also trips not useful information. Appends it to the
    list in RAM.
    """
    data_point = [0] * 14
    for match in fetched_data:
        if int(match['duration']) < 15*60:  # games that are too short don't count
            continue
        if int(match['game_mode']) not in [1, 2, 3, 4, 5, 12, 16, 22]:  # other game-modes than 5 vs 5 don't count
            continue
        if int(match['lobby_type']) not in [0, 2, 5, 6, 7]:  # other drafting than normal drafting doesn't count
            continue
        if int(match['match_id']) in match_ids:  # do not add duplicates
            continue

        radiant_team = match['radiant_team'].split(',')
        dire_team = match['dire_team'].split(',')

        data_point[0] = match['match_id']  # Split all the datapoints and append them to the correct places
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


def save_data(file_name, data):
    print('Saving data, do not interrupt.')
    with open(file_name, 'w', newline="") as data_file:
        wr = csv.writer(data_file)
        wr.writerows(data)


if __name__ == '__main__':
    count = 0
    file = input('What file do you want to save the data to (data.csv):')
    data, match_ids = load_data(file)
    print('Starting with {0} data points'.format(len(data)))
    max_id = int(input('Enter the maximum match id (enter 0 to fetch latest match):'))
    between_time = time.time()

    try:
        while 1:  # fetch new matches continuously
            count += 1
            start_time = time.time()
            old_data_len = len(data)
            fetched_data = fetch_data(max_id)[::-1]
            append_data(data, fetched_data, match_ids)
            max_id = int(fetched_data[0]['match_id'])  # makes it so you do not fetch the same data twice
            if count % 100 == 0:  # save the data to the data.csv file as a backup
                save_data(file, data)

            new_data = len(data)-old_data_len
            current_time = time.strftime("%H:%M")
            time_taken = time.time() - between_time
            print(current_time, max_id, count, 'Total data:', len(data), 'New:', new_data, 'Time:', time_taken)
            between_time = time.time()
            time.sleep(1)

    except Exception as e:
        save_data(file, data)
        print("caught error", e)
        current_time = time.strftime("%H:%M")
        print(current_time, 'saved with number of data points', len(data))

    except KeyboardInterrupt:
        save_data(file, data)
        print("Keyboard Interrupt")
        current_time = time.strftime("%H:%M")
        print(current_time, 'saved with {0} data points'.format(len(data)))
