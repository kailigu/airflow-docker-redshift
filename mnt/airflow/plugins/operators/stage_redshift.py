from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    COPY_STAGING_SQL = """
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        FORMAT AS JSON '{}'
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials="",
                 table_name="",
                 s3_bucket="",
                 s3_key="",
                 log_json_file="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table_name = table_name
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.aws_credentials = aws_credentials
        self.log_json_file = log_json_file


    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id, sslmode='disable', keepalives_idle=5)

        self.log.info(f"Deleting data in table {self.table_name} if exists")
        redshift.run(f"DELETE FROM {self.table_name}")
        
        s3_path = f"s3://{self.s3_bucket}/{self.s3_key}"
        self.log.info(f"Retrieved S3 path - {s3_path}")

        if self.log_json_file != "":
            self.log_json_file = f"s3://{self.s3_bucket}/{self.log_json_file}"
            copy_sql = self.COPY_STAGING_SQL.format(self.table_name, s3_path, credentials.access_key, credentials.secret_key, self.log_json_file)
        else:
            copy_sql = self.COPY_STAGING_SQL.format(self.table_name, s3_path, credentials.access_key, credentials.secret_key, 'auto')

        self.log.info(f"Running COPY command : {copy_sql}")
        redshift.run(copy_sql)
        self.log.info(f"Copied data from {s3_path} to table {self.table_name}")

'''

    def execute(self, context):
        self.log.info('LoadDimensionOperator not implemented yet')
'''



