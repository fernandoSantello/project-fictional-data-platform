# Project Overview

...

## Project Structure

The repository is organized into the following files and folders:

- `/airflow`: Everything related to Airflow. Logs, DAGs and a Dockerfile for a custom Airflow image.
- `/airflow/dags/currency_data_pipeline.py`: The main Pipeline for this project. Built using Airflow`s TaskFlow operations.
- `/dbml`: DBML files used for database documentation at [dbdocs.io](https://dbdocs.io/ "dbdocs.io")
- `/sql`: SQL files used for creating the three databases: ingestion, local warehouse and cloud warehouse. These files are used during container initialization.
- `/python/interfaces`: Base interfaces containing abstract methods. The interfaces are used by `services`
- `/python/services`: Base classes for base functions using libraries like Requests, mysql.connector-python and psycopg2.
- `/python/helper`: Utilizes the base functionalities provided by `/python/services` for more elaborate operations.
- `/python/controller`: Program logic using helper classes and functions. The controller class is used for the DAG Pipeline logic.
- `/python/exceptions`: Custom exceptions used through the project.
- `/resources/images`: Images relating to the project. Architecure, Power BI Graphs, etc.
- `docker-compose.yaml`: Configuration file for Docker architecture.

## Project Architecture

The following diagram represents the architecture of this project:

![Architecture](resources/images/fictional-data-platform-architecture.png)

## Database Documentation

The following links provide access to the database documentation hosted at [dbdocs.io](https://dbdocs.io/ "dbdocs.io"):

- [Ingestion Database](https://dbdocs.io/fersrp1964/ingestion_currency_data "Ingestion Database")
- [Data Warehouse (Local/Cloud)](https://dbdocs.io/fersrp1964/warehouse_currency_data "Data Warehouse (Local/Cloud)")

## Technologies

This project uses the following technologies:

- Airflow
- Docker
- Postgres
- MySQL
- AWS RDS
- Python
- Pandas
- Spark
- Power BI

## Getting Started

To get a local copy up and running, follow the following steps:

1. Clone the repo
   ```sh
   git clone https://github.com/fernandoSantello/project-fictional-data-platform
   ```
2. Navigate to the project directory.
3. Set up your own .env file
4. Build custom Airflow image using the Dockerfile at `/airflow`. The custom name and tag are `apache-airflow` and `fictional-data-platform` respectively.
5. Create the Docker Architecure using `docker-compose.yaml` at root.
6. Access and use pgAdmin, phpMyAdmin and Airflow Webserver to explore the project.

## License

Distributed under the MIT License. See `LICENSE` for more information.
