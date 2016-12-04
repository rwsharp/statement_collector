"""Gather tweets from the public API and build up a history."""

import sys
import os.path
import shutil
import datetime
import argparse
import logging
import json

import tweepy


def get_config(config_file_name):
    """Gather the twitter connection configuration details.

    :param config_file_name: name of json file with twitter connection details
    :return: configuration dictionary
    """
    if os.path.isfile(config_file_name):
        with open(config_file_name, 'r') as config_file:
            config = json.load(config_file)
    else:
        message = 'ERROR - config file not found:' + str(config_file_name)
        logging.error(message)
        raise ValueError(message)

    return config


def get_args():
    """Build arg parser and get command line arguments

    :return: parsed args namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", default="config/config.json", help="config file name")
    parser.add_argument("--data-path", default="data", help="path to data file")
    parser.add_argument("--data-file", default="trump_dump.json", help="data file name")
    parser.add_argument("--backup-suffix", default=".bak",
                        help="suffix appended to data file name to create backup data file")
    parser.add_argument("--query", default="from:realDonaldTrump", help="data file name")

    args = parser.parse_args()

    return args


def main(args):
    """Execute the Twitter query and append results to the history file.

    :param args: command line arguments from argparse
    :return: exit status
    """

    # load config file with Twitter account details
    config = get_config(args.config_file)

    # check the validity of the data path and file
    data_path = args.data_path
    data_file_name = os.path.join(data_path, args.data_file)

    if not os.path.isdir(args.data_path):
        if not os.path.exists(args.data_path):
            # create the new path
            os.makedirs(args.data_path)
        else:
            # path exists, but it's not a directory
            message = 'ERROR - data path (' + str(args.data_path) + ')already exists, but is not a directory.'
            logging.error(message)
            raise ValueError(message)

    # create backup of old file if it exists
    if os.path.isfile(data_file_name):
        backup_file_name = data_file_name + args.backup_suffix
        shutil.copy(data_file_name, backup_file_name)

    # get the latest tweets
    auth = tweepy.OAuthHandler(config['consumer']['key'], config['consumer']['secret'])
    auth.set_access_token(config['access']['token'], config['access']['secret'])

    api = tweepy.API(auth)
    max_tweets = 1000
    query = args.query

    try:
        logging.info('executing query')
        search_result = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    except:
        logging.error('ERROR - something went wrong with the query.')
        raise

    # Append the tweets to the data file.
    #
    # Some tweets may be duplicates of ones recorded earlier, however, some fields such as retweet count may have
    # updated values. By recording the tweet again there will be some ability to see if its short term popularity has
    # spiked, the tweet has been deleted, etc.
    logging.info('appening query results to history file')
    with open(data_file_name, 'a') as data_file:
        for status in search_result:
            tweet = {'collected at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     'collected by': config['consumer']['key'] + '-' + config['access']['token'],
                     'version': 0.1,
                     'status': status._json}
            print >> data_file, json.dumps(tweet)

    return 0


if __name__ == '__main__':
    logging.basicConfig(filename='statement_collector.log', filemode='a',
                        format='%(asctime)s %(filename)s:%(funcName)s:%(levelname)s:%(message)s', level=logging.INFO)
    logging.info('started')

    try:
        args = get_args()
    except:
        logging.error('failed to parse command line arguments')
        logging.error('failure')
        logging.info('finished')
        raise

    try:
        main(args)
        logging.info('success')
        logging.info('finished')
    except:
        logging.error('failure')
        logging.info('finished')
        raise


