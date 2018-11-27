# -*- coding: utf-8 -*-

from pprint import pprint

import yaml
import praw
import pymongo

import utils


HOT_LIMIT = 10
OLD_CONTENT = pymongo.MongoClient()['telegraph_digest']['content']


def normalization_coef(data):
    return 1 / (sum(data) / len(data))


def was_before(url):
    doc = {
        'digest': 'boobs',
        'url': url
    }

    if OLD_CONTENT.find_one(doc) is None:
        OLD_CONTENT.insert_one(doc)
        return False

    return True


def good_stufff(subs, reddit):
    submissons_with_cross_scores = dict()
    for submission in reddit.subreddit(subs).top('month'):
        sub_obj = {
            'self': submission,
            'cross_score': submission.score,
            'img_data': utils.do_magic(submission)
        }

        if sub_obj['img_data']['type'] in [utils.TYPE_GIF, utils.TYPE_IMG]:
            if not was_before(sub_obj['img_data']['url']):
                submissons_with_cross_scores[submission.id] = sub_obj
                print submission.score, sub_obj['img_data']['url']

        if len(submissons_with_cross_scores) == HOT_LIMIT:
            break

    return submissons_with_cross_scores


def supply(sub, config):
    reddit = praw.Reddit(user_agent=config['reddit']['user_agent'],
                        client_id=config['reddit']['client_id'],
                        client_secret=config['reddit']['client_secret'])
    subs = 'boobs+Boobies+Stacked+BustyPetite+TittyDrop'
    return good_stufff(subs, reddit)


def load_posts(config_filename, sub):
    with open(config_filename) as config_file:
        config = yaml.load(config_file.read())
    return supply(sub, config)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='prod.yml')
    # parser.add_argument('--sub')
    args = parser.parse_args()
    pprint(main(args.config, 'boobs'))
