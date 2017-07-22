#!/bin/bash
#set -x

DATE=`date +%Y%m%d`

BACKUP_PATH=/home/ubuntu/backup/data
DATA_PATH=/home/ubuntu/data/

OWNER_SLUG="cspan:members-of-congress"
DATA_FILE="list_timeline_cspan_members_of_congress.json"
OUTPUT_PATH=${DATA_PATH}/cspan_members_tweets

cd /home/ubuntu/repos/statement_collector

COMMAND="/home/ubuntu/ve_p2.7.12/bin/python /home/ubuntu/repos/statement_collector/collect_corpus_from_list.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --list-owner-slug \"${OWNER_SLUG}\""
eval ${COMMAND}

COMMAND="/home/ubuntu/ve_p2.7.12/bin/python /home/ubuntu/repos/statement_collector/prepare_corpus.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --output-path ${OUTPUT_PATH}"
eval ${COMMAND}

