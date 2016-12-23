import json

def compare(compare_key, compare_val, compare_ts, new_key, new_val, new_ts):
    if new_key == compare_key:
        if new_val != compare_val:
            if isinstance(compare_val, dict):
                raise ValueError('ERROR - you should only compare on the value items of a tweet')
            else:
                return {'multivalue field': True,
                        compare_ts: compare_val,
                        new_ts:new_val}
    else:
        return new_val


def crawl_tweet(d_tweet, d_tweet_ts, compare_key, compare_val, compare_ts):
    if isinstance(d_tweet, dict):
        d = list()
        v = list()
        for key, val in d_tweet.iteritems():
            if isinstance(val, dict):
                d.append((key, val))
            else:
                val = compare(compare_key, compare_val, compare_ts, key, val, d_tweet_ts)
                print key, ':', val
                v.append((key, val))

        if len(d) > 0:
            for (key, val) in d:
                crawl_tweet(val, d_tweet_ts, compare_key, compare_val, compare_ts)
        else:
            return
    else:
        raise ValueError('ERROR - not a dictionary')

data = list()
with open('data/elizabeth_warren.json', 'r') as tweet_file:
    for line in tweet_file:
        data.append(json.loads(line))

for d_tweet in data[0:1]:
    print crawl_tweet(d_tweet, 'new value ts', 'retweet_count', 100, 'old value ts')
