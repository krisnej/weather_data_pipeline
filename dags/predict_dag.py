from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago

with DAG(
    dag_id="docker_predict_task",
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    default_args={
        "owner": "airflow",
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "depends_on_past": False,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    docker_predict_task = DockerOperator(
        task_id="docker_predict_task",
        image="predict",
        api_version="auto",
        auto_remove=True,
        mount_tmp_dir=False,
        container_name="docker-predict-container",
        docker_url="unix://var/run/docker.sock",
        network_mode="sensorfactcodingchallenge_bridgenet",
    )

    docker_predict_task
