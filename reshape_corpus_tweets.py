
"""Reshape tweets collected for individual accounts for prepare_corpus.py"""

import os
import argparse
import json


def get_args():
    """Build arg parser and get command line arguments

    :return: parsed args namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--data-path",        default="data", help="path to data file")
    parser.add_argument("--input-data-file",  default="other_member_accounts.json", help="data file name")
    parser.add_argument("--output-data-file", default="reshaped_other_member_accounts.json", help="data file name")

    args = parser.parse_args()

    return args


def main(args):

    input_file_name = os.path.join(args.data_path, args.input_data_file)
    output_file_name = os.path.join(args.data_path, args.output_data_file)

    with open(output_file_name, 'w') as output_file:
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                data = json.loads(line)
                try:
                    output_data = {'created_at': data['status']['created_at'],
                                   'id': data['status']['id'],
                                   'retweeted': data['status']['retweeted'],
                                   'text': data['status']['text'],
                                   'user': {'screen_name': data['status']['user']['screen_name']}}
                except:
                    print '----'
                    print line.strip()
                    print '----'
                    print data
                    print '----'
                    raise
                print >> output_file, json.dumps(output_data)


if __name__ == '__main__':
    main(get_args())
