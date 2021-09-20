from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['airflow_workshop', 'dev'])
def tutorial_taskflow_api_etl_virtualenv():

    @task.virtualenv(
        use_dill=True,
        system_site_packages=False,
        requirements=['varyaml'],
    )
    def extract():
        import varyaml
        file = open("./dags/config/sample.yaml")
        data = varyaml.load(file)
        return data

    @task(multiple_outputs=True)
    def transform(employee_list: dict):

        emp_with_python_skills = []

        for emp in employee_list:
            for v in emp.values():
                if "python" in v['skills']:
                    emp_with_python_skills.append(v['name'])

        print(emp_with_python_skills)        
        return {"employee_with_python_skills": emp_with_python_skills}

    @task()
    def load(emp_with_python_skills: list):
        for emp in emp_with_python_skills:
            print(f"Employee Name: {emp}")

    emp_data = extract()
    emp_with_python = transform(emp_data)
    load(emp_with_python["employee_with_python_skills"])

tutorial_etl_dag = tutorial_taskflow_api_etl_virtualenv()
