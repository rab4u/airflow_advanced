from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta

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
    dag_id="branching-dag",
    default_args=default_args,
    catchup=False,
    schedule_interval="@once",
    is_paused_upon_creation=True)


def get_data(**kwargs):
    v1 = kwargs["params"]["var1"]
    v2 = kwargs["params"]["var2"]
    kwargs['ti'].xcom_push(key='result', value=v1 + v2)


def condition(**kwargs):
    result = int(kwargs['ti'].xcom_pull(key='result', task_ids='Get_Data'))
    if result > 0:
        print("selecting prod")
        return "Prod"
    else:
        print("selecting dev")
        return "Dev"


get_data = PythonOperator(
    task_id='Get_Data',
    dag=dag,
    provide_context=True,
    python_callable=get_data,
    params={"var1": 10, "var2": 20},
)

conditional_select = BranchPythonOperator(
    task_id='Conditional_Select',
    dag=dag,
    provide_context=True,
    python_callable=condition,
)

prod = BashOperator(
    task_id="Prod",
    bash_command="echo Result is greater than 0",
    dag=dag,
)

dev = BashOperator(
    task_id="Dev",
    bash_command="echo Result is less than 0",
    dag=dag,
)

get_data >> conditional_select >> [prod, dev]