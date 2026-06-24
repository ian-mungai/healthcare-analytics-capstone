import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
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

# Script generated for node HAI raw
HAIraw_node1780956941199 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="hai_raw", transformation_ctx="HAIraw_node1780956941199")

# Script generated for node SQL Query
SqlQuery241 = '''
SELECT
    facility_id,
    facility_name,
    measure_id,
    measure_name,
    CAST(score AS DOUBLE) AS score
FROM capstone_db.hai_raw
WHERE measure_id IN (
    'HAI_1_SIR',
    'HAI_2_SIR',
    'HAI_3_SIR',
    'HAI_4_SIR',
    'HAI_5_SIR',
    'HAI_6_SIR'
)
AND score IS NOT NULL
AND TRIM(score) <> ''
AND score <> 'Not Available'
'''
SQLQuery_node1781022939464 = sparkSqlQuery(glueContext, query = SqlQuery241, mapping = {"myDataSource":HAIraw_node1780956941199}, transformation_ctx = "SQLQuery_node1781022939464")

# Script generated for node Aggregate
Aggregate_node1781022950455 = sparkAggregate(glueContext, parentFrame = SQLQuery_node1781022939464, groups = ["facility_name", "facility_id"], aggs = [["score", "avg"]], transformation_ctx = "Aggregate_node1781022950455")

# Script generated for node Change Schema
ChangeSchema_node1781023010932 = ApplyMapping.apply(frame=Aggregate_node1781022950455, mappings=[("facility_name", "string", "hospital_name", "string"), ("facility_id", "string", "facility_id", "string"), ("`avg(score)`", "double", "infection_index", "double")], transformation_ctx="ChangeSchema_node1781023010932")

# Script generated for node HAI Curated
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1781023010932, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1781019119253", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
HAICurated_node1781023292889 = glueContext.getSink(path="s3://imungai-capstone/curated/hai/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="HAICurated_node1781023292889")
HAICurated_node1781023292889.setCatalogInfo(catalogDatabase="capstone_db",catalogTableName="hai_curated")
HAICurated_node1781023292889.setFormat("json")
HAICurated_node1781023292889.writeFrame(ChangeSchema_node1781023010932)
job.commit()