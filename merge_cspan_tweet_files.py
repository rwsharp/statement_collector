import glob
import os
import re

base_path = '/Users/rsharp/Dropbox/Uncertain Principles/Articles/Trump-o-meter/TF-IDF'
old_tweets_path = os.path.join(base_path, 'cspan_members_tweets-old')
new_tweets_path = os.path.join(base_path, 'cspan_members_tweets')
merged_tweets_path = os.path.join(base_path, 'cspan_members_tweets-merged-test')

delimiter = '\t'


# following code was to check for files that appeared in the new folder, but not the old: result didn't find any mismatch
#
# old_tweet_file_names = glob.glob(os.path.join(old_tweets_path, '*'))
# new_tweet_file_names = glob.glob(os.path.join(new_tweets_path, '*'))
#
# old_tweeters = set([os.path.split(old_tweet_file_name)[1] for old_tweet_file_name in old_tweet_file_names])
# new_tweeters = set([os.path.split(new_tweet_file_name)[1] for new_tweet_file_name in new_tweet_file_names])
# for tweeter in new_tweeters:
#     if tweeter not in old_tweeters:
#         print tweeter


old_tweets = dict()
new_tweets = dict()
merged_tweets = dict()

for old_tweet_file_name in old_tweet_file_names:
    assert os.path.isfile(old_tweet_file_name), 'ERROR - not a file: {}'.format(old_tweet_file_name)
    assert re.search('\.tsv$', old_tweet_file_name) is not None, 'ERROR - not a .tsv: {}'.format(old_tweet_file_name)

    tweeter = os.path.split(old_tweet_file_name)[1]

    old_tweets[tweeter] = list()
    new_tweets[tweeter] = list()
    merged_tweets[tweeter] = list()

    with open(old_tweet_file_name, 'r') as old_tweet_file:
        for line_number, line in enumerate(old_tweet_file):
            data = tuple(line.strip().split(delimiter))
            old_tweets[tweeter].append(data)
            merged_tweets[tweeter].append(data)

    new_tweet_file_name = os.path.join(new_tweets_path, tweeter)
    n_dupes = 0
    if os.path.isfile(new_tweet_file_name):
        with open(new_tweet_file_name, 'r') as new_tweet_file:
            for line_number, line in enumerate(new_tweet_file):
                data = tuple(line.strip().split(delimiter))
                new_tweets[tweeter].append(data)
                if data not in merged_tweets[tweeter]:
                    merged_tweets[tweeter].append(data)
                else:
                    n_dupes += 1
                    print '{} WARNING - Duplicate Tweet in {}: {}'.format(n_dupes, tweeter, data)

for tweeter, tweets in merged_tweets.iteritems():
    merged_tweets_file_name = os.path.join(merged_tweets_path, tweeter)

    with open(merged_tweets_file_name, 'w') as merged_tweets_file:
        for tweet in merged_tweets[tweeter]:
            print >> merged_tweets_file, '{}'.format(delimiter.join(tweet))



# f1 = open("cspan_members_tweets-old/AGBecerra.tsv")
# f1_contents = f1.read()
# f1.close()
#
# f2 = open("cspan_members_tweets/AGBecerra.tsv")
# f2_contents = f2.read()
# f2.close()
#
# f3 = open("cspan_members_tweets-merged/AGBecerra.tsv", "w") # open in `w` mode to write
# f3.write(f1_contents + f2_contents) # concatenate the contents
# f3.close()
