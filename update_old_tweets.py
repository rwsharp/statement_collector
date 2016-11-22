import json
import tweepy
import sys
import os.path
import argparse
import datetime
import shutil


def get_file_name(data_path, file_name, create_path=False, warn=False):
    # check the data path and file
    data_file_name = os.path.join(data_path, file_name)

    if create_path:
        if not os.path.isdir(data_path):
            if not os.path.exists(data_path):
                # create the new path
                os.makedirs(data_path)
            else:
                # path exists, but it's not a directory
                raise ValueError('ERROR - data path (' + str(data_path) + ')already exists, but it is not a directory.')

    if warn:
        if not os.path.isfile(data_file_name):
            print 'WARNING - file does not exist: ' + data_file_name

    return data_file_name


def convert_tweet_v0_to_v0_1(v0_tweet, collection_datetime, collector_config):

    v0_1_tweet = {'collected at': collection_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                  'collected by': collector_config['consumer']['key'] + '-' + collector_config['access']['token'],
                  'version': 0.1,
                  'status': v0_tweet}

    return v0_1_tweet


def observed_tweets(data_file_name):
    # get the set of tweets already in the data file to avoid duplicates
    tweet_ids = set()
    if os.path.isfile(data_file_name):
        with open(data_file_name, 'r') as data_file:
            for line in data_file:
                status = json.loads(line)
                tweet_ids.add(status['id'])
    else:
        print 'WARNING - Did not find an existing data file. Will create new file: ' + str(data_file_name)

    return tweet_ids


def main(args):

    # load config file with Twitter account details
    if os.path.isfile(args.old_config_file):
        with open(args.old_config_file, 'r') as old_config_file:
            config = json.load(old_config_file)
    else:
        raise ValueError('ERROR - config file not found:' + str(args.old_config_file))

    # check the data path and file
    old_data_file_name = get_file_name(args.data_path, args.old_data_file, warn=True)
    new_data_file_name = get_file_name(args.data_path, args.new_data_file, create_path=True, warn=True)

    # create backup of old file
    backup_file_name = old_data_file_name + '.bak'
    shutil.copy(old_data_file_name, backup_file_name)

    # set the collection time that will added to all old tweets
    # since v0 didn't have a collection time, use a single value for all old tweets
    collection_time = datetime.datetime.strptime(args.collection_time, '%Y-%m-%d %H:%M:%S')

    with open(new_data_file_name, 'a') as new_data_file:
        with open(old_data_file_name, 'r') as old_data_file:
            for line in old_data_file:
                old_status = json.loads(line)
                new_status = convert_tweet_v0_to_v0_1(old_status, collection_time, config)
                print >> new_data_file, json.dumps(new_status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--old-config-file", help="config file name of the config used to collect the old tweets")
    parser.add_argument("--collection-time", help="collection time of the old tweets (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--data-path",       default="data",                help="path to data file")
    parser.add_argument("--old-data-file",   help="data file name containing old version tweets")
    parser.add_argument("--new-data-file",   default="trump_dump.json", help="data file name for new version tweets - does not need to be empty")

    args = parser.parse_args()

    main(args)