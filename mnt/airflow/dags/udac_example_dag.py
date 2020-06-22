from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

s3_bucket = 'udacity-dend'
s3_key_log = "log_data"
s3_key_song = "song-data"
log_json_file = "log_json_path.json"

default_args = {
    'owner': 'kaili',
    'start_date': datetime(2018, 11, 1),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': True
}

dag = DAG('udac_example_dag',  
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          max_active_runs = 1       
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


create_tables_in_redshift = PostgresOperator(
  task_id="Create_tables",
  dag=dag,
  sql='create_tables.sql',
  postgres_conn_id="redshift"
)


stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    table_name="staging_events",
    s3_bucket=s3_bucket,
    s3_key=s3_key_log,
    log_json_file=log_json_file,
    dag=dag,
    provide_context=True
)


stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',  
    redshift_conn_id="redshift",
    aws_credentials="aws_credentials",
    table_name="staging_songs",
    s3_bucket=s3_bucket,
    s3_key=s3_key_song,
    log_json_file="",
    dag=dag,
    provide_context=True
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_query=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_query=SqlQueries.user_table_insert,
    table_name="users"
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_query=SqlQueries.song_table_insert,
    table_name="songs"
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_query=SqlQueries.artist_table_insert,
    table_name="artists"
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    sql_query=SqlQueries.time_table_insert,
    table_name="time"
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    sql_query=SqlQueries.user_table_insert,
    tables = ["songplays","users", "artists","songs", "time" ]
)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> create_tables_in_redshift

create_tables_in_redshift >> stage_events_to_redshift
create_tables_in_redshift >> stage_songs_to_redshift


stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table


load_songplays_table >> [load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table]

[load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks

run_quality_checks >> end_operator








