import json
import requests
import pendulum

from io import BytesIO
from datetime import datetime
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.operators.bash import BashOperator


s3_bucket = "imungai-capstone"
aws_region = "us-east-1"

datasets = {
    "hai": {
        "dataset_id": "77hc-ibv8",
        "s3_prefix": "raw/hai/",
        "description": "Healthcare-Associated Infections - Hospital"
    },
    "hospital_general": {
        "dataset_id": "xubh-q36u",
        "s3_prefix": "raw/hospital_general/",
        "description": "Hospital General Information"
    },
    "hcahps": {
        "dataset_id": "dgck-syfz",
        "s3_prefix": "raw/hcahps/",
        "description": "HCAHPS - Hospital"
    },
    "psi90": {
        "dataset_id": "muwa-iene",
        "s3_prefix": "raw/psi90/",
        "description": "Medicare PSI-90 and Component Measures"
    },
    "timely_effective_care": 
    {
    "dataset_id": "yv7e-xc69",
    "s3_prefix": "raw/timely_effective_care/",
    "description": "Timely and Effective Care - Hospital"
}
}


@dag(
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
)
def full_pipeline():

    @task()
    def build_api_url() -> dict:
        api_urls = {}

        for dataset_name, dataset_config in datasets.items():
            dataset_id = dataset_config["dataset_id"]

            api_urls[dataset_name] = (
                "https://data.cms.gov/provider-data/api/1/datastore/query/"
                f"{dataset_id}/0/download?format=json"
            )
        return api_urls

    @task()
    def copy_data_to_s3(api_urls: dict) -> list[dict]:
        uploaded_files = []
        s3_hook = S3Hook(aws_conn_id="aws_credentials", region_name=aws_region)

        for dataset_name, dataset_config in datasets.items():
            url = api_urls[dataset_name]
            s3_prefix = dataset_config["s3_prefix"]

            response = requests.get(url, timeout=180)
            response.raise_for_status()

            data = response.json()

            if "results" not in data:
                raise ValueError(
                    f"No 'results' key found for dataset {dataset_name}"
                )

            records = data["results"]

            if not isinstance(records, list):
                raise TypeError(
                    f"'results' is not a list for dataset {dataset_name}"
                )

            run_date = datetime.utcnow().strftime("%Y%m%d")

            s3_key = f"{s3_prefix}{dataset_name}_{run_date}.jsonl"

            json_data = "\n".join(
                json.dumps(record)
                for record in records
            ) + "\n"

            payload = BytesIO(
                json_data.encode("utf-8")
            )

            s3_hook.load_file_obj(
                file_obj=payload,
                key=s3_key,
                bucket_name=s3_bucket,
                replace=True
            )

            uploaded_files.append({
                "dataset_name": dataset_name,
                "record_count": len(records),
                "s3_path": f"s3://{s3_bucket}/{s3_key}",
            })

        return uploaded_files
    
    
    hai_curated = GlueJobOperator(
    task_id="hai_curated",
    job_name="prepare_hai",
    aws_conn_id="aws_credentials",
    region_name=aws_region
    )

    hospital_characteristics_curated = GlueJobOperator(
    task_id="hospital_characteristics_curated",
    job_name="prepare_hospital_characteristics",
    aws_conn_id="aws_credentials",
    region_name=aws_region
    )

    patient_experience_curated = GlueJobOperator(
    task_id="patient_experience_curated",
    job_name="prepare_patient_experience",
    aws_conn_id="aws_credentials",
    region_name=aws_region
    )

    patient_safety_curated = GlueJobOperator(
        task_id="patient_safety_curated",
        job_name="prepare_patient_safety",
        aws_conn_id="aws_credentials",
        region_name=aws_region
    )

    timely_effective_care_curated = GlueJobOperator(
        task_id="timely_effective_care_curated",
        job_name="prepare_timely_effective_care",
        aws_conn_id="aws_credentials",
        region_name=aws_region
    )

    regression_dataset = GlueJobOperator(
        task_id="regression_dataset",
        job_name="prepare_ml_dataset",
        aws_conn_id="aws_credentials",
        region_name=aws_region
    )
    
    build_api_task = build_api_url()
    copy_data_task = copy_data_to_s3(build_api_task)
    
    build_api_task >> copy_data_task >> hai_curated >> hospital_characteristics_curated >> patient_experience_curated >> patient_safety_curated >> timely_effective_care_curated >> regression_dataset

full_pipeline_dag = full_pipeline()