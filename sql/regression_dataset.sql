CREATE EXTERNAL TABLE `regression_dataset`(
  `pulmonary_embolism_dvt_rate` double COMMENT 'from deserializer', 
  `emergency_services` string COMMENT 'from deserializer', 
  `recommend_hospital` double COMMENT 'from deserializer', 
  `hospital_name` string COMMENT 'from deserializer', 
  `doctor_communication` double COMMENT 'from deserializer', 
  `wound_dehiscence_rate` double COMMENT 'from deserializer', 
  `region` string COMMENT 'from deserializer', 
  `state` string COMMENT 'from deserializer', 
  `discharge_information` double COMMENT 'from deserializer', 
  `hospital_ownership` string COMMENT 'from deserializer', 
  `infection_index` double COMMENT 'from deserializer', 
  `postop_sepsis_rate` double COMMENT 'from deserializer', 
  `pressure_ulcer_rate` double COMMENT 'from deserializer', 
  `medication_communication` double COMMENT 'from deserializer', 
  `nurse_communication` double COMMENT 'from deserializer', 
  `hospital_type` string COMMENT 'from deserializer', 
  `facility_id` string COMMENT 'from deserializer', 
  `postop_respiratory_failure_rate` double COMMENT 'from deserializer', 
  `hospital_overall_rating` double COMMENT 'from deserializer', 
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
  's3://imungai-capstone/analytics/regression_dataset/'
TBLPROPERTIES (
  'CreatedByJob'='prepare_ml_dataset', 
  'CreatedByJobRun'='jr_db29cf97b984df3ae7099965eb2bdd74b8a7f9b9fa1b5828839edf1fe1f68b1d', 
  'classification'='json')