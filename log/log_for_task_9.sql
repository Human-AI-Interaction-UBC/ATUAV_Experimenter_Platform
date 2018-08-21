BEGIN TRANSACTION;
CREATE TABLE "aoi" (
        `name`  TEXT NOT NULL,
        `task`  INTEGER NOT NULL,
        `dynamic`       INTEGER,
        `polygon`       BLOB,
        PRIMARY KEY(`name`,`task`)
);
INSERT INTO "aoi" VALUES('text',62,NULL,'[(148,203),(148,558),(583,558),(583,203)]');
INSERT INTO "aoi" VALUES('text',3,NULL,'[(147,204),(147,880),(583,880),(583,204)]');
INSERT INTO "aoi" VALUES('vis',62,'','[(630,74),(630,466),(1083,466),(1083,74)]');
INSERT INTO "aoi" VALUES('legend',62,'','[(658,502),(658,553),(1072,553),(1072,502)]');
INSERT INTO "aoi" VALUES('legend',3,'','[(772,173),(772,215),(962,215),(962,173)]');
INSERT INTO "aoi" VALUES('vis',3,'','[(632,224),(632,622),(1070,622),(1070,224)]');
INSERT INTO "aoi" VALUES('legend',5,'','[(754,192),(754,217),(1055,217),(1055,192)]');
INSERT INTO "aoi" VALUES('vis',5,NULL,'[(620,228),(620,609),(1039,609),(1039,228)]');
INSERT INTO "aoi" VALUES('text',5,NULL,'[(149,205),(149,929),(585,929),(585,205)]');
INSERT INTO "aoi" VALUES('legend',9,NULL,'[(694,173),(694,222),(964,222),(964,173)]');
INSERT INTO "aoi" VALUES('vis',9,NULL,'[(622,226),(622,421),(1024,421),(1024,223)]');
INSERT INTO "aoi" VALUES('text',9,NULL,'[(150,205),(150,531),(581,531),(581,205)]');
INSERT INTO "aoi" VALUES('text',11,'','[(151,234),(151,510),(581,510),(581,234)]');
INSERT INTO "aoi" VALUES('vis',11,'','[(614,86),(614,465),(1152,465),(1152,86)]');
INSERT INTO "aoi" VALUES('legend',11,'','[(672,121),(672,185),(759,185),(759,121)]');
INSERT INTO "aoi" VALUES('text',18,'','[(151,185),(151,722),(585,722),(585,175)]');
INSERT INTO "aoi" VALUES('vis',18,'','[(606,144),(606,449),(1186,449),(1186,144)]');
INSERT INTO "aoi" VALUES('legend',18,'','[(1073,168),(1073,230),(1149,230),(1149,168)]');
INSERT INTO "aoi" VALUES('text',27,'','[(150,174),(150,549),(580,549),(580,174)]');
INSERT INTO "aoi" VALUES('vis',27,'','[(611,152),(611,555),(897,555),(897,152)]');
INSERT INTO "aoi" VALUES('legend',27,'','[(637,131),(637,149),(896,149),(896,131)]');
INSERT INTO "aoi" VALUES('text',28,'','[(150,175),(150,473),(582,473),(582,175)]');
INSERT INTO "aoi" VALUES('vis',28,NULL,'[(606,154),(606,557),(892,557),(892,154)]');
INSERT INTO "aoi" VALUES('legend',28,NULL,'[(636,135),(636,154),(899,154),(899,135)]');
INSERT INTO "aoi" VALUES('text',30,'','[(148,173),(148,351),(580,351),(580,173)]');
INSERT INTO "aoi" VALUES('vis',30,NULL,'[(602,146),(602,539),(899,539),(899,146)]');
INSERT INTO "aoi" VALUES('legend',30,NULL,'[(674,115),(674,146),(883,146),(883,115)]');
INSERT INTO "aoi" VALUES('text',60,NULL,'[(149,204),(149,378),(582,378),(582,204)]');
INSERT INTO "aoi" VALUES('vis',60,NULL,'[(598,72),(598,474),(1075,474),(1075,72)]');
INSERT INTO "aoi" VALUES('legend',60,NULL,'[(641,479),(641,527),(886,527),(886,479)]');
INSERT INTO "aoi" VALUES('text',72,NULL,'[(146,172),(146,425),(585,425),(585,172)]');
INSERT INTO "aoi" VALUES('vis',72,NULL,'[(599,125),(599,357),(1018,357),(1018,125)]');
INSERT INTO "aoi" VALUES('legend',72,NULL,'[(939,223),(939,302),(1018,302),(1018,223)]');
CREATE TABLE intervention_state ( `intervention` TEXT, `active` INTEGER, time_stamp INTEGER, occurences INTEGER, PRIMARY KEY(`intervention`));
INSERT INTO "intervention_state" VALUES('legend_intervention',1,1534869952719693,1);
CREATE TABLE legend_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE rule_state ( `rule` TEXT, time_stamp INTEGER, occurences INTEGER, PRIMARY KEY(`rule`));
INSERT INTO "rule_state" VALUES('legend_28',1534869952719693,1);
CREATE TABLE text_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
INSERT INTO "text_fix" VALUES(1,1534869951404006,1534869951695335,291329);
INSERT INTO "text_fix" VALUES(2,1534869951720464,1534869951911924,191460);
INSERT INTO "text_fix" VALUES(3,1534869951953548,1534869952261501,307953);
CREATE TABLE "user_state" (
	`event_name`	TEXT NOT NULL,
	`type`	TEXT,
	`aoi`	TEXT,
	`feature`	TEXT,
	PRIMARY KEY(`event_name`)
);
INSERT INTO "user_state" VALUES('text_fix','fix','text',NULL);
INSERT INTO "user_state" VALUES('pupil','emdat','vis','meanpupilsize');
INSERT INTO "user_state" VALUES('vis_fix','fix','vis',NULL);
INSERT INTO "user_state" VALUES('legend_fix','fix','legend',NULL);
CREATE TABLE "user_state_task" (
        `event_name`    TEXT,
        `task`  INTEGER,
        PRIMARY KEY(`event_name`,`task`)
);
INSERT INTO "user_state_task" VALUES('text_fix',62);
INSERT INTO "user_state_task" VALUES('vis_fix',62);
INSERT INTO "user_state_task" VALUES('legend_fix',62);
INSERT INTO "user_state_task" VALUES('legend_fix',3);
INSERT INTO "user_state_task" VALUES('vis_fix',3);
INSERT INTO "user_state_task" VALUES('text_fix',3);
INSERT INTO "user_state_task" VALUES('legend_fix',5);
INSERT INTO "user_state_task" VALUES('text_fix',5);
INSERT INTO "user_state_task" VALUES('vis_fix',5);
INSERT INTO "user_state_task" VALUES('legend_fix',9);
INSERT INTO "user_state_task" VALUES('vis_fix',9);
INSERT INTO "user_state_task" VALUES('text_fix',9);
INSERT INTO "user_state_task" VALUES('text_fix',11);
INSERT INTO "user_state_task" VALUES('legend_fix',11);
INSERT INTO "user_state_task" VALUES('vis_fix',11);
INSERT INTO "user_state_task" VALUES('text_fix',18);
INSERT INTO "user_state_task" VALUES('vis_fix',18);
INSERT INTO "user_state_task" VALUES('legend_fix',18);
INSERT INTO "user_state_task" VALUES('text_fix',27);
INSERT INTO "user_state_task" VALUES('vis_fix',27);
INSERT INTO "user_state_task" VALUES('legend_fix',27);
INSERT INTO "user_state_task" VALUES('text_fix',28);
INSERT INTO "user_state_task" VALUES('vis_fix',28);
INSERT INTO "user_state_task" VALUES('legend_fix',28);
INSERT INTO "user_state_task" VALUES('text_fix',30);
INSERT INTO "user_state_task" VALUES('vis_fix',30);
INSERT INTO "user_state_task" VALUES('legend_fix',30);
INSERT INTO "user_state_task" VALUES('text_fix',60);
INSERT INTO "user_state_task" VALUES('vis_fix',60);
INSERT INTO "user_state_task" VALUES('legend_fix',60);
INSERT INTO "user_state_task" VALUES('text_fix',72);
INSERT INTO "user_state_task" VALUES('vis_fix',72);
INSERT INTO "user_state_task" VALUES('legend_fix',72);
CREATE TABLE vis_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
INSERT INTO "vis_fix" VALUES(4,1534869952369865,1534869952719693,349828);
INSERT INTO "vis_fix" VALUES(5,1534869953210854,1534869953360708,149854);
INSERT INTO "vis_fix" VALUES(6,1534869953369093,1534869953493942,124849);
INSERT INTO "vis_fix" VALUES(7,1534869953502321,1534869953793780,291459);
COMMIT;
