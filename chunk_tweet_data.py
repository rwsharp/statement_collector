import sys
import os.path
import shutil
import datetime
import argparse
import logging
import json

def get_args():
    """Build arg parser and get command line arguments

    :return: parsed args namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path", default="data", help="path to data file")
    parser.add_argument("--data-file", default="trump_dump.json", help="data file name")

    args = parser.parse_args()

    return args


def main(args):
    """Divide the original data file into individual files containing the tweets from a single day.

    :param args: command line arguments from argparse
    :return: exit status
    """

    # check the validity of the data path and file
    data_path = args.data_path
    data_file_name = os.path.join(data_path, args.data_file)

    logging.info('parsing history file')
    tweet_data = dict()
    with open(data_file_name, 'r') as data_file:
        for line_number, line in enumerate(data_file):
            tweet_event = json.loads(line)
            collected_at = datetime.datetime.strptime(tweet_event['collected at'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
            tweet = tweet_event['status']
            tweet_data.setdefault(collected_at, dict())
            tweet_data[collected_at][tweet['id']] = tweet

    for collected_at, tweets in sorted(tweet_data.iteritems()):
        output_file_name = 'data/chunked/tweets_by_realDonalTrump_' + collected_at + '.json'
        with open(output_file_name, 'w') as output_file:
            print output_file_name
            for tweet_id, tweet in sorted(tweets.iteritems()):
                print >> output_file, json.dumps(tweet)

    return 0


if __name__ == '__main__':
    #logging.basicConfig(filename='statement_collector.log', filemode='a',
    #                    format='%(asctime)s %(filename)s:%(funcName)s:%(levelname)s:%(message)s', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s %(filename)s:%(funcName)s:%(levelname)s:%(message)s', level=logging.INFO)
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

