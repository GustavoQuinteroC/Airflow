# Proceso de ETL para la Descarga y Almacenamiento de Tasas de Cambio en un Archivo CSV
# Introducción
Este informe describe la implementación de un DAG (Directed Acyclic Graph) en Apache Airflow que realiza un proceso de ETL (Extracción, Transformación y Carga) utilizando datos de tasas de cambio de una API pública. El DAG se ejecuta diariamente y guarda los datos procesados en un archivo CSV, permitiendo su posterior uso para análisis u otras tareas.

# Objetivos
El objetivo de este DAG es automatizar la descarga, transformación y almacenamiento de las tasas de cambio de monedas extranjeras con respecto al dólar estadounidense (USD) en un archivo CSV. Esto puede ser útil en casos donde se requieren datos actualizados de tasas de cambio de forma periódica.

# Proceso ETL
El DAG ejecuta las siguientes tareas:

# Extracción (Extract):
Se realiza una solicitud a la API pública de tasas de cambio de ExchangeRate-API (https://api.exchangerate-api.com).
Los datos obtenidos son almacenados en un registro temporal (XCom) para ser utilizados en las siguientes etapas.
# Transformación (Transform):
Los datos extraídos son transformados en un DataFrame de pandas.
Se redondean los valores de las tasas de cambio a dos decimales.
Los datos transformados también se almacenan en XCom.
# Carga (Load):
Los datos transformados son recuperados desde XCom y luego se almacenan en un archivo CSV en una ruta especificada en el servidor.
![imagen](https://github.com/user-attachments/assets/a831fc03-f5bc-4013-82b1-2f7f9179983d)

# Descripción Detallada
Dependencias y Configuración del DAG:

El DAG utiliza PythonOperator para cada una de las tres tareas (extracción, transformación y carga).
El DAG tiene un intervalo de ejecución diaria (schedule_interval=timedelta(days=1)), lo que significa que se ejecutará una vez al día a partir del 1 de enero de 2023 (start_date=datetime(2023, 1, 1)).
Los argumentos por defecto (default_args) permiten configurar aspectos importantes como la política de reintentos y el manejo de fallos.
Tareas:

Extracción: Usa requests.get() para hacer una solicitud HTTP a la API de tasas de cambio, y almacena los resultados en el sistema de almacenamiento temporal de Airflow (XCom) para uso posterior.
Transformación: Convierte los datos extraídos en un formato tabular (DataFrame de pandas), redondea los valores y los almacena de nuevo en XCom.
Carga: Toma los datos transformados desde XCom y los guarda en un archivo CSV en el sistema de archivos local.
Consideraciones y Configuraciones
Rutas de Almacenamiento: Es importante asegurarse de que la ruta donde se guardará el archivo CSV (/path/to/save/exchange_rates.csv) sea válida y accesible para el sistema en el que está corriendo Airflow.

Escalabilidad: El DAG es escalable y podría modificarse fácilmente para almacenar los datos en una base de datos o en un sistema de almacenamiento en la nube, como Amazon S3 o Google Cloud Storage.

# Resultados Esperados
El DAG genera un archivo CSV que contiene las tasas de cambio entre el dólar estadounidense (USD) y otras monedas. Este archivo puede ser utilizado para análisis financiero, monitoreo de tasas de cambio o para otras tareas automatizadas que requieran datos actualizados.

Ejemplo de contenido del CSV generado:

![imagen](https://github.com/user-attachments/assets/a67722d3-9ecc-423b-9b55-337afedb8d3b)

...	...
# Conclusiones
Este DAG automatiza la descarga diaria de tasas de cambio de una API y las guarda en formato CSV, lo que es útil para tener datos actualizados de monedas para análisis u otros fines. Puede ser utilizado como base para proyectos más complejos de integración de datos o análisis financiero.

# Posibles Mejoras
Almacenamiento en bases de datos.
Notificación por correo al final del proceso.
Manejo de excepciones y registros más detallados en caso de fallos en la API.
Referencias
Documentación de Airflow
API de tasas de cambio - ExchangeRate-API



