import json
import tweepy
import sys
import os.path
import argparse
import datetime


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


def main(args):

    data_file_name = get_file_name(args.data_path, args.data_file)

    tweet_data = dict()

    with open(data_file_name, 'r') as data_file:
        for line in data_file:
            tweet = json.loads(line)

            status = tweet['status']

            # tweet ID
            tweet_data.setdefault(status['id'], dict())

            # static fields
            target_field, source_field = 'created at', 'created_at'
            if target_field in tweet_data[status['id']]:
                assert tweet_data[status['id']][target_field] == status[source_field]
            else:
                tweet_data[status['id']][target_field] = status[source_field]

            target_field, source_field = 'text', 'text'
            if target_field in tweet_data[status['id']]:
                assert tweet_data[status['id']][target_field] == status[source_field]
            else:
                tweet_data[status['id']][target_field] = status[source_field]

            # dynamic fields
            target_field, source_field = 'rt', 'retweet_count'
            tweet_data[status['id']].setdefault(target_field, dict())
            tweet_data[status['id']][target_field][tweet['collected at']] = status[source_field]

    for id, tweet in sorted(tweet_data.iteritems()):
        print id
        for field, val in tweet.iteritems():
            print field, val
        print


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path",   default="data",            help="path to data file")
    parser.add_argument("--data-file",   default="trump_dump.json", help="data file name")

    args = parser.parse_args()

    main(args)