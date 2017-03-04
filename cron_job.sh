#! /bin/bash
BASEDIR=$(dirname "$0")
cd $BASEDIR
source env/bin/activate
cd telegraph_digest
python boobs_sender.py