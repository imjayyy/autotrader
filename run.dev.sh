#!/bin/bash
BASEDIR=$(dirname "$0")
WORKER_NAME=autotrader_worker
FLOWER_PROCESS_PATTERN='A celery_worker flower'
BEAT_PROCESS_PATTERN='A celery_worker beat'
cd "$BASEDIR" || exit

# Kill previous
pkill -9 -f $WORKER_NAME
pkill -9 -f "$FLOWER_PROCESS_PATTERN"
pkill -9 -f "$BEAT_PROCESS_PATTERN"

# Start Flower
celery -A celery_worker flower --address=127.0.0.1 --port=5566 &

#Start beat
celery -A celery_worker beat --loglevel=info &
# Start celery
celery -A celery_worker worker -P eventlet --loglevel=DEBUG --logfile celery.log --concurrency=8 -n $WORKER_NAME


