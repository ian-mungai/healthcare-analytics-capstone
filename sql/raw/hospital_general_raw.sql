CREATE EXTERNAL TABLE IF NOT EXISTS `capstone_db`.`hospital_general_raw` (
  `facility_id` string,
  `facility_name` string,
  `address` string,
  `citytown` string,
  `state` string,
  `zip_code` string,
  `countyparish` string,
  `telephone_number` string,
  `hospital_type` string,
  `hospital_ownership` string,
  `emergency_services` string,
  `meets_criteria_for_birthing_friendly_designation` string,
  `hospital_overall_rating` string,
  `hospital_overall_rating_footnote` string,
  `mort_group_measure_count` string,
  `count_of_facility_mort_measures` string,
  `count_of_mort_measures_better` string,
  `count_of_mort_measures_no_different` string,
  `count_of_mort_measures_worse` string,
  `mort_group_footnote` string,
  `safety_group_measure_count` string,
  `count_of_facility_safety_measures` string,
  `count_of_safety_measures_better` string,
  `count_of_safety_measures_no_different` string,
  `count_of_safety_measures_worse` string,
  `safety_group_footnote` string,
  `readm_group_measure_count` string,
  `count_of_facility_readm_measures` string,
  `count_of_readm_measures_better` string,
  `count_of_readm_measures_no_different` string,
  `count_of_readm_measures_worse` string,
  `readm_group_footnote` string,
  `pt_exp_group_measure_count` string,
  `count_of_facility_pt_exp_measures` string,
  `pt_exp_group_footnote` string,
  `te_group_measure_count` string,
  `count_of_facility_te_measures` string,
  `te_group_footnote` string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
  'ignore.malformed.json' = 'FALSE',
  'dots.in.keys' = 'FALSE',
  'case.insensitive' = 'TRUE',
  'mapping' = 'TRUE'
)
STORED AS INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://imungai-capstone/raw/hospital_general/'
TBLPROPERTIES ('classification' = 'json');