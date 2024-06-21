# airflow_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.edgemodifier import Label
from kafka_consumer import poll_kafka_messages, commit_kafka_offsets
from emr_serverless_client import EMRServerlessClient

# Constants
APPLICATION_ID = 'your_application_id'
EXECUTION_ROLE_ARN = 'your_execution_role_arn'
LOG_URI = 's3://your_log_bucket'

# Default args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

# Create the DAG
dag = DAG(
    'kafka_to_rds_dag',
    default_args=default_args,
    description='Poll Kafka messages and write to RDS via EMR Serverless',
    schedule_interval='*/10 * * * *',
    catchup=False
)

# Task 1: Poll Kafka
def task_poll_kafka(**kwargs):
    messages = poll_kafka_messages()
    kwargs['ti'].xcom_push(key='messages', value=messages)
    return 'create_emr_connection' if messages else 'skip_tasks'

poll_kafka_task = BranchPythonOperator(
    task_id='poll_kafka_task',
    python_callable=task_poll_kafka,
    provide_context=True,
    dag=dag
)

# Task 2: Create EMR Connection
def create_emr_connection(**kwargs):
    messages = kwargs['ti'].xcom_pull(key='messages', task_ids='poll_kafka_task')
    if messages:
        emr_client = EMRServerlessClient(APPLICATION_ID, EXECUTION_ROLE_ARN, LOG_URI)
        kwargs['ti'].xcom_push(key='emr_client', value=emr_client)
        return 'write_to_rds'
    return 'skip_tasks'

create_emr_connection_task = BranchPythonOperator(
    task_id='create_emr_connection',
    python_callable=create_emr_connection,
    provide_context=True,
    dag=dag
)

# Task 3: Write to RDS
def write_to_rds(**kwargs):
    messages = kwargs['ti'].xcom_pull(key='messages', task_ids='poll_kafka_task')
    emr_client = kwargs['ti'].xcom_pull(key='emr_client', task_ids='create_emr_connection')
    if messages and emr_client:
        job_run_id = emr_client.start_job(messages)
        kwargs['ti'].xcom_push(key='job_run_id', value=job_run_id)
        return 'commit_kafka_offsets'
    return 'skip_tasks'

write_to_rds_task = BranchPythonOperator(
    task_id='write_to_rds',
    python_callable=write_to_rds,
    provide_context=True,
    dag=dag
)

# Task 4: Commit Kafka Offsets
def commit_kafka_offsets_task(**kwargs):
    messages = kwargs['ti'].xcom_pull(key='messages', task_ids='poll_kafka_task')
    emr_client = kwargs['ti'].xcom_pull(key='emr_client', task_ids='create_emr_connection')
    job_run_id = kwargs['ti'].xcom_pull(key='job_run_id', task_ids='write_to_rds')
    if messages and emr_client and job_run_id:
        commit_kafka_offsets()
        emr_client.stop_job(job_run_id)
        return 'done'
    return 'skip_tasks'

commit_kafka_offsets_task = BranchPythonOperator(
    task_id='commit_kafka_offsets',
    python_callable=commit_kafka_offsets_task,
    provide_context=True,
    dag=dag
)

# Task to skip remaining tasks if no messages are found
def skip_tasks():
    return 'done'

skip_tasks_task = PythonOperator(
    task_id='skip_tasks',
    python_callable=skip_tasks,
    dag=dag
)

done_task = PythonOperator(
    task_id='done',
    python_callable=lambda: print("All tasks done."),
    dag=dag
)

# DAG task dependencies
poll_kafka_task >> [create_emr_connection_task, skip_tasks_task]
create_emr_connection_task >> [write_to_rds_task, skip_tasks_task]
write_to_rds_task >> [commit_kafka_offsets_task, skip_tasks_task]
commit_kafka_offsets_task >> done_task
skip_tasks_task >> done_task
