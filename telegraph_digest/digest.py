# -*- coding: utf-8 -*-

from pprint import pprint

import yaml
import praw

import utils


HOT_LIMIT = 10


def normalization_coef(data):
    return 1 / (sum(data) / len(data))


def good_stufff(subs, reddit):
    submissons_with_cross_scores = dict()
    for sub in subs:
        submissons = [s for s in reddit.subreddit(sub).hot(limit=HOT_LIMIT)]
        scores = [s.score for s in submissons]
        scores = [s * normalization_coef(scores) for s in scores]
        for ind, submisson in enumerate(submissons):
            submissons_with_cross_scores[submisson.id] = {
                'self': submisson,
                'cross_score': scores[ind]
            }
    return sorted(submissons_with_cross_scores.items(), key=lambda x: x[1]['cross_score'], reverse=True)[:HOT_LIMIT]



def supply(sub, config):
    reddit = praw.Reddit(user_agent=config['reddit']['user_agent'],
                        client_id=config['reddit']['client_id'],
                        client_secret=config['reddit']['client_secret'])
    subs = ['boobs', 'Boobies', 'Stacked', 'BustyPetite', 'TittyDrop']
    return good_stufff(subs, reddit)


def main(config_filename, sub):
    with open(config_filename) as config_file:
        config = yaml.load(config_file.read())
    return supply(sub, config)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='prod.yml')
    # parser.add_argument('--sub')
    args = parser.parse_args()
    main(args.config, 'boobs')
