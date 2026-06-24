CREATE EXTERNAL TABLE `timely_effective_care_curated`(
  `facility_id` string COMMENT 'from deserializer', 
  `hospital_name` string COMMENT 'from deserializer', 
  `healthcare_worker_flu_vaccination` double COMMENT 'from deserializer', 
  `ed_length_of_stay_minutes` double COMMENT 'from deserializer', 
  `opioid_safety_compliance` double COMMENT 'from deserializer', 
  `sepsis_care_compliance` double COMMENT 'from deserializer', 
  `vte_prophylaxis_compliance` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://imungai-capstone/curated/timely_effective_care/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_timely_effective_care', 
  'CreatedByJobRun'='jr_be59c724c1e83e37b9a488d4a0659f9c3414734399bb167ac2f2910604c2d902', 
  'classification'='json')