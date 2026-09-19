from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator

default_args = {
    'owner': 'integra',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

PROJECT_ID = Variable.get("gcp_project", default_var="integra-project")
REGION = Variable.get("gcp_region", default_var="us-central1")
BUCKET = Variable.get("gcs_bucket", default_var="integra-hoard-bucket")

# The DAG corresponds to the Slow-Wave Deep Sleep (SWDS) Cycle
with DAG(
    'swds_cycle_dag',
    default_args=default_args,
    description='Automates the Slow-Wave Deep Sleep (SWDS) Cycle processing The Hoard data',
    schedule_interval='@daily',
    start_date=datetime(2026, 9, 1),
    catchup=False,
    tags=['job:datacloud:antigravity', 'integra-os', 'swds'],
) as dag:

    # Path to the Dataflow pipeline script
    pipeline_script = '/home/airflow/gcs/data/pipelines/swds_pipeline.py'
    
    # Task to trigger the Phoenix Engine Dataflow pipeline
    run_phoenix_engine = DataflowCreatePythonJobOperator(
        task_id='run_phoenix_engine_swds',
        py_file=pipeline_script,
        job_name='swds-phoenix-engine-{{ ds_nodash }}',
        options={
            'input': f'gs://{BUCKET}/The Hoard/*.json',
            'output_table': f'{PROJECT_ID}:integra_memory.archived_hoard',
            'project': PROJECT_ID,
            'region': REGION,
            'temp_location': f'gs://{BUCKET}/temp/',
            'runner': 'DataflowRunner',
        },
        location=REGION,
        wait_until_finished=True,
    )

    run_phoenix_engine
