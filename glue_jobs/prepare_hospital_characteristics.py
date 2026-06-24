import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

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
AWSGlueDataCatalog_node1781023757248 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="hospital_general_raw", transformation_ctx="AWSGlueDataCatalog_node1781023757248")

# Script generated for node Filter Fields
SqlQuery188 = '''
SELECT
    facility_id,
    facility_name,
    hospital_type,
    hospital_ownership,
    emergency_services,
    CAST(hospital_overall_rating AS DOUBLE) AS hospital_overall_rating,
    state
FROM capstone_db.hospital_general_raw
WHERE facility_id IS NOT NULL
AND hospital_overall_rating IS NOT NULL
AND TRIM(hospital_overall_rating) <> ''
AND hospital_overall_rating <> 'Not Available'
'''
FilterFields_node1781023772690 = sparkSqlQuery(glueContext, query = SqlQuery188, mapping = {"myDataSource":AWSGlueDataCatalog_node1781023757248}, transformation_ctx = "FilterFields_node1781023772690")

# Script generated for node Create Regions
SqlQuery187 = '''
SELECT
    *,
    CASE
        WHEN state IN (
            'CT','MA','ME','NH','NJ','NY','PA','RI','VT'
        ) THEN 'Northeast'

        WHEN state IN (
            'IL','IN','IA','KS','MI','MN',
            'MO','NE','ND','OH','SD','WI'
        ) THEN 'Midwest'

        WHEN state IN (
            'AL','AR','DC','DE','FL','GA',
            'KY','LA','MD','MS','NC',
            'OK','SC','TN','TX','VA','WV'
        ) THEN 'South'

        ELSE 'West'
    END AS region
FROM myDataSource
'''
CreateRegions_node1781023822733 = sparkSqlQuery(glueContext, query = SqlQuery187, mapping = {"myDataSource":FilterFields_node1781023772690}, transformation_ctx = "CreateRegions_node1781023822733")

# Script generated for node Change Schema
ChangeSchema_node1781023856201 = ApplyMapping.apply(frame=CreateRegions_node1781023822733, mappings=[("facility_id", "string", "facility_id", "string"), ("facility_name", "string", "hospital_name", "string"), ("hospital_type", "string", "hospital_type", "string"), ("hospital_ownership", "string", "hospital_ownership", "string"), ("emergency_services", "string", "emergency_services", "string"), ("hospital_overall_rating", "double", "hospital_overall_rating", "double"), ("state", "string", "state", "string"), ("region", "string", "region", "string")], transformation_ctx="ChangeSchema_node1781023856201")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1781023856201, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1781019119253", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1781023885503 = glueContext.getSink(path="s3://imungai-capstone/curated/hospital_characteristics/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1781023885503")
AmazonS3_node1781023885503.setCatalogInfo(catalogDatabase="capstone_db",catalogTableName="hospital_characteristics_curated")
AmazonS3_node1781023885503.setFormat("json")
AmazonS3_node1781023885503.writeFrame(ChangeSchema_node1781023856201)
job.commit()