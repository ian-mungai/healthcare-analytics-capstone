import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

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

# Script generated for node Patient Experience
PatientExperience_node1781027241232 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="patient_experience_curated", transformation_ctx="PatientExperience_node1781027241232")

# Script generated for node Hospital Characteristics
HospitalCharacteristics_node1781027178201 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="hospital_characteristics_curated", transformation_ctx="HospitalCharacteristics_node1781027178201")

# Script generated for node Patient Safety
PatientSafety_node1781027258383 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="patient_safety_curated", transformation_ctx="PatientSafety_node1781027258383")

# Script generated for node HAI
HAI_node1781027133066 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="hai_curated", transformation_ctx="HAI_node1781027133066")

# Script generated for node Timely and Effective Care
TimelyandEffectiveCare_node1781027278932 = glueContext.create_dynamic_frame.from_catalog(database="capstone_db", table_name="timely_effective_care_curated", transformation_ctx="TimelyandEffectiveCare_node1781027278932")

# Script generated for node Join hospital characteristics
Joinhospitalcharacteristics_node1781027148395 = Join.apply(frame1=HAI_node1781027133066, frame2=HospitalCharacteristics_node1781027178201, keys1=["facility_id"], keys2=["facility_id"], transformation_ctx="Joinhospitalcharacteristics_node1781027148395")

# Script generated for node Join patient experience
Joinpatientexperience_node1781027234729 = Join.apply(frame1=Joinhospitalcharacteristics_node1781027148395, frame2=PatientExperience_node1781027241232, keys1=["facility_id"], keys2=["facility_id"], transformation_ctx="Joinpatientexperience_node1781027234729")

# Script generated for node Join patient safety
Joinpatientsafety_node1781027637019 = Join.apply(frame1=Joinpatientexperience_node1781027234729, frame2=PatientSafety_node1781027258383, keys1=["facility_id"], keys2=["facility_id"], transformation_ctx="Joinpatientsafety_node1781027637019")

# Script generated for node Join timely and effective care
Jointimelyandeffectivecare_node1781027680472 = Join.apply(frame1=Joinpatientsafety_node1781027637019, frame2=TimelyandEffectiveCare_node1781027278932, keys1=["facility_id"], keys2=["facility_id"], transformation_ctx="Jointimelyandeffectivecare_node1781027680472")

# Script generated for node Drop Fields
DropFields_node1781033405558 = DropFields.apply(frame=Jointimelyandeffectivecare_node1781027680472, paths=["`.facility_id`", "`.hospital_name`", "facility_name"], transformation_ctx="DropFields_node1781033405558")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropFields_node1781033405558, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1781026694156", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1781029342659 = glueContext.getSink(path="s3://imungai-capstone/analytics/regression_dataset/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1781029342659")
AmazonS3_node1781029342659.setCatalogInfo(catalogDatabase="capstone_db",catalogTableName="regression_dataset")
AmazonS3_node1781029342659.setFormat("json")
AmazonS3_node1781029342659.writeFrame(DropFields_node1781033405558)
job.commit()