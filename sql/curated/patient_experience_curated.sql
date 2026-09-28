CREATE EXTERNAL TABLE `patient_experience_curated`(
  `facility_id` string COMMENT 'from deserializer', 
  `hospital_name` string COMMENT 'from deserializer', 
  `nurse_communication` double COMMENT 'from deserializer', 
  `doctor_communication` double COMMENT 'from deserializer', 
  `medication_communication` double COMMENT 'from deserializer', 
  `discharge_information` double COMMENT 'from deserializer', 
  `recommend_hospital` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET>/curated/patient_experience/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_patient_experience', 
  'classification'='json')