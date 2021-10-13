BEGIN TRANSACTION;
CREATE TABLE "aoi" (
        `name`  TEXT NOT NULL,
        `task`  INTEGER NOT NULL,
        `dynamic`       INTEGER,
        `polygon`       BLOB,
        PRIMARY KEY(`name`,`task`)
);
INSERT INTO "aoi" VALUES('ref_102',62,'','[(156,207), (156,207), (146,207), (146,327), (344,327), (344,307), (581,307), (581,207)]');
INSERT INTO "aoi" VALUES('ref_100',62,'','[(344,307), (344,327), (146,327), (146,377), (227,377), (227,357), (580,357), (580,307)]');
INSERT INTO "aoi" VALUES('ref_101',62,'','[(227,357), (227,377), (146,377), (146,405), (576,405), (576,382), (580,382), (580,357)]');
INSERT INTO "aoi" VALUES('ref_101',60,'','[(156,207), (156,207), (146,207), (146,304), (576,304), (576,304), (580,304), (580,207)]');
INSERT INTO "aoi" VALUES('ref_100',60,'','[(251,304), (251,327), (146,327), (146,377), (404,377), (404,357), (580,357), (580,304)]');
INSERT INTO "aoi" VALUES('ref_100',66,'','[(544,427), (544,447), (151,447), (151,504), (425,504), (425,477), (581,477), (581,427)]');
INSERT INTO "aoi" VALUES('ref_101',66,NULL,'[(353,352), (353,372), (151,372), (151,447), (544,447), (544,427), (581,427), (581,352)]');
INSERT INTO "aoi" VALUES('ref_100',72,'','[(576,227), (576,227), (146,227), (146,297), (453,297), (453,277), (581,277), (581,227)]');
INSERT INTO "aoi" VALUES('ref_101',72,'','[(204,352), (204,372), (146,372), (146,422), (363,422), (363,402), (581,402), (581,352)]');
INSERT INTO "aoi" VALUES('ref_102',72,NULL,'[(453,277), (453,297), (146,297), (146,372), (204,372), (204,352), (581,352), (581,277)]');
INSERT INTO "aoi" VALUES('ref_101',74,NULL,'[(576,332), (576,332), (146,332), (146,432), (455,432), (455,407), (580,407), (580,332)]');
INSERT INTO "aoi" VALUES('ref_100',76,NULL,'[(477,353), (477,377), (146,377), (146,431), (526,431), (526,407), (580,407), (580,353)]');
INSERT INTO "aoi" VALUES('ref_102',30,NULL,'[(323,277), (323,297), (146,297), (146,352), (511,352), (511,327), (581,327), (580,277)]');
INSERT INTO "aoi" VALUES('ref_100',28,NULL,'[(481,202), (481,222), (150,222), (150,297), (242,297), (242,277), (580,277), (580,202)]');
INSERT INTO "aoi" VALUES('ref_101',28,NULL,'[(242,277), (242,297), (150,297), (150,326), (574,326), (574,302), (580,302), (580,277)]');
INSERT INTO "aoi" VALUES('ref_102',28,NULL,'[(574,326), (574,326), (150,326), (150,372), (528,372), (528,352), (579,352), (579,326)]');
INSERT INTO "aoi" VALUES('ref_103',28,NULL,'[(370,402), (370,422), (150,422), (150,476), (440,476), (440,452), (580,452), (580,402)]');
INSERT INTO "aoi" VALUES('ref_104',28,NULL,'[(315,352), (315,372), (150,372), (150,422), (370,422), (370,402), (579,402), (579,352)]');
INSERT INTO "aoi" VALUES('ref_102',27,NULL,'[(463,402), (463,422), (150,422), (150,472), (410,472), (410,452), (580,452), (580,402)]');
INSERT INTO "aoi" VALUES('ref_103',27,NULL,'[(410,252), (410,272), (150,272), (150,422), (463,422), (463,402), (580,402), (580,252)]');
INSERT INTO "aoi" VALUES('ref_104',27,NULL,'[(410,452), (410,472), (150,472), (150,547), (219,547), (219,527), (579,527), (579,452)]');
INSERT INTO "aoi" VALUES('ref_100',20,NULL,'[(344,202), (344,222), (146,222), (146,297), (492,297), (492,277), (580,277), (580,202)]');
INSERT INTO "aoi" VALUES('ref_101',20,NULL,'[(492,277), (492,297), (146,297), (150,375), (545,375), (545,352), (579,352), (580,277)]');
INSERT INTO "aoi" VALUES('ref_100',18,NULL,'[(221,402), (221,422), (146,422), (146,497), (400,497), (400,477), (580,477), (580,402)]');
INSERT INTO "aoi" VALUES('ref_101',18,NULL,'[(479,352), (479,372), (146,372), (146,422), (221,422), (221,402), (580,402), (580,352)]');
INSERT INTO "aoi" VALUES('ref_102',18,NULL,'[(400,477), (400,497), (146,497), (146,547), (576,547), (576,527), (580,527), (580,477)]');
INSERT INTO "aoi" VALUES('ref_103',18,NULL,'[(471,602), (471,622), (146,622), (146,722), (513,722), (513,702), (580,702), (580,602)]');
INSERT INTO "aoi" VALUES('ref_101',11,NULL,'[(156,237), (156,257), (146,257), (576,357), (576,357), (576,337), (581,337), (581,237)]');
INSERT INTO "aoi" VALUES('ref_100',9,NULL,'[(334,407), (334,427), (146,427), (146,527), (470,527), (470,507), (580,507), (580,407)]');
INSERT INTO "aoi" VALUES('ref_101',9,NULL,'[(309,307), (309,327), (146,327), (146,427), (334,427), (334,407), (580,407), (580,307)]');
INSERT INTO "aoi" VALUES('ref_100',5,NULL,'[(389,327), (389,327), (150,327), (150,452), (425,452), (425,432), (579,432), (579,327)]');
INSERT INTO "aoi" VALUES('ref_101',5,NULL,'[(425,432), (425,452), (150,452), (150,527), (277,527), (277,507), (579,507), (579,432)]');
INSERT INTO "aoi" VALUES('ref_103',5,NULL,'[(277,507), (277,527), (150,527), (150,602), (421,602), (421,582), (579,582), (579,507)]');
INSERT INTO "aoi" VALUES('ref_104',5,NULL,'[(421,582), (421,602), (150,602), (150,656), (574,656), (574,632), (580,632), (580,582)]');
INSERT INTO "aoi" VALUES('ref_106',5,NULL,'[(574,756), (574,756), (150,756), (150,827), (483,827), (483,807), (580,807), (580,756)]');
INSERT INTO "aoi" VALUES('ref_109',5,NULL,'[(574,656), (574,656), (150,656), (150,756), (574,756), (574,732), (579,732), (579,656)]');
INSERT INTO "aoi" VALUES('ref_110',5,NULL,'[(483,807), (483,827), (150,827), (150,927), (253,927), (253,907), (580,907), (580,807)]');
INSERT INTO "aoi" VALUES('ref_100',3,NULL,'[(379,507), (379,527), (146,527), (146,577), (419,577), (419,557), (580,557), (580,507)]');
INSERT INTO "aoi" VALUES('ref_101',3,NULL,'[(359,432), (359,452), (146,452), (146,527), (379,527), (379,507), (580,507), (580,432)]');
INSERT INTO "aoi" VALUES('ref_102',3,NULL,'[(402,682), (402,702), (146,702), (146,802), (387,802), (387,782), (580,782), (580,682)]');
INSERT INTO "aoi" VALUES('ref_104',3,NULL,'[(387,782), (387,802), (146,802), (146,877), (428,877), (428,857), (580,857), (580,782)]');
INSERT INTO "aoi" VALUES('ref_105',3,NULL,'[(419,557), (419,577), (146,577), (146,702), (402,702), (402,682), (580,682), (580,557)]');
INSERT INTO "aoi" VALUES('ref_101',76,'','[(227,275), (227,302), (146,302), (146,331), (273,331), (273,307), (580,307), (580,275)]');
INSERT INTO "aoi" VALUES('ref_106',3,NULL,'[(434,264), (434,275), (146,275), (146,405), (491,401), (490,380), (580,377), (580,253)]');
INSERT INTO "aoi" VALUES('ref_100',30,NULL,'[(576,222), (576,222), (146,222), (146,297), (323,297), (323,277), (581,277), (580,227)]');
CREATE TABLE intervention_state ( `intervention` TEXT, `active` INTEGER, time_stamp INTEGER, occurences INTEGER);
CREATE TABLE ref_100_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_101_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_103_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_104_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_106_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_109_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE ref_110_fix ( `id` INTEGER, `time_start` INTEGER, `time_end` INTEGER, `duration` INTEGER, PRIMARY KEY(`id`) );
CREATE TABLE rule_state ( `rule` TEXT, time_stamp INTEGER, active INTEGER, occurences INTEGER);
CREATE TABLE "user_state" (
	`event_name`	TEXT NOT NULL,
	`type`	TEXT,
	`aoi`	TEXT,
	`feature`	TEXT,
	PRIMARY KEY(`event_name`)
);
INSERT INTO "user_state" VALUES('ref_100_fix','fix','ref_100','');
INSERT INTO "user_state" VALUES('ref_101_fix','fix','ref_101','');
INSERT INTO "user_state" VALUES('ref_102_fix','fix','ref_102','');
INSERT INTO "user_state" VALUES('ref_103_fix','fix','ref_103','');
INSERT INTO "user_state" VALUES('ref_104_fix','fix','ref_104','');
INSERT INTO "user_state" VALUES('ref_105_fix','fix','ref_105','');
INSERT INTO "user_state" VALUES('ref_106_fix','fix','ref_106','');
INSERT INTO "user_state" VALUES('ref_107_fix','fix','ref_107','');
INSERT INTO "user_state" VALUES('ref_108_fix','fix','ref_108','');
INSERT INTO "user_state" VALUES('ref_109_fix','fix','ref_109','');
INSERT INTO "user_state" VALUES('ref_110_fix','fix','ref_110',NULL);
CREATE TABLE "user_state_task" (
        `event_name`    TEXT,
        `task`  INTEGER,
        PRIMARY KEY(`event_name`,`task`)
);
INSERT INTO "user_state_task" VALUES('ref_102_fix',3);
INSERT INTO "user_state_task" VALUES('ref_101_fix',3);
INSERT INTO "user_state_task" VALUES('ref_100_fix',3);
INSERT INTO "user_state_task" VALUES('ref_100_fix',5);
INSERT INTO "user_state_task" VALUES('ref_101_fix',5);
INSERT INTO "user_state_task" VALUES('ref_103_fix',5);
INSERT INTO "user_state_task" VALUES('ref_100_fix',9);
INSERT INTO "user_state_task" VALUES('ref_101_fix',9);
INSERT INTO "user_state_task" VALUES('ref_100_fix',11);
INSERT INTO "user_state_task" VALUES('ref_101_fix',11);
INSERT INTO "user_state_task" VALUES('ref_104_fix',3);
INSERT INTO "user_state_task" VALUES('ref_105_fix',3);
INSERT INTO "user_state_task" VALUES('ref_104_fix',5);
INSERT INTO "user_state_task" VALUES('ref_106_fix',5);
INSERT INTO "user_state_task" VALUES('ref_109_fix',5);
INSERT INTO "user_state_task" VALUES('ref_110_fix',5);
INSERT INTO "user_state_task" VALUES('ref_100_fix',18);
INSERT INTO "user_state_task" VALUES('ref_101_fix',18);
INSERT INTO "user_state_task" VALUES('ref_102_fix',18);
INSERT INTO "user_state_task" VALUES('ref_103_fix',18);
INSERT INTO "user_state_task" VALUES('ref_100_fix',20);
INSERT INTO "user_state_task" VALUES('ref_101_fix',20);
INSERT INTO "user_state_task" VALUES('ref_102_fix',27);
INSERT INTO "user_state_task" VALUES('ref_103_fix',27);
INSERT INTO "user_state_task" VALUES('ref_104_fix',27);
INSERT INTO "user_state_task" VALUES('ref_100_fix',28);
INSERT INTO "user_state_task" VALUES('ref_101_fix',28);
INSERT INTO "user_state_task" VALUES('ref_103_fix',28);
INSERT INTO "user_state_task" VALUES('ref_104_fix',28);
INSERT INTO "user_state_task" VALUES('ref_102_fix',30);
INSERT INTO "user_state_task" VALUES('ref_100_fix',60);
INSERT INTO "user_state_task" VALUES('ref_101_fix',60);
INSERT INTO "user_state_task" VALUES('ref_100_fix',62);
INSERT INTO "user_state_task" VALUES('ref_101_fix',62);
INSERT INTO "user_state_task" VALUES('ref_102_fix',62);
INSERT INTO "user_state_task" VALUES('ref_100_fix',66);
INSERT INTO "user_state_task" VALUES('ref_101_fix',66);
INSERT INTO "user_state_task" VALUES('ref_100_fix',72);
INSERT INTO "user_state_task" VALUES('ref_102_fix',72);
INSERT INTO "user_state_task" VALUES('ref_101_fix',74);
INSERT INTO "user_state_task" VALUES('ref_100_fix',76);
INSERT INTO "user_state_task" VALUES('ref_101_fix',76);
INSERT INTO "user_state_task" VALUES('ref_106_fix',3);
INSERT INTO "user_state_task" VALUES('ref_100_fix',30);
COMMIT;
