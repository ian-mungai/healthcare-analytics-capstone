CREATE EXTERNAL TABLE IF NOT EXISTS `capstone_db`.`timely_effective_care_raw` (
  `facility_id` string,
  `facility_name` string,
  `address` string,
  `citytown` string,
  `state` string,
  `zip_code` string,
  `countyparish` string,
  `telephone_number` string,
  `_condition` string,
  `measure_id` string,
  `measure_name` string,
  `score` string,
  `sample` string,
  `footnote` string,
  `start_date` string,
  `end_date` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'FALSE',
  'dots.in.keys' = 'FALSE',
  'case.insensitive' = 'TRUE',
  'mapping' = 'TRUE'
)
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://imungai-capstone/raw/timely_effective_care/'
TBLPROPERTIES ('classification' = 'json');