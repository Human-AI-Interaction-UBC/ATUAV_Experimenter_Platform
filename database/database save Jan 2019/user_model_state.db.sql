BEGIN TRANSACTION;
CREATE TABLE "user_state_task" (
        `event_name`    TEXT,
        `task`  INTEGER,
        PRIMARY KEY(`event_name`,`task`)
);
INSERT INTO `user_state_task` (event_name,task) VALUES ('text_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('pupil',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('reading_proficiency',1);
INSERT INTO `user_state_task` (event_name,task) VALUES ('reading_proficiency',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('vis_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('legend_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_1_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_2_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_3_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_4_fix',62);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_4_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_3_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_2_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_1_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('legend_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('vis_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('text_fix',3);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_1_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_2_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_3_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_4_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('legend_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('text_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('vis_fix',5);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_1_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_2_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_3_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_4_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('legend_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('vis_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('text_fix',9);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_1_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_2_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_3_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_4_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('text_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('legend_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('vis_fix',11);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_1_fix',2);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_2_fix',2);
INSERT INTO `user_state_task` (event_name,task) VALUES ('ref_3_fix',2);
CREATE TABLE "user_state" (
	`event_name`	TEXT NOT NULL,
	`type`	TEXT,
	`aoi`	TEXT,
	`feature`	TEXT,
	PRIMARY KEY(`event_name`)
);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('text_fix','fix','text',NULL);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('pupil','emdat','vis','meanpupilsize');
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('reading_proficiency','ml','',NULL);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('vis_fix','fix','vis',NULL);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('legend_fix','fix','legend',NULL);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('ref_1_fix','fix','ref_1',NULL);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('ref_2_fix','fix','ref_2','');
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('ref_3_fix','fix','ref_3',NULL);
INSERT INTO `user_state` (event_name,type,aoi,feature) VALUES ('ref_4_fix','fix','ref_4',NULL);
CREATE TABLE "aoi" (
        `name`  TEXT NOT NULL,
        `task`  INTEGER NOT NULL,
        `dynamic`       INTEGER,
        `polygon`       BLOB,
        PRIMARY KEY(`name`,`task`)
);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('text',62,1,'[(132,229),(132,555),(606,555),(606,229)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('vis2',62,1,'[(378,371),(378,401),(553,401),(553,371)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('text',3,1,'[(0,0),(0,100),(100,100),(100,0)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('vis',62,'','[(616,94),(616,509),(1090,509),(1090,94)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('legend',62,'','[(653,499),(653,557),(1075,557),(1075,499)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_1',62,'','[(244,233),(244,253),(578,253),(244,233),(578,233),(152,258),(152,279),(196,279),(196,258),(578,233)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_2',62,'','[(534,254),(534,279),(583,279),(583,254),(534,254),(152,282),(152,302),(259,302),(259,283),(152,282)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_3',62,'','[(256,331),(256,353),(440,353),(440,331)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_4',62,'','[(199,380),(199,404),(380,404),(380,380)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_4',3,'','[(199,380),(199,404),(380,404),(380,380)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_3',3,'','[(256,331),(256,353),(440,353),(440,331)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_2',3,'','[(534,254),(534,279),(583,279),(583,254),(534,254),(152,282),(152,302),(259,302),(259,283),(152,282)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_1',3,'','[(244,233),(244,253),(578,253),(244,233),(578,233),(152,258),(152,279),(196,279),(196,258),(578,233)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('legend',3,'','[(653,499),(653,557),(1075,557),(1075,499)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('vis',3,'','[(616,94),(616,509),(1090,509),(1090,94)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_1',5,'','[(244,233),(244,253),(578,253),(244,233),(578,233),(152,258),(152,279),(196,279),(196,258),(578,233)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_2',5,'','[(534,254),(534,279),(583,279),(583,254),(534,254),(152,282),(152,302),(259,302),(259,283),(152,282)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_3',5,'','[(256,331),(256,353),(440,353),(440,331)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_4',5,'','[(199,380),(199,404),(380,404),(380,380)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('legend',5,'','[(653,499),(653,557),(1075,557),(1075,499)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('vis',5,NULL,'[(616,94),(616,509),(1090,509),(1090,94)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('text',5,NULL,'[(132,229),(132,555),(606,555),(606,229)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_1',9,'','');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_2',9,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_3',9,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_4',9,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('legend',9,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('vis',9,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('text',9,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('8',70,NULL,NULL);
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_1',2,'','[(149,306),(149,328),(345,328),(345,306)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_2',2,'','[(444,329),(444,353),(580,353),(580,329),(444,329),(149,358),(149,376),(230,376),(230,358),(149,358)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('ref_3',2,'','[(381,381),(381,405),(582,405),(582,381)]');
INSERT INTO `aoi` (name,task,dynamic,polygon) VALUES ('12',74,NULL,NULL);
COMMIT;
