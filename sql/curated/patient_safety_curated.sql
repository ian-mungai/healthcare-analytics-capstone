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
  's3://imungai-capstone/curated/patient_safety/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_patient_safety', 
  'CreatedByJobRun'='jr_7fcdd9448cb1a6aeb137eb52ef98e13ab97019a5dcbf5abe02804245078d79c5', 
  'classification'='json')