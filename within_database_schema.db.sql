BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `condition_questionnaire` (
	`user_id`	TEXT NOT NULL,
	`condition_type`  TEXT NOT NULL,
	`useful`	INTEGER,
	`useful_understand` INTEGER,
	`useful_focus`  INTEGER,
	`distracting` INTEGER,
	`easynotice`  INTEGER,
	`confusing` INTEGER,
	`right_timing`  INTEGER,
	`well_integrated` INTEGER,
	`satisfied` INTEGER,
	`reuse_again` INTEGER,
	`freecomment_like`  TEXT,
	`freecomment_dislike` TEXT,
	`freecomment_possible_improv` TEXT,
	PRIMARY KEY(`user_id`,`condition_type`)
);
COMMIT;