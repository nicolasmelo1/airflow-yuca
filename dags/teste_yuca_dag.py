from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import timedelta, datetime
import os


CURRENT_WORKING_DIRECTORY = os.getcwd()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'teste_yuca_dag',
    default_args=default_args,
    description='A simple dag to run every day and check if tomorrow is next month',
    schedule_interval=timedelta(days=1),
    template_searchpath = [os.getcwd() + '/sql/monthly_avarage_price/'],
    start_date=datetime.now(),
    tags=['example'],
)

def is_tomorrow_next_month():
    """
    Checks if tomorrow is the next month so we update ALWAYS in the LAST DAY of the month

    Returns:
        bool: Returns True if tomorrow is next month and false otherwise
    """
    return datetime.now().strftime("%m") != (datetime.now() + timedelta(days=1)).strftime("%m")


def retrieve_average_price_of_apartments_in_sao_paulo_from_big_query():
    """
    This retrieves the avarage price of apartments in Sao Paulo from Google's Big Query.

    IMPORTANT: This uses google.big_query api, refer here for further documentation: 
    https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-python

    IMPORTANT: Notice that `current_year` and `current_month` are hard coded, in a real environment we would leave the 
    commented code. We needed to do this because this was the last data available.

    Returns:
        int: Returns the avarage price of apartments in sao paulo by month
    """
    if is_tomorrow_next_month():
        from google.cloud import bigquery

        client = bigquery.Client()
        current_year = "2018"#datetime.now().strftime('%Y')
        current_month = "02"#datetime.now().strftime("%m")
        with open(CURRENT_WORKING_DIRECTORY + '/sql/monthly_avarage_price/monthly_avarage_price_by_month.sql', 'r') as f:
            query = f.read()
            query = query.format(str(current_year) + str(current_month))
            query_job = client.query(query)
            for row in query_job:
                return row['avarage_price_in_sao_paulo'] 


def create_monthly_avarage_price_table():
    """
    Responsible for creating the `monthly_sao_paulo_rent_price` table in our example database.
    """
    if is_tomorrow_next_month():
        import sqlite3

        connection = sqlite3.connect(os.environ.get('AIRFLOW_CONN_OPERATIONS_EXAMPLE_DB', ''))
        with open(CURRENT_WORKING_DIRECTORY + '/sql/monthly_avarage_price/create_monthly_avarage_price_table_in_database.sql', 'r') as f:
            query = f.read()
            connection.execute(query)
            connection.commit()
            connection.close()


def insert_monthly_avarage_price_data(task_instance):
    """
    Responsible for inserting the data in the created `monthly_sao_paulo_rent_price` table in our example database.

    Notice that we use xcomm here to get the data from another task, 
    refer to the documentation for further reference: https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#xcoms
    """
    if is_tomorrow_next_month():
        import sqlite3
        
        connection = sqlite3.connect(os.environ.get('AIRFLOW_CONN_OPERATIONS_EXAMPLE_DB', ''))
        with open(CURRENT_WORKING_DIRECTORY + '/sql/monthly_avarage_price/insert_monthly_avarage_price_data_in_database.sql', 'r') as f:
            query = f.read()
            query = query.format(
                task_instance.xcom_pull(task_ids='get_average_price_monthly_in_sao_paulo_from_big_query'), 
                str(int(datetime.now().strftime('%m'))),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            )
            connection.execute(query)
            connection.commit()
            connection.close()

get_average_price_monthly_in_sao_paulo_from_big_query = PythonOperator(
    task_id='get_average_price_monthly_in_sao_paulo_from_big_query',
    python_callable=retrieve_average_price_of_apartments_in_sao_paulo_from_big_query,
    dag=dag,
)

create_monthly_avarage_price_table_in_database = PythonOperator(
    task_id='create_monthly_avarage_price_table_in_database',
    python_callable=create_monthly_avarage_price_table,
    dag=dag
)

insert_monthly_avarage_price_data_in_database = PythonOperator(
    task_id='insert_monthly_avarage_price_data_in_database',
    python_callable=insert_monthly_avarage_price_data,
    dag=dag
)

get_average_price_monthly_in_sao_paulo_from_big_query >> create_monthly_avarage_price_table_in_database >> \
    insert_monthly_avarage_price_data_in_database