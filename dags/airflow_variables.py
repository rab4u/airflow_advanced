from airflow.models import Variable
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


facebook_token = Variable.get("facebook_token_password")
facebook_user_id = Variable.get("facebook_user_id")

default_args = {
    "owner": "rab4u",
    "depends_on_past": False,
    "start_date": datetime(2020, 7, 25),
    "email": ["myemail@mail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="airflow_variables",
    default_args=default_args,
    catchup=False,
    schedule_interval="@once",
    is_paused_upon_creation=True,
    tags=['airflow_workshop', 'dev']
    )

t2 = BashOperator(
    task_id="print_airflow_variables",
    bash_command=f"echo 'fabcebook_token: {facebook_token} facebook_user_id: {facebook_user_id}'",
    dag=dag
)

t2