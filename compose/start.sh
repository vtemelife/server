#!/bin/sh
set -e
rm celerybeat.pid
rm celerybeat-schedule
make start
