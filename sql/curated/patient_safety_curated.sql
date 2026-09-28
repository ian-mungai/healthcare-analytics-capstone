CREATE EXTERNAL TABLE `patient_safety_curated`(
  `facility_id` string COMMENT 'from deserializer', 
  `hospital_name` string COMMENT 'from deserializer', 
  `pressure_ulcer_rate` double COMMENT 'from deserializer', 
  `postop_respiratory_failure_rate` double COMMENT 'from deserializer', 
  `pulmonary_embolism_dvt_rate` double COMMENT 'from deserializer', 
  `postop_sepsis_rate` double COMMENT 'from deserializer', 
  `wound_dehiscence_rate` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET>/curated/patient_safety/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_patient_safety', 
  'classification'='json')