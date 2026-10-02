# healthcare-analytics-capstone

Apache Airflow and AWS Glue pipeline that turns five public CMS hospital quality datasets into analysis-ready data.

This repository is the capstone project for a Master's degree program. Airflow downloads five Centers for Medicare & Medicaid Services (CMS) hospital quality datasets from the CMS Provider Data Catalog and stores them in Amazon S3. Six AWS Glue jobs clean, transform and curate them into tables and a regression dataset. A Jupyter notebook fits a linear regression model on that dataset.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Architecture](#architecture)
- [Data](#data)
- [Deploy and Teardown](#deploy-and-teardown)
- [Repository Layout](#repository-layout)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Background

The pipeline covers a complete data engineering workflow on public healthcare data:

- Automated ingestion of five CMS datasets through the Provider Data Catalog API
- A data lake in Amazon S3 with raw, curated and analytics prefixes
- Workflow orchestration with Apache Airflow in Docker Compose
- Extract, transform and load (ETL) processing in AWS Glue
- Curated hospital quality tables and a regression-ready dataset for reporting and statistical modeling

Technology stack: Python, Apache Airflow, Amazon S3, AWS Glue, Structured Query Language (SQL), Docker and Jupyter Notebook.

## Install

Prerequisites: Docker with Docker Compose, Git and an AWS account with permission to create an S3 bucket and AWS Glue jobs.

This project requires local configuration for AWS and Airflow. Do not commit personal account identifiers, access keys, bucket names or local machine paths. Use placeholders in committed files and configure real values locally.

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

### AWS Setup Requirements

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
4. Give the Glue execution role permissions for:
   - S3 read and write access
   - Glue job execution
   - CloudWatch logging
5. Configure AWS credentials locally or through an Airflow connection.

### Airflow AWS Connection

The DAG expects an Airflow connection named:

```text
aws_credentials
```

Create it in the Airflow UI:

1. Start Airflow (see [Usage](#usage)) and open `http://localhost:8080`.
2. Go to **Admin > Connections**.
3. Add a connection.
4. Use the following values:
   - Connection Id: `aws_credentials`
   - Connection Type: `Amazon Web Services`
   - AWS Access Key ID: your local AWS access key, if not using an IAM role
   - AWS Secret Access Key: your local AWS secret key, if not using an IAM role
   - Region Name: your AWS region

Do not commit AWS credentials to the repository.

## Usage

Start Airflow from the repository root. The first command initializes the metadata database and creates `config/airflow.cfg`:

```sh
docker compose up airflow-init
docker compose up -d
```

Open `http://localhost:8080` and trigger the `full_pipeline` DAG. It has no schedule, so it runs only when triggered.

The DAG and notebook require non-empty `S3_BUCKET` and `AWS_REGION` environment variables. Docker Compose reads the private `.env` file. For a notebook started outside Compose, supply these two variables to the notebook process; the notebook does not load `.env` automatically. Missing values fail before reading or writing S3. Credentials stay in the AWS credential chain or the Airflow connection, never in the notebook.

Each of the six Glue jobs requires `--S3_BUCKET`. The DAG passes the same bucket to every job. When starting a Glue job outside Airflow, set that argument explicitly. The Glue Data Catalog database is `capstone_db`; its table names, the job names and the CMS dataset identifiers match the names in the DAG and SQL files.

SQL files contain `<S3_BUCKET>` tokens and must be rendered before execution:

```sh
python3 scripts/render_sql.py sql/raw/hai_raw.sql > /tmp/hai_raw.sql
```

Set `S3_BUCKET` in the command environment first. The renderer validates the bucket, writes SQL to stdout and never submits a query. Rendered SQL contains private deployment configuration; keep it local. The DDL holds no Glue run identifiers, because they are not reusable table configuration.

`linear_regression.ipynb` reads the regression dataset from `analytics/regression_dataset/` in the bucket.

## Architecture

1. Apache Airflow orchestrates data ingestion and transformation workflows.
2. CMS datasets are extracted from the CMS Provider Data Catalog API.
3. Raw datasets are stored in Amazon S3 as JSON Lines files.
4. AWS Glue jobs perform cleansing, transformation and curation.
5. SQL models generate analytics and regression-ready datasets.
6. The final datasets support downstream analysis and reporting.

## Data

The pipeline downloads these datasets from the [CMS Provider Data Catalog](https://data.cms.gov/provider-data/):

| Dataset | Catalog identifier |
| --- | --- |
| Healthcare-Associated Infections (HAI) - Hospital | `77hc-ibv8` |
| Hospital General Information | `xubh-q36u` |
| Hospital Consumer Assessment of Healthcare Providers and Systems (HCAHPS) Patient Survey - Hospital | `dgck-syfz` |
| Medicare Patient Safety Indicators (PSI-90) and Component Measures | `muwa-iene` |
| Timely and Effective Care - Hospital | `yv7e-xc69` |

Classification: Public. The datasets hold hospital-level measures, not patient-level records. Each dataset's catalog metadata lists its access level as `public` and names no license; use them under the terms of the CMS Provider Data Catalog.

## Deploy and Teardown

Deployment is the local Docker Compose stack in [Usage](#usage) plus the AWS resources in [AWS Setup Requirements](#aws-setup-requirements).

Stop the local stack and remove its containers and volumes, including the Airflow metadata database:

```sh
docker compose down --volumes --remove-orphans
```

Remove the AWS resources when they are no longer needed. These commands delete the project's data, catalog tables and jobs; they cannot be undone:

```sh
for job in prepare_hai prepare_hospital_characteristics prepare_patient_experience prepare_patient_safety prepare_timely_effective_care prepare_ml_dataset; do
  aws glue delete-job --job-name "$job" --region "$AWS_REGION"
done
aws glue delete-database --name capstone_db --region "$AWS_REGION"
aws s3 rb "s3://$S3_BUCKET" --force
```

## Repository Layout

```text
.
├── .githooks/
│   └── commit-msg
├── dags/
│   └── full_pipeline.py
├── glue_jobs/
│   ├── prepare_hai.py
│   ├── prepare_hospital_characteristics.py
│   ├── prepare_ml_dataset.py
│   ├── prepare_patient_experience.py
│   ├── prepare_patient_safety.py
│   └── prepare_timely_effective_care.py
├── scripts/
│   ├── check_commit_message.py
│   └── render_sql.py
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
├── LICENSE
└── README.md
```

## Limitations

- The data is public, hospital-level CMS reporting. The models and results are not clinically validated and do not support clinical decisions.
- The stack runs locally in Docker Compose with manually created AWS resources; it is not a production deployment.
- The notebook keeps its saved public CMS outputs, figures and model results; editing configuration does not rerun or revalidate them.
- Local logs, compiled caches and Tableau exports are not part of the repository and have not been reviewed for publication.

## Contributing

Individual capstone project; contributions are not accepted.

## License

[MIT](LICENSE) © Ian Mungai
