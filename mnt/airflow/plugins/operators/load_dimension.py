from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 sql_query="",
                 table_name="",
                 truncate=False,
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table_name = table_name
        self.truncate = truncate

    def execute(self, context):
        """
          Load data into dimensional tables from staging tables.
          Use a truncate flag to empty the tables prior to load.
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.truncate:
            self.log.info(f"Truncating table {self.table_name} as flag set to True")
            redshift.run(f"TRUNCATE TABLE {self.table_name}")


        self.log.info(f"Loading data into Dimension Table {self.table_name}")
        redshift.run(self.sql_query)
        self.log.info(f"Dimension Table {self.table_name} is loaded.")
