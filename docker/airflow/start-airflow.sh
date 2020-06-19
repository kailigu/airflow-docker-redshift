#!/usr/bin/env bash

# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME

# Initiliase the metadatabase
airflow initdb

# Run the scheduler in background
airflow scheduler &> /dev/null &

# Run the web sever in foreground (for docker logs)
exec airflow webserver