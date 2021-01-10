import keras.models as models
import requests

import time

from evaluate_network import predict_with_model
from hero_dict import heroID_to_name
from match_downloader import fetch_data

num_heroes = 129


def get_hero_name_by_id(ids):
    hero_names = []
    for hero_id in list(ids):
        hero_names.append(heroID_to_name[hero_id])

    return hero_names


def get_match_by_id(match_id):
    r = requests.get('https://api.opendota.com/api/matches/{0}'.format(match_id))
    fetched_data = r.json()

    radiant_hero_id = []
    dire_hero_id = []
    banned_heroes_id = []
    for pick in fetched_data['picks_bans']:
        if pick['is_pick']:
            if pick['team'] == 0:
                radiant_hero_id.append(pick['hero_id'])
            else:
                dire_hero_id.append(pick['hero_id'])
        else:
            banned_heroes_id.append(pick['hero_id'])

    allied_heroes = list(map(int, radiant_hero_id))
    enemy_heroes = list(map(int, dire_hero_id))
    banned_heroes = list(map(int, banned_heroes_id))
    duration = int(fetched_data['duration'])

    medal = 40
    if fetched_data['skill']:
        medal = int(fetched_data['skill']) * 20

    return fetched_data, create_datapoints(1, allied_heroes, enemy_heroes, banned_heroes, duration, medal)


def print_summary(fetched_data, evaluation):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fetched_data['start_time']))
    duration = '{0}:{1}'.format(fetched_data['duration'] // 60, fetched_data['duration'] % 60)
    skill_group = fetched_data['skill']

    dire_hero_id = []
    radiant_hero_id = []
    banned_heroes_id = []
    for pick in fetched_data['picks_bans']:
        if pick['is_pick']:
            if pick['team'] == 0:
                radiant_hero_id.append(pick['hero_id'])
            else:
                dire_hero_id.append(pick['hero_id'])
        else:
            banned_heroes_id.append(pick['hero_id'])         

    dire_picks = ', '.join(get_hero_name_by_id(dire_hero_id))
    radiant_picks = ', '.join(get_hero_name_by_id(radiant_hero_id))
    bans = ', '.join(get_hero_name_by_id(banned_heroes_id))
    winner = 'Radiant' if fetched_data['radiant_win'] else 'Dire'
    rounded_eval = str(round(evaluation, 2))
    favour = 'Radiant' if round(evaluation) else 'Dire'

    summary = 'The match {0}, started {1}, and lasted {2}. The game is played in skill group {3}\n' \
        'The radiant team is: {4}\nThe dire team is: {5}\nThe bans are: {6}\nThe winning team is {7}\n' \
              'The evaluation for this game is {8}, favouring the {9}\n'.format(
                    match_id,
                    start_time,
                    duration,
                    skill_group,
                    radiant_picks,
                    dire_picks,
                    bans,
                    winner,
                    rounded_eval,
                    favour
              )
    print(summary)


def create_datapoints(is_radiant, allied_heroes, enemy_heroes, banned_heroes, duration, medal):
    match_datapoint = [0] * (num_heroes * 2 + 1)

    if is_radiant:
        for hero_id in allied_heroes:
            match_datapoint[hero_id] = 1
        for hero_id in enemy_heroes:
            match_datapoint[hero_id + num_heroes] = 1
    else:
        for hero_id in allied_heroes:
            match_datapoint[hero_id + num_heroes] = 1
        for hero_id in enemy_heroes:
            match_datapoint[hero_id] = 1

    data_point_duration = 115  # this is not a hero id so it is used as duration
    data_point_rank = 116  # this is also not a hero id so is used as rank
    data_point_radiant = 0
    match_datapoint[data_point_duration] = duration  # duration
    match_datapoint[data_point_rank] = medal  # rank
    match_datapoint[data_point_radiant] = is_radiant  # side

    samples = []

    if len(allied_heroes) != 5:  # this means that there is need for a pick
        unused_hero_id = [0, 24, 115, 116, 117, 118, 122, 124, 125, 127] + allied_heroes + enemy_heroes + banned_heroes
        picked_hero_id = list(set(range(num_heroes + 1)) - set(unused_hero_id))
        for hero_id in picked_hero_id:
            sample = match_datapoint.copy()
            sample[hero_id] = 1
            samples.append(sample)
    else:
        samples.append(match_datapoint)
        picked_hero_id = []

    return samples, picked_hero_id


def evaluate_matches(net, samples):
    samples = list(samples)
    raw_evaluation = predict_with_model(net, samples)
    flat_raw_evaluation = [evaluation[0] for evaluation in raw_evaluation]
    return flat_raw_evaluation


def evaluate_picks(net, samples, hero_id):
    evaluations = evaluate_matches(net, samples)
    hero_names = get_hero_name_by_id(hero_id)

    id_with_eval = []
    for i in range(len(hero_names)):
        id_with_eval.append([hero_names[i], evaluations[i]])

    return sorted(id_with_eval, key=lambda x: x[1])


if __name__ == '__main__':
    net_name = 'trained_model' #input('Enter name of network:')
    print('Loading model')
    net = models.load_model(net_name)

    mode = 'None'
    while mode not in ['1', '2']:
        mode = input('Do you want to:\n1 - Evaluate match?\n2 - Draft suggestion?\n')

    if mode == '1':
        match_id = 1
        while match_id:
            try: 
                match_id = int(input('Enter match id of the match you want to evaluate:'))
                fetched_data, match_sample = get_match_by_id(match_id)
                evaluation = evaluate_matches(net, match_sample[0])
                print_summary(fetched_data, evaluation[0])

            except TypeError:
                print('Match id was invalid or could not be parsed, try a different id')

    elif mode == '2':
        is_radiant = int(input('Enter 1 if you are radiant, enter 0 if you are dire:'))
        allied_heroes = list(map(int, input('Enter your 4 allied heroes by heroID separated by commas:').split(',')))
        enemy_heroes = list(map(int, input('Enter your 5 enemy heroes by heroID separated by commas:').split(',')))
        banned_heroes = list(map(int, input('Enter any banned hero by heroID separated by commas:').split(',')))
        duration = 60 * int(input('Enter desired length of game in minutes:'))
        medal = int(input('What is you medal rank as a number:'))

        samples, hero_id = create_datapoints(is_radiant, allied_heroes, enemy_heroes, banned_heroes, duration, medal)

        results = evaluate_picks(net, samples, hero_id)

        print('Worst picks')
        for result in results[:15]:
            print(result[0].ljust(30), round(result[1], 3))
        print('...')
        for result in results[-15:]:
            print(result[0].ljust(30), round(result[1], 3))
        print('Best picks')

