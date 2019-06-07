BEGIN TRANSACTION;
CREATE TABLE "rule_task" (
	`rule_name`	TEXT NOT NULL,
	`task`	INTEGER
);
CREATE TABLE "rule" (
	`name`	TEXT NOT NULL,
	`delivery_sql_condition`	BLOB,
	`removal_sql_condition`	BLOB,
	`max_repeat`	INTEGER,
	`active_retrigger`	INTEGER,
	PRIMARY KEY(`name`)
);
CREATE TABLE "rule_delivery_trigger" (
	`rule_name`	TEXT NOT NULL,
	`delivery_trigger_event`	TEXT
);
CREATE TABLE "rule_removal_trigger" (
	`rule_name`	TEXT NOT NULL,
	`removal_trigger_event`	TEXT
);
CREATE TABLE "rule_intervention_payload" (
	`rule_name` TEXT NOT NULL,
	`intervention_name` TEXT
);
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
COMMIT;
