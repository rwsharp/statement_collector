import json
import tweepy
import sys
import os.path

def main():

    config_file_name = 'config.json'
    with open(config_file_name, 'r') as config_file:
        config = json.load(config_file)

    data_file_name = 'trump_dump.json'

    observed_tweets = set()
    if os.path.isfile(data_file_name):
        with open(data_file_name, 'r') as data_file:
            for line in data_file:
                status = json.loads(line)
                observed_tweets.add(status['id'])

    auth = tweepy.OAuthHandler(config['consumer']['key'], config['consumer']['secret'])
    auth.set_access_token(config['access']['token'], config['access']['secret'])

    api = tweepy.API(auth)
    max_tweets = 100
    query = 'from:realDonaldTrump'
    search_result = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

    with open(data_file_name, 'a') as data_file:
        for status in search_result:
            if status.id not in observed_tweets:
                print >> data_file, json.dumps(status._json)


if __name__ == '__main__':
    main()