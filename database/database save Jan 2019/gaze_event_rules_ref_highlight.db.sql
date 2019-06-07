BEGIN TRANSACTION;
CREATE TABLE "rule_task" (
	`rule_name`	TEXT NOT NULL,
	`task`	INTEGER
);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_1_rule',62);
INSERT INTO `rule_task` (rule_name,task) VALUES ('legend_rule',1);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_2_rule',62);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_3_rule',62);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_4_rule',62);
INSERT INTO `rule_task` (rule_name,task) VALUES ('legend_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_1_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_2_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_3_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_4_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_1_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_2_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('ref_3_rule',2);
INSERT INTO `rule_task` (rule_name,task) VALUES ('',NULL);
CREATE TABLE "rule_removal_trigger" (
	`rule_name`	TEXT NOT NULL,
	`removal_trigger_event`	TEXT
);
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('legend_rule','ref_1_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('legend_rule','ref_2_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('legend_rule','ref_3_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('legend_rule','ref_4_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_1_rule','ref_3_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_1_rule','ref_4_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_2_rule','ref_3_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_2_rule','ref_4_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_3_rule','ref_1_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_3_rule','ref_2_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_4_rule','ref_1_fix');
INSERT INTO `rule_removal_trigger` (rule_name,removal_trigger_event) VALUES ('ref_4_rule','ref_2_fix');
CREATE TABLE "rule_intervention_payload" (
	`rule_name` TEXT NOT NULL,
	`intervention_name` TEXT
);
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('legend_rule','legend_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_1_rule','bar_1_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_2_rule','bar_2_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_3_rule','bar_3_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_3_rule','bar_4_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_4_rule','bar_5_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_4_rule','bar_6_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_1_demo','bar_1_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('ref_1_demo','bar_2_intervention');
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('',NULL);
INSERT INTO `rule_intervention_payload` (rule_name,intervention_name) VALUES ('',NULL);
CREATE TABLE "rule_delivery_trigger" (
	`rule_name`	TEXT NOT NULL,
	`delivery_trigger_event`	TEXT
);
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('legend_rule','text_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_1_rule','ref_1_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_2_rule','ref_2_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_3_rule','ref_3_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_4_rule','ref_4_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_1_demo','ref_1_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_2_demo','ref_2_fix');
INSERT INTO `rule_delivery_trigger` (rule_name,delivery_trigger_event) VALUES ('ref_3_demo','ref_3_fix');
CREATE TABLE "rule" (
	`name`	TEXT NOT NULL,
	`delivery_sql_condition`	BLOB,
	`removal_sql_condition`	BLOB,
	`max_repeat`	INTEGER,
	`active_retrigger`	INTEGER,
	PRIMARY KEY(`name`)
);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('legend_rule','Select
	case when count(*) > 0
		then 1
		else 0
	end result
From
(select * from text_fix TF, vis_fix VF
where TF.time_start < VF.time_start
group by VF.id
having count(TF.id) > 0);
','select 1 as result;','',NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_1_rule','select 1 as result;','select 1 as result;',NULL,NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_2_rule','select 1 as result;','select 1 as result',NULL,NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_3_rule','Select 1 as result;','select 1 as result',NULL,NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_4_rule','select 1 as result;','Select
	case when count(*) > 0
		then 1
		else 0
	end result
From
text_fix, intervention_state
where intervention_state.intervention = "bar_4_intervention"
and text_fix.time_end > intervention_state.time_stamp + 3000000;',NULL,NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_1_demo','select 1 as result;','select 1 as result;',NULL,NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_2_demo','select 1 as result;','select 1 as result;','',NULL);
INSERT INTO `rule` (name,delivery_sql_condition,removal_sql_condition,max_repeat,active_retrigger) VALUES ('ref_3_demo','Select
	case when count(*) > 1
		then 1
		else 0
	end result
From
ref_3_fix, rule_state
where rule_state.rule = "ref_3_rule"
and ref_3_fix.time_end > rule_state.time_stamp;','select 1 as result;',NULL,NULL);
CREATE TABLE "intervention" (
	`name`	TEXT NOT NULL,
	`max_repeat`	INTEGER,
	`function`	BLOB NOT NULL,
	`arguments`	BLOB,
	`delivery_delay`	INTEGER,
	`transition_in`	INTEGER,
	`transition_out`	INTEGER,
	PRIMARY KEY(`name`)
);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('bar_1_intervention',NULL,'highlightVisOnly','{"type": "reference", "id": 1, "bold": true, "bold_thickness": 3, "desat": true, "color": "green", "arrow": false}',10,500,500);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('legend_intervention',1,'highlightLegend','{"type": "legend", "color": "blue", "bold": true, "bold_thickness": 5, "desat": false, "arrow": false, "arrow_direction": "bottom"}',0,500,500);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('bar_2_intervention',NULL,'highlightVisOnly','{"type": "reference", "id":3, "bold": true, "bold_thickness": 3, "desat": true, "color": "green", "arrow": false}
',0,500,500);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('bar_3_intervention','','highlightVisOnly','{"type": "reference", "id":2, "bold": true, "bold_thickness": 3, "desat": true, "color": "green", "arrow": false}',0,500,500);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('bar_5_intervention',NULL,'highlightVisOnly','{"type": "reference", "id": 4, "bold": true, "bold_thickness": 3, "desat": true, "color": "green", "arrow": false}',10,500,500);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('bar_4_intervention',NULL,'highlightVisOnly','{"type": "reference", "id": 5, "bold": true, "bold_thickness": 3, "desat": true, "color": "green", "arrow": false}',0,500,500);
INSERT INTO `intervention` (name,max_repeat,function,arguments,delivery_delay,transition_in,transition_out) VALUES ('bar_6_intervention',NULL,'highlightVisOnly','{"type": "reference", "id": 6, "bold": true, "bold_thickness": 3, "desat": true, "color": "green", "arrow": false}',0,500,500);
COMMIT;
