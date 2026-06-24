CREATE EXTERNAL TABLE IF NOT EXISTS `capstone_db`.`psi90_raw` (
  `facility_id` string,
  `facility_name` string,
  `address` string,
  `citytown` string,
  `state` string,
  `zip_code` string,
  `countyparish` string,
  `measure_id` string,
  `measure_name` string,
  `rate` string,
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
LOCATION 's3://imungai-capstone/raw/psi90/'
TBLPROPERTIES ('classification' = 'json');