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
- Jupyter Notebook

## Repository Structure

```text
.
├── dags/
│   └── full_pipeline.py
├── glue_jobs/
│   ├── prepare_hai.py
│   ├── prepare_hospital_characteristics.py
│   ├── prepare_ml_dataset.py
│   ├── prepare_patient_experience.py
│   ├── prepare_patient_safety.py
│   └── prepare_timely_effective_care.py
├── sql/
│   ├── raw/
│   │   ├── hai_raw.sql
│   │   ├── hcahps_raw.sql
│   │   ├── hospital_general_raw.sql
│   │   ├── psi90_raw.sql
│   │   └── timely_effective_care_raw.sql
│   ├── curated/
│   │   ├── hai_curated.sql
│   │   ├── hospital_characteristics_curated.sql
│   │   ├── patient_experience_curated.sql
│   │   ├── patient_safety_curated.sql
│   │   └── timely_effective_care_curated.sql
│   └── regression_dataset.sql
├── config/                 # airflow.cfg is generated here locally; not committed
├── plugins/
├── docker-compose.yaml
├── linear_regression.ipynb
├── .env.example
├── .gitignore
└── README.md
```

## Account-Specific Configuration

This project requires local configuration for AWS and Airflow. Do not commit personal account identifiers, access keys, bucket names, or local machine paths.

Use placeholders in committed files and configure real values locally.

### Local Airflow Files

1. Copy `.env.example` to `.env` and set `AIRFLOW_UID`, `FERNET_KEY`, `S3_BUCKET` and `AWS_REGION` (the file shows how to generate the key).
2. `config/airflow.cfg` is created by the `airflow-init` service on first start and is ignored by Git. It contains `fernet_key` and `secret_key`, so never commit it.
3. Run `git config core.hooksPath .githooks` once per clone. The commit-msg hook requires Conventional Commit subjects and rejects AI attribution lines.

### Required Local Values

| Value                  | Description                                      | Example Placeholder             |
| ---------------------- | ------------------------------------------------ | ------------------------------- |
| AWS region             | AWS region used for S3 and Glue                  | `AWS_REGION=your-aws-region`    |
| S3 bucket              | Destination bucket for raw and curated data      | `S3_BUCKET=your-s3-bucket-name` |
| Airflow AWS connection | Airflow connection used by S3 and Glue operators | `aws_credentials`               |

## AWS Setup Requirements

Before running the full pipeline, configure these AWS resources:

1. Create an S3 bucket for the project.
2. Create or configure AWS Glue jobs matching the job names used in the DAG:
   - `prepare_hai`
   - `prepare_hospital_characteristics`
   - `prepare_patient_experience`
   - `prepare_patient_safety`
   - `prepare_timely_effective_care`
   - `prepare_ml_dataset`
3. Upload or reference the Glue scripts from the `glue_jobs/` directory.
4. Ensure the Glue execution role has permissions for:
   - S3 read/write access
   - Glue job execution
   - CloudWatch logging
5. Configure AWS credentials locally or through an Airflow connection.

## Airflow AWS Connection

The DAG expects an Airflow connection named:

```text
aws_credentials
```

Create it in the Airflow UI:

1. Open Airflow at `http://localhost:8080`.
2. Go to **Admin > Connections**.
3. Add a new connection.
4. Use the following values:
   - Connection Id: `aws_credentials`
   - Connection Type: `Amazon Web Services`
   - AWS Access Key ID: your local AWS access key, if not using an IAM role
   - AWS Secret Access Key: your local AWS secret key, if not using an IAM role
   - Region Name: your AWS region

Do not commit AWS credentials to the repository.

## Key Features

- Automated healthcare data ingestion
- Cloud-based data lake architecture
- Workflow orchestration with Apache Airflow
- ETL processing using AWS Glue
- CMS healthcare quality dataset integration
- Analytical and modeling-ready data outputs
- Containerized local development environment

## License

This project is provided for educational and portfolio purposes.

## Portable Deployment Configuration

The DAG and notebook require non-empty `S3_BUCKET` and `AWS_REGION` environment variables. Docker Compose reads the private `.env` file. For a notebook started outside Compose, supply these two variables to the notebook process; the notebook does not load `.env` automatically. Missing values fail before reading or writing S3. Credentials remain in the existing AWS credential chain or Airflow connection, never in the notebook.

Each of the six Glue jobs requires `--S3_BUCKET`. The DAG passes the same bucket to every job. When starting a Glue job outside Airflow, set that argument explicitly. The established `capstone_db` schema, table names, job names and public CMS dataset identifiers are unchanged.

SQL files contain `<S3_BUCKET>` tokens and must be rendered before execution:

```sh
python3 scripts/render_sql.py sql/raw/hai_raw.sql > /tmp/hai_raw.sql
```

Set `S3_BUCKET` in the command environment first. The renderer validates the bucket, writes SQL to stdout and never submits a query. Rendered SQL contains private deployment configuration; keep it local. Historical Glue run identifiers were removed from DDL because they are not reusable table configuration.

The notebook retains historical public CMS outputs, figures and model results; editing configuration does not rerun or revalidate those results. Local logs, compiled caches and Tableau exports are separate review targets and are not cleared for publication by these source changes.
