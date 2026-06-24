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
AWSGlueDataCatalog_node1781026177640 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="psi90_raw", transformation_ctx="AWSGlueDataCatalog_node1781026177640")

# Script generated for node SQL Query
SqlQuery186 = '''
SELECT
    facility_id,
    facility_name,
    measure_id,
    CAST(rate AS DOUBLE) AS rate
FROM capstone_db.psi90_raw
WHERE measure_id IN (
    'PSI_03',
    'PSI_11',
    'PSI_12',
    'PSI_13',
    'PSI_14'
)
AND rate IS NOT NULL
AND TRIM(rate) <> ''
AND rate <> 'Not Available'
'''
SQLQuery_node1781026331564 = sparkSqlQuery(glueContext, query = SqlQuery186, mapping = {"myDataSource":AWSGlueDataCatalog_node1781026177640}, transformation_ctx = "SQLQuery_node1781026331564")

# Script generated for node Pivot Rows Into Columns
PivotRowsIntoColumns_node1781026356890 = SQLQuery_node1781026331564.gs_pivot(aggCol="rate", aggFunction="mean", colList=["measure_id"])

# Script generated for node Change Schema
ChangeSchema_node1781026390226 = ApplyMapping.apply(frame=PivotRowsIntoColumns_node1781026356890, mappings=[("facility_id", "string", "facility_id", "string"), ("facility_name", "string", "hospital_name", "string"), ("PSI_03", "double", "pressure_ulcer_rate", "double"), ("PSI_11", "double", "postop_respiratory_failure_rate", "double"), ("PSI_12", "double", "pulmonary_embolism_dvt_rate", "double"), ("PSI_13", "double", "postop_sepsis_rate", "double"), ("PSI_14", "double", "wound_dehiscence_rate", "double")], transformation_ctx="ChangeSchema_node1781026390226")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1781026390226, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1781019119253", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1781026449120 = glueContext.getSink(path="s3://imungai-capstone/curated/patient_safety/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1781026449120")
AmazonS3_node1781026449120.setCatalogInfo(catalogDatabase="capstone_db",catalogTableName="patient_safety_curated")
AmazonS3_node1781026449120.setFormat("json")
AmazonS3_node1781026449120.writeFrame(ChangeSchema_node1781026390226)
job.commit()