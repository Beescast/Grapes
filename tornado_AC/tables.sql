drop database if exists grapes;

create database grapes character set 'utf8';

use grapes;

#原始cookie 数据

CREATE TABLE original_cookie(
uid VARCHAR (15) PRIMARY KEY  NOT NULL,
name VARCHAR (20) NOT NULL ,
cookie json NOT NULL ,
rids VARCHAR (50) ,
level int
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#cookie激活表

CREATE TABLE cookie_used(
uid VARCHAR (15) PRIMARY KEY  NOT NULL,
name VARCHAR (20) NOT NULL ,
rid varchar (10) ,
level int,
dteventtime datetime
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

#cookie未激活表

CREATE TABLE cookie_state(
uid VARCHAR (15) PRIMARY KEY  NOT NULL,
name VARCHAR (20) NOT NULL ,
cookie json NOT NULL ,
rids VARCHAR (50) ,
level int,
flag int
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


-----------------------------
create table ts_cookie
(
 uid int unsigned primary key not null,
 name varchar(50) not null,
 cookies json not null
 );

CREATE TABLE `ta_cookie` (
  `uid` int unsigned NOT NULL,
  `name` varchar(50) NOT NULL,
  `province` varchar(32) NOT NULL,
  `city` varchar(32) NOT NULL,
  `isp` varchar(32) NOT NULL,
  `cookie` json NOT NULL,
  `flag` int(4) NOT NULL,
  `level` int(4) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table tr_user
(
 id int primary key not null auto_increment, 
 IP varchar(50) not null,
 uid int,  
 name varchar(50) not null,
 province varchar(32) not null,
 city varchar(32) not null,
 isp varchar(32) not null,
 flag int(1) not null ,
 dtstarttime datetime,
 dtendtime datetime
);
CREATE TABLE chatdata (
  id int NOT NULL auto_increment,
  rid varchar(15),
  txt varchar(50),
  dteventtime datetime,
  PRIMARY KEY  (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=404227 DEFAULT CHARSET=utf8;


CREATE TABLE `pradata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rid` varchar(15) DEFAULT NULL,
  `txt` varchar(200) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `flag` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE tmp (
  id int NOT NULL auto_increment,
  uid varchar(15),
  time datetime,
  PRIMARY KEY  (`id`)
)

CREATE TABLE `danmu_bac_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rid` varchar(15),
  `danmu_type_id` varchar(45) DEFAULT NULL,
  `cate_name` varchar(45) DEFAULT NULL,
  `cate_id` varchar(45) DEFAULT NULL,
  `txt` text,
  `in_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

CREATE TABLE `tmp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(15) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1039 DEFAULT CHARSET=utf8


CREATE TABLE `self_danmu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `txt` varchar(45) NOT NULL,
  `type` varchar(45) NOT NULL,
  `rid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`txt`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8;

CREATE TABLE `dz_cookie` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uid` varchar(16) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `cookie` json DEFAULT NULL,
  `rid` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

insert into tmp(uid,time) values('126531400','2017-04-11 11:04:48.970000')

select cate_id from roomType where rid='244548'
select count(id) as num from pradata where rid='208114'

desc danmu_data.danmu_bac_data

select * from danmu_data.danmu_bac_data where cate_name="颜值"

insert into ta_cookie values("123",'345',"湖北省","武汉市","CHINANET",'{"acf_ct": "0", "acf_biz": "1", "acf_stk": "3ba7ecb5961a62d9", "acf_uid": "76506310", "acf_auth": "6e0efB5Ylyym7XCG4e4K%2B1MxYH9IImB4Nr006q1m0thlG5p6Rk1Raks5Ah0nECoKNfSx7TOlcLlUNR1UoS4r8Naw6nkVRzzRVnN2EeXbqtgTy5cL6FOI", "acf_devid": "d336ade848437899cbaad1d1ee2cd3e1", "acf_ltkid": "90290247", "acf_groupid": "1", "acf_nickname": "%E9%97%BB%E4%BA%BA%E9%B8%BF%E9%A3%8E", "acf_own_room": "0", "acf_username": "76506310", "wan_auth37wan": "d75f202dc009edxbm6IP2vVNT%2BKs2GIcBv72bg6H8vbaBPRSEMCfoBKUERpOaFW2AeGi7f6LHa%2Bc8rRuB5dDGkOSsvMsGJGE7xZJXFgF8E2ctWa12w", "acf_phonestatus": "1", "_dys_refer_action_code": "show_recommend_dyrecom_room", "Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7": "1490236071"}',1);

grant replication slave on *.* to 'repl'@'%' identified by 'Bees@0831@';

change master to master_host='192.168.3.174',master_port= 3306, master_log_file='mysql-bin.000003', master_log_pos= 4827, master_user='repl',master_password='Bees@0831@';

alter table chatdata convert to charset utf8;
alter table pradata convert to charset utf8;
alter table ta_cookie convert to charset utf8;
alter table ts_cookie convert to charset utf8;
alter table tr_user convert to charset utf8;