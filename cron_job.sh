#! /bin/bash
BASEDIR=$(dirname "$0")
cd $BASEDIR
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") cron_job start"
source env/bin/activate
cd telegraph_digest
python boobs_sender.py
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") cron_job end"
