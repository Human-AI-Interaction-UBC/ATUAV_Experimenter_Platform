BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `user_state_task` (
	`event_name`	TEXT,
	`task`	INTEGER,
	PRIMARY KEY(`event_name`,`task`)
);
CREATE TABLE IF NOT EXISTS `user_state` (
	`event_name`	TEXT NOT NULL,
	`type`	TEXT,
	`aoi`	TEXT,
	`feature`	TEXT,
	PRIMARY KEY(`event_name`)
);
CREATE TABLE IF NOT EXISTS `aoi` (
	`name`	TEXT NOT NULL,
	`task`	INTEGER NOT NULL,
	`dynamic`	INTEGER,
	`polygon`	BLOB,
	PRIMARY KEY(`name`,`task`)
);
COMMIT;
