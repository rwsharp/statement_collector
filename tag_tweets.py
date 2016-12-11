import json
import tweepy
import sys
import os.path
import argparse
import datetime
import re


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

    if args.dump:
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


        header = ['id', 'created at', 'text', 'tags', 'notes']
        print args.delimiter.join(header)
        for id, tweet in sorted(tweet_data.iteritems()):
            print_data = map(lambda s: unicode(s).encode('utf-8'), [id, tweet['created at'], re.sub('\n', '', tweet['text']), '', ''])
            print args.delimiter.join(print_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path",   default="data",            help="path to data file")
    parser.add_argument("--data-file",   default="trump_dump.json", help="data file name")
    parser.add_argument("--dump",        action="store_true",       help="dump json tweets to csv for tagging")
    parser.add_argument("--delimiter",   default="|",               help="csv delimiter")

    args = parser.parse_args()

    main(args)