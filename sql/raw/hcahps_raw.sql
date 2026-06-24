CREATE EXTERNAL TABLE IF NOT EXISTS `capstone_db`.`hcahps_raw` (
  `facility_id` string,
  `facility_name` string,
  `address` string,
  `citytown` string,
  `state` string,
  `zip_code` string,
  `countyparish` string,
  `telephone_number` string,
  `hcahps_measure_id` string,
  `hcahps_question` string,
  `hcahps_answer_description` string,
  `patient_survey_star_rating` string,
  `patient_survey_star_rating_footnote` string,
  `hcahps_answer_percent` string,
  `hcahps_answer_percent_footnote` string,
  `hcahps_linear_mean_value` string,
  `number_of_completed_surveys` string,
  `number_of_completed_surveys_footnote` string,
  `survey_response_rate_percent` string,
  `survey_response_rate_percent_footnote` string,
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
LOCATION 's3://imungai-capstone/raw/hcahps/'
TBLPROPERTIES ('classification' = 'json');