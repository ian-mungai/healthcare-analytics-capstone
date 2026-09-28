CREATE EXTERNAL TABLE `hospital_characteristics_curated`(
  `facility_id` string COMMENT 'from deserializer', 
  `hospital_name` string COMMENT 'from deserializer', 
  `hospital_type` string COMMENT 'from deserializer', 
  `hospital_ownership` string COMMENT 'from deserializer', 
  `emergency_services` string COMMENT 'from deserializer', 
  `hospital_overall_rating` double COMMENT 'from deserializer', 
  `state` string COMMENT 'from deserializer', 
  `region` string COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET>/curated/hospital_characteristics/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_hospital_characteristics', 
  'classification'='json')