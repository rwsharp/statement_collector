#!/bin/bash
#set -x

DATE=`date +%Y%m%d`

WP_PATH=/home/bitnami/apps/wordpress/htdocs/wp-content/uploads/trump
DATA_PATH=/home/bitnami/data/trump

OWNER_SLUG="cspan:members-of-congress"
DATA_FILE="list_timeline_cspan_members_of_congress.json"
TWEETS_TEXT_FILE="tweets_text_cspan_members_of_congress.${DATE}.txt"


cd /home/bitnami/repos/statement_collector

COMMAND="/home/bitnami/ve_p2.7.12/bin/python /home/bitnami/repos/statement_collector/collect_corpus_from_list.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --list-owner-slug \"${OWNER_SLUG}\""
eval $COMMAND

COMMAND="cat ${DATA_PATH}/${DATA_FILE} | jq -a .text | /home/bitnami/ve_p2.7.12/bin/python -c \"import sys;[sys.stdout.write(line.strip().strip('\\\"') + '\n') for line in sys.stdin]\" > ${DATA_PATH}/${TWEETS_TEXT_FILE}"
eval ${COMMAND}

