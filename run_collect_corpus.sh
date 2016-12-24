#!/bin/bash
set -x

WP_PATH=/home/bitnami/apps/wordpress/htdocs/wp-content/uploads/trump
DATA_PATH=/home/bitnami/data/trump

OWNER_SLUG="cspan:members-of-congress"
DATA_FILE="list_timeline_cspan_members_of_congress.json"

cd /home/bitnami/repos/statement_collector
/home/bitnami/ve_p2.7.12/bin/python /home/bitnami/repos/statement_collector/collect_corpus_from_list.py --data-path ${DATA_PATH} --data-file ${DATA_FILE} --list-owner-slug "${OWNER_SLUG}"

