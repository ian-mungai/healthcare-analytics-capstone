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
  's3://imungai-capstone/curated/patient_experience/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_patient_experience', 
  'CreatedByJobRun'='jr_91c60fea65c65544e5310a0ca70c8ad0231be3c38a265f9eb77655d2e0b2c7a5', 
  'classification'='json')