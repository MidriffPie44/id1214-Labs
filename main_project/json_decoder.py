import json
import csv

with open('output.json') as json_file:
    raw_data = json.load(json_file)

data = [['match_id', 'r1', 'r2', 'r3', 'r4', 'r5', 'd1', 'd2', 'd3', 'd4', 'd5', 'duration', 'rank', 'r_win']]
data_point = [0] * 14
for match in raw_data:
    if int(match['duration']) < 15*60:  # games that are too short don't count
        continue
    if int(match['game_mode']) not in [1, 2, 3, 4, 5, 12, 16, 22]:  # other game-modes than 5 vs 5 don't count
        continue
    if int(match['lobby_type']) not in [0, 2, 5, 6, 7]:  # other drafting than normal drafting doesn't count
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
    print(data_point)
    data.append(data_point.copy())


with open('data.csv', 'a+', newline="") as data_file:
    wr = csv.writer(data_file)
    for match in data:
        wr.writerow(match)

