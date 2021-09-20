from airflow import DAG
from airflow.models.dag import dag
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import json


def create_client_etl_dags(dag_id,
               schedule,
               default_args):

    def extract(*args):
        print('Exract data')

    def transform(*args):
        print('transform data')
    
    def load(*args):
        print('Load data')

    dag = DAG(dag_id,
              schedule_interval=schedule,
              default_args=default_args,
              tags=[f"airflow_workshop_{dag_id}", 'dev']
              )

    with dag:
        t1 = PythonOperator(
            task_id='extract',
            python_callable=extract)

        t2 = PythonOperator(
            task_id='transform',
            python_callable=transform)

        t3 = PythonOperator(
            task_id='load',
            python_callable=load)
        
        t1 >> t2 >> t3

    return dag


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1)
    }

with open("./dags/config/clients_etl.json") as file:
    client_elt_config = json.load(file)

    for client in client_elt_config:
        dag_id = client['dag_id']
        globals()[dag_id] = create_client_etl_dags(
            dag_id=dag_id,
            schedule=client['schedule'],
            default_args=default_args
        )