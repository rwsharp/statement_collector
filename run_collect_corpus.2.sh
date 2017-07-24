#!/bin/bash
set -x

OTHER_MEMBERS=("@RepTomMarino"
               "@RandyNeugebauer"
               "@Rep_LizCheney"
               "@Rep_DevinNunes"
               "@AlanGrayson"
               "@congbillposey"
               "@SenateBanking"
               "@RepLaMalfa"
               "@RobWittman"
               "@RepGuthrie"
               "@KellyAyotte"
               "@PatrickMurphyFL"
               "@aguilarpete"
               "@CongHuelskamp"
               "@johnculberson"
               "@leezeldin"
               "@JohnCarneyDE"
               "@KamalaHarris")

DATE=`date +%Y%m%d`

BASE_PATH=/home/ubuntu
SCRIPT_PATH=${BASE_PATH}/repos/statement_collector
BACKUP_PATH=${BASE_PATH}/backup/data_test
DATA_PATH=${BASE_PATH}/data_test
OUTPUT_PATH=${DATA_PATH}/cspan_members_tweets_test

PYTHON_EXE=${BASE_PATH}/ve_p2.7.12/bin/python

OWNER_SLUG="cspan:members-of-congress"
DATA_FILE="list_timeline_cspan_members_of_congress.json"

COMMAND="cd ${SCRIPT_PATH}"
#echo ${COMMAND}
eval ${COMMAND}

COMMAND="${PYTHON_EXE} ${SCRIPT_PATH}/collect_corpus_from_list.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --list-owner-slug \"${OWNER_SLUG}\""
#echo ${COMMAND}
eval ${COMMAND}

COMMAND="${PYTHON_EXE} ${SCRIPT_PATH}/prepare_corpus.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --output-path ${OUTPUT_PATH}"
#echo ${COMMAND}
eval ${COMMAND}

DATA_FILE="other_member_accounts.full_tweets.json"
RESHAPED_DATA_FILE="other_member_accounts.json"

# get the max tweet id from the already collected tweets - this helps us avoid duplication in the next tweet pull
if [ -e "${DATA_PATH}/${RESHAPED_DATA_FILE}" ]
then
    MAX_TWEET=`cat ${DATA_PATH}/${RESHAPED_DATA_FILE} | jq '.id' | sort -r | head -n 1`
else
    MAX_TWEET=0
fi

for MEMBER in ${OTHER_MEMBERS[*]}
do
    QUERY="from:${MEMBER}"
    COMMAND="${PYTHON_EXE} ${SCRIPT_PATH}/main.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --query \"${QUERY}\" --since-id ${MAX_TWEET}"
    #echo ${COMMAND}
    eval ${COMMAND}
    COMMAND="cp ${DATA_PATH}/${DATA_FILE} ${BACKUP_PATH}/${DATA_FILE}"
    #echo ${COMMAND}
    eval ${COMMAND}
done

COMMAND="${PYTHON_EXE} ${SCRIPT_PATH}/reshape_corpus_tweets.py --data-path ${DATA_PATH} --input-data-file ${DATA_FILE} --output-data-file ${RESHAPED_DATA_FILE}"
#echo ${COMMAND}
eval $COMMAND

COMMAND="${PYTHON_EXE} ${SCRIPT_PATH}/prepare_corpus.py --data-path ${DATA_PATH} --data-file ${RESHAPED_DATA_FILE} --output-path ${OUTPUT_PATH}"
#echo ${COMMAND}
eval ${COMMAND}
