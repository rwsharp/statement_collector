import json
import tweepy
import sys
import os.path
import argparse
import datetime
import shutil


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
    if os.path.isfile(args.config_file):
        with open(args.config_file, 'r') as config_file:
            config = json.load(config_file)
    else:
        raise ValueError('ERROR - config file not found:' + str(args.config_file))

    # check the data path and file
    data_path = args.data_path
    data_file_name = os.path.join(data_path, args.data_file)

    if not os.path.isdir(args.data_path):
        if not os.path.exists(args.data_path):
            # create the new path
            os.makedirs(args.data_path)
        else:
            # path exists, but it's not a directory
            raise ValueError('ERROR - data path (' + str(args.data_path) + ')already exists, but it is not a directory.')

    # create backup of old file
    backup_file_name = data_file_name + '.bak'
    shutil.copy(data_file_name, backup_file_name)

    # get the latest tweets and add them to the data file
    # some tweets may be duplicates for ones recorded earlier, however, some data such as retweet count may be updated
    # giving some ability to see if the short term popularity of a tweet spikes
    auth = tweepy.OAuthHandler(config['consumer']['key'], config['consumer']['secret'])
    auth.set_access_token(config['access']['token'], config['access']['secret'])

    api = tweepy.API(auth)
    max_tweets = 1000
    query = 'from:realDonaldTrump'
    search_result = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

    with open(data_file_name, 'a') as data_file:
        for status in search_result:
            tweet = {'collected at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                     'collected by': config['consumer']['key'] + '-' + config['access']['token'],
                     'version': 0.1,
                     'status': status._json}
            print >> data_file, json.dumps(tweet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--config-file", default="config.json",     help="config file name")
    parser.add_argument("--data-path",   default="data",            help="path to data file")
    parser.add_argument("--data-file",   default="trump_dump.json", help="data file name")

    args = parser.parse_args()

    main(args)