import json
import tweepy
import sys
import os.path
import argparse
import datetime
from collections import Counter
import re
from dateutil import tz

def is_negative(normalized_word_list):
    world_is_unfair_words = set(['biased', 'fools', 'dishonest', 'inacurate', 'overrated', 'crooked', 'onesided',
                                 'complaints', 'sad', 'false', 'terrible', 'bad', 'failing'])

    is_neg = False
    for word in normalized_word_list:
        if word in world_is_unfair_words:
            is_neg = True
            break

    return is_neg


def normalized(string):
    common_words = set(['if', 'the', 'to', 'a', 'and', 'of', 'in', 'for', 'is', 'be', 'on', 'it', 'at', 'as', 'was',
                        'am', 'has', 'do', 'but', 'had'])

    # split words on white space
    n_string = string.split()
    # all to lower case
    n_string = map(lambda s: s.lower(), n_string)
    # remove any remaining punctuation
    n_string = map(lambda s: re.sub('\W+', '', s), n_string)
    # remove common words
    n_string = filter(lambda s: s not in common_words, n_string)


    return n_string


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
    trends = {
        'times': dict(),
        'source': dict()
    }

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

            target_field, source_field = 'source', 'source'
            if target_field in tweet_data[status['id']]:
                assert tweet_data[status['id']][target_field] == status[source_field]
            else:
                tweet_data[status['id']][target_field] = status[source_field]

            # dynamic fields
            target_field, source_field = 'rt', 'retweet_count'
            tweet_data[status['id']].setdefault(target_field, dict())
            tweet_data[status['id']][target_field][tweet['collected at']] = status[source_field]

    for id, tweet in tweet_data.iteritems():
        tweet_time = datetime.datetime.strptime(tweet['created at'], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S')
        trends['times'][tweet_time] = tweet['created at']
        trends['source'][tweet_time] = tweet['source']

    # track by time of day
    utc_tz = tz.gettz('UTC')
    est_tz = tz.gettz('America/New_York')

    day_parts = {'you should really get some sleep': (datetime.time(0, 0, 0), datetime.time(4, 0, 0)),
                 'early morning': (datetime.time(4, 0, 1), datetime.time(8, 0, 0)),
                 'morning': (datetime.time(8, 0, 1), datetime.time(12, 0, 0)),
                 'afternoon': (datetime.time(12, 0, 1), datetime.time(16, 0, 0)),
                 'evening': (datetime.time(16, 0, 1), datetime.time(20, 0, 0)),
                 'late night': (datetime.time(20, 0, 1), datetime.time(23, 59, 59))}

    tweet_day_parts = list()

    starts, day_parts_list = zip(*sorted([(start, day_part) for day_part, (start, end) in day_parts.iteritems()]))
    header = ['tweet time'] + list(day_parts_list)

    print 'Tweet frequency by day part'
    print ','.join(header)
    for tweet_time, created_at in sorted(trends['times'].iteritems()):
        for day_part, (start, end) in day_parts.iteritems():
            utc_tweet_time = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
            utc_tweet_time = utc_tweet_time.replace(tzinfo=utc_tz)
            est_tweet_time = utc_tweet_time.astimezone(est_tz)
            if start <= est_tweet_time.time() <= end:
                tweet_day_parts.append(day_part)
                break

        day_part_counter = Counter(tweet_day_parts)
        print_data = [tweet_time] + [day_part_counter[day_part] for day_part in day_parts_list]
        print ','.join(map(str, print_data))

    # tweets by source
    sources = {'Android': '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>',
               'iPhone': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
               'Twitter Web': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>',
               'Twitter Ads': '<a href="https://ads.twitter.com" rel="nofollow">Twitter Ads</a>'}

    tweet_sources = list()

    tweet_source_list = ['Android', 'iPhone', 'Twitter Web', 'Twitter Ads']

    header = ['tweet time'] + tweet_source_list + ['other']

    print
    print 'Tweets by source'
    print ','.join(header)
    for tweet_time, source in sorted(trends['source'].iteritems()):
        tweet_source = 'other'
        for source_name, source_url in sources.iteritems():
            if source == source_url:
                tweet_source = source_name
        tweet_sources.append(tweet_source)
        if tweet_source == 'other':
            print 'WARNING - new source detected:' + str(source)

        tweet_source_counter = Counter(tweet_sources)
        print_data = [tweet_time] + [tweet_source_counter[tweet_source] for tweet_source in tweet_source_list + ['other']]
        print ','.join(map(str, print_data))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path",   default="data",            help="path to data file")
    parser.add_argument("--data-file",   default="trump_dump.json", help="data file name")

    args = parser.parse_args()

    main(args)
