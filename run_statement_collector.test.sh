#!/bin/bash
set -x

WP_PATH=/home/bitnami/apps/wordpress/htdocs/wp-content/uploads/trump
DATA_PATH=/home/bitnami/data/trump

QUERY="from:realDonaldTrump"
DATA_FILE=trump_dump.json

#cd /home/bitnami/repos/statement_collector
#/home/bitnami/ve_p2.7.12/bin/python /home/bitnami/repos/statement_collector/main.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --query "${QUERY}"
#cp ${DATA_PATH}/${DATA_FILE} ${WP_PATH}/${DATA_FILE}


#QUERY="from:POTUS"
#SINCE_ID="822446982648210000"  # Between the last Obama @POTUS tweet: 822446982648201200 and the first Trump @POTUS tweet: 822521968465416200 
#DATA_FILE=potus45.json

#cd /home/bitnami/repos/statement_collector
#/home/bitnami/ve_p2.7.12/bin/python /home/bitnami/repos/statement_collector/main.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --query "${QUERY}" --since-id ${SINCE_ID}
#cp ${DATA_PATH}/${DATA_FILE} ${WP_PATH}/${DATA_FILE}


QUERY="from:SenWarren OR from:elizabethforma"
DATA_FILE=elizabeth_warren.json

cd /home/bitnami/repos/statement_collector
/home/bitnami/ve_p2.7.12/bin/python /home/bitnami/repos/statement_collector/main.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --query "${QUERY}"
cp ${DATA_PATH}/${DATA_FILE} ${WP_PATH}/${DATA_FILE}

