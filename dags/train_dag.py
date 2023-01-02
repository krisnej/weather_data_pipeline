import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

with DAG(
    dag_id="docker_train_task",
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

    docker_train_task = DockerOperator(
        task_id="docker_train_task",
        image="train_predict",
        api_version="auto",
        auto_remove=True,
        environment={"API_KEY": os.environ.get("API_KEY")},
        mount_tmp_dir=False,
        mounts=[
            Mount(
                source=f"{os.environ.get('LOCAL_DAGS_PATH')}/dags",
                target="/dags",
                type="bind",
            ),
        ],
        container_name="docker-train-container",
        docker_url="unix://var/run/docker.sock",
        network_mode="weather_data_pipeline_bridgenet",
        entrypoint="python dags/temperature_forecast/train.py",
    )

    docker_train_task
