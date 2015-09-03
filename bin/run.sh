#!/usr/bin/env bash

function start () {
  gunicorn --reload app.main:application
}

function stop () {
  ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  *)
    echo "Usage: run.sh {start|stop}"
    exit 1
esac
