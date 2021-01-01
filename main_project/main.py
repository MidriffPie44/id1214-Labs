import keras.models as models
import numpy as np

from evaluate_network import predict_with_model

from hero_dict import heroID_to_name

num_heroes = 129


def get_hero_name_by_id(ids):
    hero_names = []
    for hero_id in list(ids):
        hero_names.append(heroID_to_name[hero_id])

    return hero_names


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
    match_datapoint[data_point_duration] = duration  # duration
    match_datapoint[data_point_rank] = medal  # rank

    unused_hero_id = [0, 24, 115, 116, 117, 118, 122, 124, 125, 127] + allied_heroes + enemy_heroes + banned_heroes
    used_hero_id = list(set(range(num_heroes+1)) - set(unused_hero_id))
    samples = []
    for hero_id in used_hero_id:
        sample = match_datapoint.copy()
        sample[hero_id] = 1
        samples.append(sample)

    return samples, used_hero_id


def evaluate_match(net, samples, hero_id):
    raw_evaluation = predict_with_model(net, samples)
    flat_raw_evaluation = [evaluation[0] for evaluation in raw_evaluation]

    hero_names = get_hero_name_by_id(hero_id)

    id_with_eval = []
    for i in range(len(raw_evaluation)):
        id_with_eval.append([hero_names[i], flat_raw_evaluation[i]*100])

    return sorted(id_with_eval, key=lambda x: x[1])


if __name__ == '__main__':
    net_name = input('Enter name of network:')
    net = models.load_model(net_name)

    is_radiant = input('enter 1 if you are radiant enter 0 if you are dire:')
    allied_heroes = list(map(int, input('enter your 4 allied heroes by heroID separated by commas:').split(',')))
    enemy_heroes = list(map(int, input('enter your 5 enemy heroes by heroID separated by commas:').split(',')))
    banned_heroes = list(map(int, input('enter any banned hero by heroID separated by commas:').split(',')))
    duration = 60 * int(input('enter desired length of game in minutes:'))
    medal = int(input('what is you medal rank as a number:'))

    samples, hero_id = create_datapoints(is_radiant, allied_heroes, enemy_heroes, banned_heroes, duration, medal)

    results = evaluate_match(net, samples, hero_id)

    for result in results:
        print(result[0].ljust(30), result[1])
