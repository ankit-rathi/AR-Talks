from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Define the DAG
dag = DAG(
    'simple_dag',
    default_args=default_args,
    description='A simple DAG that writes to and reads from a file',
    schedule_interval='*/0.5 * * * *',  # Runs every 30 seconds
    catchup=False,
)

# Task 1: Write "hello" to a file
def write_hello():
    with open('hello.txt', 'w') as f:
        f.write('hello')

write_task = PythonOperator(
    task_id='write_hello',
    python_callable=write_hello,
    dag=dag,
)

# Task 2: Read the file and print its contents
def read_hello():
    with open('hello.txt', 'r') as f:
        content = f.read()
        print(content)

read_task = PythonOperator(
    task_id='read_hello',
    python_callable=read_hello,
    dag=dag,
)

# Define task dependencies
write_task >> read_task
