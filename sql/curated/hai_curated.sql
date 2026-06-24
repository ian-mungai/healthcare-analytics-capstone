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
  's3://imungai-capstone/curated/hai/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_hai_dataset', 
  'CreatedByJobRun'='jr_617a114fe0b71ae78f3250638be3a6aa0b311b58708e2892f78803364ad480e8', 
  'classification'='json')