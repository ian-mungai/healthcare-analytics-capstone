# healthcare-analytics-capstone

## Overview

Healthcare Analytics Capstone is a healthcare data engineering and analytics platform developed as the capstone project for a Master's degree program.

The project demonstrates the design and implementation of a modern cloud-based data pipeline using Apache Airflow, AWS S3, AWS Glue, SQL, and Docker. It ingests publicly available CMS hospital quality datasets, performs data transformation and curation, and produces analytics-ready datasets for reporting, visualization, and predictive modeling.

## Project Objectives

- Build an automated healthcare data pipeline
- Implement a scalable cloud-based data lake architecture
- Transform and curate healthcare quality datasets
- Create analytical datasets suitable for reporting and statistical modeling
- Demonstrate end-to-end data engineering workflows

## Data Sources

The project utilizes public datasets from the Centers for Medicare & Medicaid Services (CMS), including:

- Healthcare-Associated Infections (HAI)
- Hospital General Information
- HCAHPS Patient Experience Surveys
- PSI-90 Patient Safety Indicators
- Timely and Effective Care Measures

## Architecture

1. Apache Airflow orchestrates data ingestion and transformation workflows.
2. CMS datasets are extracted from public data sources.
3. Raw datasets are stored in Amazon S3.
4. AWS Glue jobs perform cleansing, transformation, and curation.
5. SQL models generate analytics and regression-ready datasets.
6. Final datasets support downstream analysis and reporting.

## Technology Stack

- Python
- Apache Airflow
- AWS S3
- AWS Glue
- SQL
- Docker

## Repository Structure

```text
dags/
glue_jobs/
sql/
config/
plugins/
docker/
```

## Key Features

- Automated healthcare data ingestion
- Cloud-based data lake architecture
- Workflow orchestration with Airflow
- ETL processing using AWS Glue
- Analytical and modeling-ready datasets
- Containerized development environment

## License

This project is provided for educational and portfolio purposes.
