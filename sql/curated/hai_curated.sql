CREATE EXTERNAL TABLE `hai_curated`(
  `hospital_name` string COMMENT 'from deserializer', 
  `facility_id` string COMMENT 'from deserializer', 
  `infection_index` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://<S3_BUCKET>/curated/hai/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_hai_dataset', 
  'classification'='json')