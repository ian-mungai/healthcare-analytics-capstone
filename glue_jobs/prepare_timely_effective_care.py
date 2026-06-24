import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame
import gs_pivot

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1781026750393 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="timely_effective_care_raw", transformation_ctx="AWSGlueDataCatalog_node1781026750393")

# Script generated for node SQL Query
SqlQuery439 = '''
SELECT
    facility_id,
    facility_name,
    measure_id,
    CAST(score AS DOUBLE) AS score
FROM capstone_db.timely_effective_care_raw
WHERE measure_id IN (
    'SEP_1',
    'IMM_3',
    'OP_18b',
    'SAFE_USE_OF_OPIOIDS'
)
AND score IS NOT NULL
AND TRIM(score) <> ''
AND score <> 'Not Available'
'''
SQLQuery_node1781026807656 = sparkSqlQuery(glueContext, query = SqlQuery439, mapping = {"myDataSource":AWSGlueDataCatalog_node1781026750393}, transformation_ctx = "SQLQuery_node1781026807656")

# Script generated for node SQL Query
SqlQuery440 = '''
SELECT
    facility_id,
    facility_name,
    score AS ed_volume
FROM capstone_db.timely_effective_care_raw
WHERE measure_id = 'EDV'
AND score IS NOT NULL
AND TRIM(score) <> ''
AND score <> 'Not Available'
'''
SQLQuery_node1781040169092 = sparkSqlQuery(glueContext, query = SqlQuery440, mapping = {"myDataSource":AWSGlueDataCatalog_node1781026750393}, transformation_ctx = "SQLQuery_node1781040169092")

# Script generated for node Pivot Rows Into Columns
PivotRowsIntoColumns_node1781026839524 = SQLQuery_node1781026807656.gs_pivot(aggCol="score", aggFunction="mean", colList=["measure_id"])

# Script generated for node Change Schema
ChangeSchema_node1781026871641 = ApplyMapping.apply(frame=PivotRowsIntoColumns_node1781026839524, mappings=[("facility_id", "string", "facility_id", "string"), ("facility_name", "string", "hospital_name", "string"), ("EDV", "double", "ed_volume", "string"), ("IMM_3", "double", "healthcare_worker_flu_vaccination", "double"), ("OP_18b", "double", "ed_length_of_stay_minutes", "double"), ("SAFE_USE_OF_OPIOIDS", "double", "opioid_safety_compliance", "double"), ("SEP_1", "double", "sepsis_care_compliance", "double")], transformation_ctx="ChangeSchema_node1781026871641")

# Script generated for node Join
Join_node1781040247467 = Join.apply(frame1=SQLQuery_node1781040169092, frame2=ChangeSchema_node1781026871641, keys1=["facility_id"], keys2=["facility_id"], transformation_ctx="Join_node1781040247467")

# Script generated for node Change Schema
ChangeSchema_node1781041010871 = ApplyMapping.apply(frame=Join_node1781040247467, mappings=[("sepsis_care_compliance", "double", "sepsis_care_compliance", "double"), ("ed_length_of_stay_minutes", "double", "ed_length_of_stay_minutes", "double"), ("hospital_name", "string", "hospital_name", "string"), ("`.ed_volume`", "string", "ed_volume", "string"), ("healthcare_worker_flu_vaccination", "double", "healthcare_worker_flu_vaccination", "double"), ("opioid_safety_compliance", "double", "opioid_safety_compliance", "double"), ("facility_id", "string", "facility_id", "string")], transformation_ctx="ChangeSchema_node1781041010871")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1781041010871, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1781026694156", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1781026895017 = glueContext.getSink(path="s3://imungai-capstone/curated/timely_effective_care/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1781026895017")
AmazonS3_node1781026895017.setCatalogInfo(catalogDatabase="capstone_db",catalogTableName="timely_effective_care_curated")
AmazonS3_node1781026895017.setFormat("json")
AmazonS3_node1781026895017.writeFrame(ChangeSchema_node1781041010871)
job.commit()