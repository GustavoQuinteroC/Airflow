from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd

# Definir argumentos por defecto
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Función de extracción: descarga datos de un API
def extract_data(**kwargs):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'  # API de tasas de cambio
    response = requests.get(url)
    data = response.json()
    rates = data['rates']  # Extrae las tasas de cambio
    kwargs['ti'].xcom_push(key='exchange_rates', value=rates)  # Almacena en XCom

# Función de transformación: convierte los datos a un DataFrame de pandas
def transform_data(**kwargs):
    rates = kwargs['ti'].xcom_pull(key='exchange_rates')  # Recupera tasas de cambio
    df = pd.DataFrame(list(rates.items()), columns=['currency', 'rate'])  # Crea DataFrame
    df['rate'] = df['rate'].apply(lambda x: round(x, 2))  # Redondea las tasas
    kwargs['ti'].xcom_push(key='transformed_data', value=df.to_dict(orient='records'))  # Almacena DataFrame

# Función de carga: guarda los datos en un archivo CSV
def load_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='transformed_data')  # Recupera datos transformados
    df = pd.DataFrame(data)  # Convierte a DataFrame
    df.to_csv('/root/airflow/resultados/exchange_rates.csv', index=False)  # Guarda en CSV

# Crear el DAG
with DAG(
    'etl_currency_to_csv',
    default_args=default_args,
    description='Un DAG que descarga tasas de cambio y las guarda en un archivo CSV',
    schedule_interval=timedelta(days=1),  # Se ejecuta diariamente
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
        provide_context=True
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
        provide_context=True
    )

    extract_task >> transform_task >> load_task  # Definición de dependencias
