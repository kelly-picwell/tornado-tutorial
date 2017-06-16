#!/bin/bash

docker-compose up -d
output=`docker port tornado_tutorial_postgres`
export PG_PORT="${output#*:}"

str="postgresql://postgres@localhost:${PG_PORT}/tutorial"
export TUTORIAL_HOST="localhost"
export TUTORIAL_USER="postgres"
export TUTORIAL_PORT=$PG_PORT
export TUTORIAL_DBNAME="tutorial"
export TUTORIAL_PASSWORD=""
export PGSQL_TUTORIAL="postgresql://postgres@localhost:${PG_PORT}/tutorial"

wait-for $str
prep-it
