### Setup latest airflow 
Note: Increase your docker memory from 2GB to 4GB
1. Open terminal and create a folder with name ```airflow_workshop```
2. Run this cmd in the terminal to download official airflow docker image and its dependicies  ```curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.3/docker-compose.yaml'```
3. Create dags, plugins and logs directories ```mkdir -p ./dags ./logs ./plugins```
4. Create .env file with airflow user id and airflow group id ```echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env```
5. Initialize airflow database with below cmd ```docker-compose up airflow-init```
6. Run the airflow ```docker-compose up```
7. login to airflow UI - localhost:8080 and username : airflow password: airflow