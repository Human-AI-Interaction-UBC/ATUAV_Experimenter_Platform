BEGIN TRANSACTION;
CREATE TABLE "aoi" (
        `name`  TEXT NOT NULL,
        `task`  INTEGER NOT NULL,
        `dynamic`       INTEGER,
        `polygon`       BLOB,
        PRIMARY KEY(`name`,`task`)
);
INSERT INTO "aoi" VALUES('text',1,1,'[(132,229),(132,555),(606,555),(606,229)]');
INSERT INTO "aoi" VALUES('vis2',1,1,'[(378,371),(378,401),(553,401),(553,371)]');
INSERT INTO "aoi" VALUES('text',2,1,'[(0,0),(0,100),(100,100),(100,0)]');
INSERT INTO "aoi" VALUES('vis',1,'','[(616,94),(616,509),(1090,509),(1090,94)]');
INSERT INTO "aoi" VALUES('legend',1,'','[(653,499),(653,557),(1075,557),(1075,499)]');
INSERT INTO "aoi" VALUES('top_left',1,'','[(0,0),(0,300),(300,300),(300,0)]');
INSERT INTO "aoi" VALUES('ref_1',1,'','[(244,233),(244,253),(578,253),(244,233),(578,233),(152,258),(152,279),(196,279),(196,258),(578,233)]');
INSERT INTO "aoi" VALUES('ref_2',1,'','[(534,254),(534,279),(583,279),(583,254),(534,254),(152,282),(152,302),(259,302),(259,283),(152,282)]');
INSERT INTO "aoi" VALUES('ref_3',1,'','[(256,331),(256,353),(440,353),(440,331)]');
INSERT INTO "aoi" VALUES('ref_4',1,'','[(199,380),(199,404),(380,404),(380,380)]');
INSERT INTO "aoi" VALUES('ref_4',2,'','[(199,380),(199,404),(380,404),(380,380)]');
INSERT INTO "aoi" VALUES('ref_3',2,'','[(256,331),(256,353),(440,353),(440,331)]');
INSERT INTO "aoi" VALUES('ref_2',2,'','[(534,254),(534,279),(583,279),(583,254),(534,254),(152,282),(152,302),(259,302),(259,283),(152,282)]');
INSERT INTO "aoi" VALUES('ref_1',2,'','[(244,233),(244,253),(578,253),(244,233),(578,233),(152,258),(152,279),(196,279),(196,258),(578,233)]');
INSERT INTO "aoi" VALUES('legend',2,'','[(653,499),(653,557),(1075,557),(1075,499)]');
INSERT INTO "aoi" VALUES('vis',2,'','[(616,94),(616,509),(1090,509),(1090,94)]');
CREATE TABLE intervention_state ( `intervention` TEXT, `active` INTEGER, time_stamp INTEGER, occurences INTEGER, PRIMARY KEY(`intervention`));
CREATE TABLE legend_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE pupil ( `id` INTEGER, `interval_value` INTEGER, `task_value` TEXT, `runtime_value` TEXT, PRIMARY KEY(`id`) );
CREATE TABLE reading_proficiency ( `id` INTEGER, `time_stamp` INTEGER, `raw_prediction` REAL, `value` TEXT, PRIMARY KEY(`id`) );
CREATE TABLE ref_1_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_2_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_3_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_4_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE rule_state ( `rule` TEXT, time_stamp INTEGER, occurences INTEGER, PRIMARY KEY(`rule`));
CREATE TABLE "user_state" (
	`event_name`	TEXT NOT NULL,
	`type`	TEXT,
	`aoi`	TEXT,
	`feature`	TEXT,
	PRIMARY KEY(`event_name`)
);
INSERT INTO "user_state" VALUES('text_fix','fix','text',NULL);
INSERT INTO "user_state" VALUES('pupil','emdat','vis','meanpupilsize');
INSERT INTO "user_state" VALUES('reading_proficiency','ml','',NULL);
INSERT INTO "user_state" VALUES('bad_type','same','text',NULL);
INSERT INTO "user_state" VALUES('vis_fix','fix','vis',NULL);
INSERT INTO "user_state" VALUES('legend_fix','fix','legend',NULL);
INSERT INTO "user_state" VALUES('ref_1_fix','fix','ref_1',NULL);
INSERT INTO "user_state" VALUES('ref_2_fix','fix','ref_2','');
INSERT INTO "user_state" VALUES('ref_3_fix','fix','ref_3',NULL);
INSERT INTO "user_state" VALUES('ref_4_fix','fix','ref_4',NULL);
CREATE TABLE "user_state_task" (
        `event_name`    TEXT,
        `task`  INTEGER,
        PRIMARY KEY(`event_name`,`task`)
);
INSERT INTO "user_state_task" VALUES('text_fix',1);
INSERT INTO "user_state_task" VALUES('pupil',2);
INSERT INTO "user_state_task" VALUES('reading_proficiency',1);
INSERT INTO "user_state_task" VALUES('reading_proficiency',2);
INSERT INTO "user_state_task" VALUES('vis_fix',1);
INSERT INTO "user_state_task" VALUES('legend_fix',1);
INSERT INTO "user_state_task" VALUES('ref_1_fix',1);
INSERT INTO "user_state_task" VALUES('ref_2_fix',1);
INSERT INTO "user_state_task" VALUES('ref_3_fix',1);
INSERT INTO "user_state_task" VALUES('ref_4_fix',1);
INSERT INTO "user_state_task" VALUES('ref_4_fix',2);
INSERT INTO "user_state_task" VALUES('ref_3_fix',2);
INSERT INTO "user_state_task" VALUES('ref_2_fix',2);
INSERT INTO "user_state_task" VALUES('ref_1_fix',2);
INSERT INTO "user_state_task" VALUES('legend_fix',2);
INSERT INTO "user_state_task" VALUES('vis_fix',2);
CREATE TABLE vis_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
COMMIT;
