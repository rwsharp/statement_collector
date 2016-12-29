"""Divide the tweets collected by collect_corpus_from_list.py and split them into .tsv (time, text) files by
list member.
"""

import os
import argparse
import json
import re
import datetime


def get_args():
    """Build arg parser and get command line arguments

    :return: parsed args namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path",   default="data", help="path to data file")
    parser.add_argument("--data-file",   default="list_timeline_cspan_members_of_congress.json", help="data file name")
    parser.add_argument("--output-path", default="data/cspan_members_of_congress_member_tweets", help="path to data file")

    args = parser.parse_args()

    return args


def main(args):
    delimiter = '\t'

    formatted_tweet_data = dict()

    with open(os.path.join(args.data_path, args.data_file), 'r') as input_file:
        for line in input_file:
            tweet = json.loads(line)
            name = tweet['user']['screen_name']
            formatted_tweet_data.setdefault(name, list())

            tweet_date = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y%m%d')
            tweet_text = repr(tweet['text']).strip('u').strip('"')
            tweet_text = re.sub('\\\U', ' \\\U', tweet_text)
            tweet_text = re.sub('\s', ' ', tweet_text)
            print_data = [tweet_date, tweet_text]

            formatted_tweet_data[name].append(print_data)

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    if not os.path.isdir(args.output_path):
        raise ValueError('ERROR - output path exists, but is not a directory.')

    for name, tweets in formatted_tweet_data.iteritems():
        file_name = os.path.join(args.output_path, name + '.tsv')
        with open(file_name, 'w') as output_file:
            for tweet_data in sorted(tweets):
                print >> output_file, delimiter.join(tweet_data)



if __name__ == '__main__':
    main(get_args())