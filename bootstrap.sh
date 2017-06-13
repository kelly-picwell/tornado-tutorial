#!/bin/sh

docker-compose up -d
wait-for postgresql://postgres@localhost:5432/tutorial
prep-it

export TUTORIAL_HOST='localhost'
export TUTORIAL_USER='postgres'
export TUTORIAL_PORT='5432'
export TUTORIAL_DBNAME='tutorial'
export TUTORIAL_PASSWORD=''
export PGSQL_TUTORIAL='postgresql://postgres@localhost:5432/tutorial'
