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
AWSGlueDataCatalog_node1781024165625 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="hcahps_raw", transformation_ctx="AWSGlueDataCatalog_node1781024165625")

# Script generated for node SQL Query
SqlQuery327 = '''
SELECT
    facility_id,
    facility_name,
    hcahps_measure_id,
    CAST(patient_survey_star_rating AS DOUBLE) AS rating
FROM capstone_db.hcahps_raw
WHERE hcahps_measure_id IN (
    'H_CLEAN_STAR_RATING',
    'H_COMP_1_STAR_RATING',
    'H_COMP_2_STAR_RATING',
    'H_COMP_5_STAR_RATING',
    'H_COMP_6_STAR_RATING',
    'H_RECMND_STAR_RATING'
)
AND patient_survey_star_rating IS NOT NULL
AND TRIM(patient_survey_star_rating) <> ''
AND patient_survey_star_rating <> 'Not Available'
'''
SQLQuery_node1781024207258 = sparkSqlQuery(glueContext, query = SqlQuery327, mapping = {"myDataSource":AWSGlueDataCatalog_node1781024165625}, transformation_ctx = "SQLQuery_node1781024207258")

# Script generated for node Pivot Rows Into Columns
PivotRowsIntoColumns_node1781024464138 = SQLQuery_node1781024207258.gs_pivot(aggCol="rating", aggFunction="mean", colList=["hcahps_measure_id"])

# Script generated for node Change Schema
ChangeSchema_node1781024848156 = ApplyMapping.apply(frame=PivotRowsIntoColumns_node1781024464138, mappings=[("facility_id", "string", "facility_id", "string"), ("facility_name", "string", "hospital_name", "string"), ("H_CLEAN_STAR_RATING", "double", "cleanliness_score", "double"), ("H_COMP_1_STAR_RATING", "double", "nurse_communication", "double"), ("H_COMP_2_STAR_RATING", "double", "doctor_communication", "double"), ("H_COMP_5_STAR_RATING", "double", "medication_communication", "double"), ("H_COMP_6_STAR_RATING", "double", "discharge_information", "double"), ("H_RECMND_STAR_RATING", "double", "recommend_hospital", "double")], transformation_ctx="ChangeSchema_node1781024848156")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1781024848156, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1781019119253", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1781024933978 = glueContext.getSink(path="s3://imungai-capstone/curated/patient_experience/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1781024933978")
AmazonS3_node1781024933978.setCatalogInfo(catalogDatabase="capstone_db",catalogTableName="patient_experience_curated")
AmazonS3_node1781024933978.setFormat("json")
AmazonS3_node1781024933978.writeFrame(ChangeSchema_node1781024848156)
job.commit()