import json
import csv

with open('output.json') as json_file:
    raw_data = json.load(json_file)

data = []
datapoint = [0]*14
for match in raw_data:
    if int(match['duration']) < 15*60:  # games that are too short don't count
        continue
    if int(match['game_mode']) not in [1,2,3,4,5,12,16,22]:  # other game-modes than 5 vs 5 don't count
        continue
    if int(match['lobby_type']) not in [0,2,5,6,7]: # other drafting than normal drafting doesn't count
        continue

    radiant_team = match['radiant_team'].split(',')
    dire_team = match['dire_team'].split(',')

    datapoint[0] = match['match_id']
    datapoint[1] = radiant_team[0]
    datapoint[2] = radiant_team[1]
    datapoint[3] = radiant_team[2]
    datapoint[4] = radiant_team[3]
    datapoint[5] = radiant_team[4]
    datapoint[6] = dire_team[0]
    datapoint[7] = dire_team[1]
    datapoint[8] = dire_team[2]
    datapoint[9] = dire_team[3]
    datapoint[10] = dire_team[4]
    datapoint[11] = int(match['radiant_win'])
    datapoint[12] = match['duration']
    datapoint[13] = match['avg_rank_tier']
    print(datapoint)
    data.append(datapoint.copy())


with open('data.csv', 'w', newline="") as data_file:
    wr = csv.writer(data_file)
    wr.writerows(data)

