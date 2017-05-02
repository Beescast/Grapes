-- MySQL dump 10.14  Distrib 5.5.36-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bocms
-- ------------------------------------------------------
-- Server version	5.5.36-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `boc_acount`
--

DROP TABLE IF EXISTS `boc_acount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_acount` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL COMMENT 'Mail作为帐号',
  `uname` varchar(50) NOT NULL COMMENT '帐号',
  `nickname` varchar(50) NOT NULL COMMENT '显示名称',
  `pwd` varchar(64) NOT NULL COMMENT '密码',
  `tel` varchar(30) NULL COMMENT '电话',
  `phone` varchar(30) NULL COMMENT '手机',
  `addr` varchar(100) NULL COMMENT '地址',
  `photo` varchar(100) NULL COMMENT '头像',
  `thumb` varchar(100) NULL COMMENT '缩略图',
  `status` int(1) NOT NULL DEFAULT '1' COMMENT '用户状态，0 禁用',
  `login_today` int(11) NOT NULL COMMENT '今日登录次数',
  `pwd_errors` int(1) NOT NULL DEFAULT '0' COMMENT '密码错误次数',
  `login_ip` varchar(25) NOT NULL COMMENT '最后登录的IP',
  `reg_time` int(11) NOT NULL COMMENT '添加时间',
  `login_time` int(11) NOT NULL COMMENT '最后一次登录时间',
  `ga` varchar(20) NOT NULL COMMENT 'GA 两部验证密钥 开启与否',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='前端会员帐号';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `boc_article`
--

DROP TABLE IF EXISTS `boc_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一编号',
  `cid` int(11) NOT NULL COMMENT '所属栏目',
  `ccid` int(11) NOT NULL DEFAULT '0' COMMENT '栏目条目ID伪栏目',
  `sort_id` int(11) DEFAULT '0' COMMENT '排序编号',
  `audit` int(1) NOT NULL DEFAULT '0' COMMENT '0:1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `ctype` int(4) NOT NULL DEFAULT '0' COMMENT '默认分类',
  `type_id` int(4) DEFAULT NULL COMMENT '类型',
  `title` tinytext NOT NULL COMMENT '标题',
  `title_seo` tinytext,
  `intro` varchar(500) DEFAULT NULL COMMENT '简介(200汉字)',
  `tags` tinytext COMMENT '标签',
  `content` text COMMENT '内容',
  `timeline` int(11) DEFAULT NULL COMMENT '发布/修改时间',
  `expiretime` int(10) DEFAULT NULL COMMENT '公告过期时间',
  `status` int(1) NOT NULL DEFAULT '0' COMMENT '0:1状态,1 发布，0 草稿',
  `author` varchar(50) DEFAULT NULL COMMENT '消息作者',
  `author_url` tinytext COMMENT '作者链接',
  `source` varchar(50) DEFAULT NULL COMMENT '消息来源',
  `source_url` tinytext COMMENT '来源链接',
  `click` int(11) NOT NULL DEFAULT '0' COMMENT '浏览次数',
  `recommend` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐到分类门户的页面显示',
  `homepage` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐到首页显示',
  `recommend_photo` int(1) NOT NULL DEFAULT '0' COMMENT '0:1作为分类栏目的跑马灯图片新闻',
  `homepage_photo` int(1) NOT NULL DEFAULT '0' COMMENT '0:1作为首页的跑马灯图片新闻',
  `color` int(1) NOT NULL DEFAULT '0' COMMENT '突显状态/颜色',
  `photo` tinytext COMMENT '相关图片',
  `thumb` tinytext COMMENT '图片缩略图',
  `attachment` tinytext COMMENT '附件',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_article`
--

LOCK TABLES `boc_article` WRITE;
/*!40000 ALTER TABLE `boc_article` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_article` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_article_tag`
--

DROP TABLE IF EXISTS `boc_article_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_article_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(30) NOT NULL COMMENT '标签',
  `record` int(11) DEFAULT NULL COMMENT '使用的 article id',
  `count` int(11) DEFAULT NULL COMMENT '计数',
  PRIMARY KEY (`id`),
  KEY `record_index` (`id`,`tag`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='标签表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_article_tag`
--

LOCK TABLES `boc_article_tag` WRITE;
/*!40000 ALTER TABLE `boc_article_tag` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_article_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_columns`
--

DROP TABLE IF EXISTS `boc_columns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_columns` (
  `id` int(4) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `sort_id` int(4) DEFAULT NULL COMMENT '排序',
  `parent_id` int(4) NOT NULL DEFAULT '0' COMMENT '父标识(col id)',
  `depth` int(4) NOT NULL DEFAULT '1' COMMENT '深度',
  `identify` tinytext NOT NULL COMMENT 'url唯一标记(word or link)',
  `path` tinytext NOT NULL COMMENT 'urlpath',
  `title` tinytext NOT NULL COMMENT '标题',
  `title_seo` tinytext NULL COMMENT '优化标题',
  `tags` tinytext NULL COMMENT '标签',
  `intro` text NULL COMMENT '简介',
  `mid` int(2) NOT NULL COMMENT '模型标识(Model id)',
  `temp_index` varchar(50) NULL COMMENT '前台模板栏目index',
  `temp_show` varchar(50) NULL COMMENT '内容展示模板show',
  `status` int(1) NOT NULL DEFAULT '1' COMMENT '0删除 1正常',
  `show` int(1) NOT NULL DEFAULT '1' COMMENT '0隐藏 1正常',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='栏目';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_columns`
--

LOCK TABLES `boc_columns` WRITE;
/*!40000 ALTER TABLE `boc_columns` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_columns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_configs`
--

DROP TABLE IF EXISTS `boc_configs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_configs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_id` int(11) NOT NULL,
  `category` varchar(30) NOT NULL COMMENT '分类',
  `key` varchar(30) NOT NULL COMMENT '键值',
  `value` tinytext NOT NULL COMMENT '值',
  `label` varchar(100) NOT NULL COMMENT '标题',
  `intor` tinytext NULL COMMENT '简介',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COMMENT='配置';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_configs`
--

-- 2015-04-02 09:23:15
LOCK TABLES `boc_configs` WRITE;
INSERT INTO `boc_configs` (`id`, `sort_id`, `category`, `key`, `value`, `label`, `intor`) VALUES
(1,	1,	'adminer',	'title_suffix',	'后台标题后缀',	'标题后缀',	'后端标题栏显示内容的后缀.'),
(2,	9,	'site',	'copyright',	'Copyright 2014',	'CopyRight',	'站点版权内容!'),
(3,	8,	'site',	'email',	'mail@mail.com',	'联系邮箱',	'网站联系人'),
(4,	4,	'site',	'title_suffix',	'标题后缀gh s',	'公司名称|品牌名称',	'前台站点标题的后缀优化'),
(5,	5,	'site',	'title_seo',	'dddd dfdd \nas',	'首页标题[Title]',	'网站首页优化标题'),
(6,	6,	'site',	'tags',	'标签s',	'关键词[Keywords]',	'网站首页关键词设定，使用`,`来间隔标签.'),
(7,	7,	'site',	'intro',	'简介',	'站点描述[Description]',	'网站首页描述'),
(8,	10,	'site',	'icp',	'ICP',	'ICP编号',	''),
(9,	9,	'adminer',	'rember_hours',	'72',	'记住登录',	'记住登录的时间，默认单位为小时。'),
(15,	10,	'adminer',	'nopurview',	'login,welcome,manager,ajax',	'权限过滤',	''),
(10,	11,	'adminer',	'forbidden_hours',	'2',	'登录禁用',	'账户登录错误超过6次时的禁用时间[小时]。'),
(11,	12,	'email',	'stmp',	'smtp.126.com',	'STMP服务器',	''),
(12,	13,	'email',	'account',	'erasin@126.com',	'帐号',	'发送帐号'),
(13,	14,	'email',	'pwd',	'lastway',	'密码',	''),
(14,	15,	'email',	'port',	'25',	'端口',	'STMP端口[25]'),
(22,	12,	'email',	'name',	'电邮名称',	'电邮名称',	'邮件地址显示的名称'),
(16,	3,	'site',	'title',	'前端标题 ss',	'网站标题',	'用于保存前台站点的默认首页标题'),
(17,	1,	'upload',	'upload_size',	'120m',	'上传大小限制',	'默认上传权限大小'),
(18,	2,	'upload',	'inline_file_types',	'gif|jpe?g|png|doc?|mp?|zip|pdf',	'上传后缀过滤',	'文件类型的上传'),
(19,	3,	'upload',	'memory_limit',	'120m',	'内存限制',	''),
(20,	4,	'upload',	'max_file_uploads',	'10',	'上传文件个数',	'个数限制'),
(21,	5,	'upload',	'scale_width',	'0',	'上传图片默认宽度',	'主要为编辑器上传图片设定'),
(23,	7,	'upload',	'watermark',	'0',	'图片水印',	'图片使用背景为透明的PNG格式'),
(24,	0,	'html',	'html',	'0',	'开启静态',	'是否使用静态生成'),
(25,	0,	'html',	'token',	'',	'验证密码',	'对生成页面操作进行验证,用于第三方触发'),
(26,	0,	'html',	'urlmodel',	'0',	'路由模式',	'0:ID;1:标题,2:拼音'),
(27,	6,	'upload',	'scale_height',	'0',	'上传图片高度',	'主要为编辑器上传图片压缩高度');
/*!40000 ALTER TABLE `boc_configs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_feedback`
--

DROP TABLE IF EXISTS `boc_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_id` int(11) DEFAULT NULL COMMENT '排序编号',
  `audit` int(1) NOT NULL DEFAULT '0' COMMENT '0:1审核',
  `type_id` int(11) DEFAULT NULL COMMENT '分类',
  `title` varchar(100) DEFAULT NULL COMMENT '标题',
  `content` text COMMENT '详细内容',
  `answer` text COMMENT '回答问题',
  `username` varchar(50) DEFAULT NULL COMMENT '用户名',
  `tel` varchar(50) DEFAULT NULL COMMENT '电话',
  `fax` varchar(50) CHARACTER SET utf8 COLLATE utf8_estonian_ci DEFAULT NULL COMMENT '传真',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `addr` varchar(100) DEFAULT NULL COMMENT '地址',
  `solve` int(1) DEFAULT '0' COMMENT '解决',
  `show` int(1) DEFAULT NULL COMMENT '是否显示',
  `timeline` int(11) DEFAULT NULL COMMENT '发布时间',
  `timeline_answer` int(11) DEFAULT NULL COMMENT '回复时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='反馈';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_feedback`
--

LOCK TABLES `boc_feedback` WRITE;
/*!40000 ALTER TABLE `boc_feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_gallery`
--

DROP TABLE IF EXISTS `boc_gallery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_gallery` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `cid` int(4) NOT NULL COMMENT '栏目标识',
  `ccid` int(11) NOT NULL DEFAULT '0' COMMENT '栏目条目ID伪栏目',
  `sort_id` int(11) NOT NULL COMMENT '排序',
  `audit` int(1) NOT NULL DEFAULT '0' COMMENT '0:1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `ctype` int(4) NOT NULL DEFAULT '0' COMMENT '默认分类',
  `title` tinytext NULL COMMENT '标题',
  `title_seo` tinytext NULL COMMENT '优化标题',
  `tags` tinytext NULL COMMENT '标签',
  `intro` varbinary(500) NULL COMMENT '简介',
  `photo` text NULL COMMENT '图片列表',
  `thumb` text NULL COMMENT '对应压缩图',
  `timeline` int(11) NOT NULL COMMENT '时间线',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='画廊';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_gallery`
--

LOCK TABLES `boc_gallery` WRITE;
/*!40000 ALTER TABLE `boc_gallery` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_gallery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_honor`
--

DROP TABLE IF EXISTS `boc_honor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_honor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_id` int(11) DEFAULT NULL COMMENT '排序编号',
  `audit` int(1) NOT NULL DEFAULT '0' COMMENT '0:1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `ctype` int(4) NOT NULL DEFAULT '0' COMMENT '默认分类',
  `cid` int(11) NOT NULL COMMENT '所属栏目 columns.id',
  `ccid` int(11) NOT NULL COMMENT '附属栏目id',
  `title` tinytext NOT NULL COMMENT '标题',
  `content` text COMMENT '详细内容',
  `url` tinytext COMMENT 'URL地址',
  `photo` tinytext COMMENT '图片',
  `thumb` tinytext COMMENT '缩略图',
  `show` int(1) DEFAULT '1' COMMENT '是否显示',
  `timeline` int(11) DEFAULT NULL COMMENT '发布日期',
  `title_seo` varchar(250) default NULL,
  `tags` varchar(250) default NULL,
  `intro` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='荣耀';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_honor`
--

LOCK TABLES `boc_honor` WRITE;
/*!40000 ALTER TABLE `boc_honor` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_honor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_links`
--

DROP TABLE IF EXISTS `boc_links`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_links` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `cid` int(4) NOT NULL COMMENT '栏目 id',
  `ccid` int(11) NOT NULL DEFAULT '0' COMMENT '栏目条目ID伪栏目',
  `sort_id` int(11) DEFAULT NULL COMMENT '排序编号',
  `audit` int(1) NOT NULL DEFAULT '0' COMMENT '0:1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `ctype` int(4) NOT NULL DEFAULT '0' COMMENT '默认分类',
  `title` tinytext NOT NULL COMMENT '标题',
  `content` text COMMENT '详细内容',
  `tip` tinytext COMMENT '鼠标悬停提示',
  `link` tinytext COMMENT 'URL地址',
  `photo` tinytext COMMENT '图片',
  `thumb` tinytext COMMENT '缩略图',
  `show` int(1) DEFAULT '1' COMMENT '是否显示',
  `timeline` int(11) DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='友情链接';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_links`
--

LOCK TABLES `boc_links` WRITE;
/*!40000 ALTER TABLE `boc_links` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_links` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_lists`
--

DROP TABLE IF EXISTS `boc_lists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_lists` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `cid` int(4) NOT NULL COMMENT '栏目 id',
  `ccid` int(11) NOT NULL DEFAULT '0' COMMENT '栏目条目ID伪栏目',
  `sort_id` int(11) NOT NULL COMMENT '排序',
  `audit` int(1) NOT NULL DEFAULT '0' COMMENT '0:1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `ctype` int(4) NOT NULL DEFAULT '0' COMMENT '默认分类',
  `title` tinytext NULL COMMENT '小标题',
  `content` text NULL COMMENT '内容',
  `timeline` int(11) NOT NULL COMMENT '时间线',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='小列表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_lists`
--

LOCK TABLES `boc_lists` WRITE;
/*!40000 ALTER TABLE `boc_lists` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_lists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_log`
--

DROP TABLE IF EXISTS `boc_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `controller` VARCHAR(50) NOT NULL,
  `url` MEDIUMTEXT NOT NULL COMMENT '控制器',
  `category` VARCHAR(50) NOT NULL DEFAULT '' COMMENT '级别: 1 view,2update,add,3,del',
  `message` TINYTEXT NOT NULL COMMENT '备注',
  `mid` INT(6) NOT NULL COMMENT '操作人',
  `ip` VARCHAR(20) NOT NULL COMMENT 'IP地址',
  `timeline` INT(11) NOT NULL COMMENT '时间线',
  PRIMARY KEY (`id`)
)
COMMENT='操作日志'
COLLATE='utf8_general_ci'
ENGINE=MyISAM
AUTO_INCREMENT=17;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_log`
--

LOCK TABLES `boc_log` WRITE;
/*!40000 ALTER TABLE `boc_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_manager`
--

DROP TABLE IF EXISTS `boc_manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_manager` (
  `id` int(6) NOT NULL AUTO_INCREMENT,
  `uname` varchar(50) NOT NULL COMMENT '用户名',
  `nickname` varchar(50) NULL COMMENT '显示名称',
  `pwd` varchar(64) NOT NULL COMMENT '密码',
  `gid` varchar(64) NOT NULL DEFAULT '2' COMMENT '用户组ID',
  `email` varchar(100) NOT NULL COMMENT 'email',
  `tel` varchar(30) NULL COMMENT '电话',
  `phone` varchar(30) NULL COMMENT '手机',
  `addr` varchar(100) NULL COMMENT '地址',
  `status` int(1) NOT NULL DEFAULT '1' COMMENT '用户状态，0 禁用',
  `login_today` int(11) NULL COMMENT '今日登录次数',
  `pwd_errors` int(1) NOT NULL DEFAULT '0' COMMENT '密码错误次数',
  `login_ip` varchar(25) NULL COMMENT '最后登录的IP',
  `reg_time` int(11) NULL COMMENT '添加时间',
  `login_time` int(11) NULL COMMENT '最后一次登录时间',
  `ga` int(1) NULL DEFAULT '0' COMMENT 'GA 两部验证密钥 开启与否',
  `getpass` int(11) NULL COMMENT '获取密码时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='后端管理帐号';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_manager`
--

LOCK TABLES `boc_manager` WRITE;
/*!40000 ALTER TABLE `boc_manager` DISABLE KEYS */;
INSERT INTO `boc_manager` VALUES (1,'bocadmin','超级用户','11372a6e7343831f12352cfd049ff59c','1','customservice@bocweb.cn','','','',1,0,0,'127.0.0.1',1376471117,1397098814,1,1389317880);
/*!40000 ALTER TABLE `boc_manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_manager_group`
--

DROP TABLE IF EXISTS `boc_manager_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_manager_group` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `purview` text NOT NULL COMMENT '权限id序列',
  `title` varchar(50) NOT NULL COMMENT '用户组名称',
  `title_en` varchar(50) NOT NULL COMMENT '用户组名称en',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='权限组';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_manager_group`
--

LOCK TABLES `boc_manager_group` WRITE;
/*!40000 ALTER TABLE `boc_manager_group` DISABLE KEYS */;
INSERT INTO `boc_manager_group` VALUES (2,'7afb566e83d3dca2d8a47c8cc29e7e36,ff2fa0336fe8fbc6a51c4707aa47c3e3,a155574e57e9a8a0d0c6ecb1c511da68,fddc215a132fa97ca3c193f1cae5cf9f,c54e594684ebf2862c75ba29d83f71be,2ebbbd65b4e2fc52a3ce44de2160e8d2,12fb6543af2e5541b0fc4f8fdd950be0,8d2159c1e0cf70473e66866eb026e80f,c166381208e23d3f4d65dec1231ccf76,a87d77b65f6d1e8380b3d05290a994d0,430f99bc176c67ec705091d6a5da07d4,d230f6a24270b02237beb82a23e2742f,54b064097df1ab924354f87efcdc4ea0,2338d4221db8f9c52bcc2d64ee436b23,70fc54e47310e38ef19160c17ecd91af,ad92c9d2ad1d512ea852e8ae88f762ff,d0101b9aa277c72e45d078dd8369fc65','用户','users'),(3,'4115dd2b6affc9e3626c695e398f335a,7afb566e83d3dca2d8a47c8cc29e7e36,ff2fa0336fe8fbc6a51c4707aa47c3e3,bfc0ef3829e8d84dfc8d31e5edc26d0f,a155574e57e9a8a0d0c6ecb1c511da68,fddc215a132fa97ca3c193f1cae5cf9f,7d5101dc315695e13463ffdf708b5865,a2756c433a39a2319e61bcd68a758265,5341fd0c5de128ab7979a7414b2e586a,e537f9c0308cbfeb6ee40b4e4c344947,35845fea21044129353364ba21f144a0,efdb91a0f150375b423d8361d254241f,a3c8c3d444880bda2a553b8f3eb6695b,4141c0f8e6a977cd7048cd9d751af350,bbff3957029793ef5163df61fbe018a5,dbc10e6bbc54c0ea6f49e604839f5526,048c50d364a23dfcec0a87aa49e19eb8,c54e594684ebf2862c75ba29d83f71be,3345e3e48188396dc21242fb119ba6b1,a93b06daaedb7fd811ab57131fabc630,af47d02385ccc820bce012061718aff8,78b231e4efafea1d14789b0ad8941cf2,bef23131580195c4a411d4222ef68c9f,214ea1a7fecff45a8447cea07943d068','访客','guest'),(1,'a634cc19664a4f86577556784da60940,7afb566e83d3dca2d8a47c8cc29e7e36,ff2fa0336fe8fbc6a51c4707aa47c3e3,bfc0ef3829e8d84dfc8d31e5edc26d0f,a155574e57e9a8a0d0c6ecb1c511da68,fddc215a132fa97ca3c193f1cae5cf9f,52b7869014f743535798ba509432feb1,a2756c433a39a2319e61bcd68a758265,5341fd0c5de128ab7979a7414b2e586a,e537f9c0308cbfeb6ee40b4e4c344947,c2bc4d65c38311ab74b9dc39680d82df,efdb91a0f150375b423d8361d254241f,a3c8c3d444880bda2a553b8f3eb6695b,4141c0f8e6a977cd7048cd9d751af350,3045880458ee8b8734bf6b3307acd0d5,dbc10e6bbc54c0ea6f49e604839f5526,048c50d364a23dfcec0a87aa49e19eb8,c54e594684ebf2862c75ba29d83f71be,3345e3e48188396dc21242fb119ba6b1,2ebbbd65b4e2fc52a3ce44de2160e8d2,12fb6543af2e5541b0fc4f8fdd950be0,8d2159c1e0cf70473e66866eb026e80f,c166381208e23d3f4d65dec1231ccf76,3025704bb00b809798194964bccb8d3d,60decd16ccd83e013261697b7cc93bc6,7847598074d20e5abc220cb05a606213,afef320193ab13431e6b085c847b8094,9b4b25e0ea18183e9b085cc116246220,2e0115348725a3f383d8daa4354c7c3a,524c66aa98b226bd78bc7e7ad0423de7,66bfe11515e892dbf8bb4a5a92792e8b,50b03d671787f35800682c10c90a75bf,a1873764d0aa66fa9c6d34e16dcc86c2,0e69c6f28f25c24fe241da13093f9b12,6d119f7ae0c3c090ed51e672203c000f,7ff25ae6e8120b5ae5b5fb7b86a11641,53a396649c27c4e0dbd96fe57c2377e9,f59d0f67b7223a083e4449d583e90307,a41e16b61dd21e98c8143409d807890b,e44bd2f89f2820521a93c981c8af920d,f729102b0a0a547d20a4322e2d12cf71,7cf04cb70fa2f26d449acfb7974fd417,a7cd680c1676df4fdb93e7bdd83d6b3c,5f667ab7322f039e4e7e0ba8b04edf2f,6470d2304686b20640688c6d9dc44b46,df53f98d0b09ef3173cc8d594671fa6f,051071e245077a8126a4607e2148f327,224a58fde770d8718f7c06ac852fd9ae,0309718bf1a4785dcbf1e34461213c3e,d174c0a461db66945abcd861216dd94a,494b71b75af1e63c628544872f3c54d4,454f6e4ce4e57bd58eefda7d3fea1fa5,a87d77b65f6d1e8380b3d05290a994d0,430f99bc176c67ec705091d6a5da07d4,d230f6a24270b02237beb82a23e2742f,e5ba15d009798276692f84b4e0c9c1e9,026e09db119a340d72c2d5a611dfedb1,33a3ca4433131ad797eb4a7ff8bdb40b,87f64ed3bd52c1d6396fcb9908cb7fdf','管理员','root');
/*!40000 ALTER TABLE `boc_manager_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_manager_purview`
--

DROP TABLE IF EXISTS `boc_manager_purview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_manager_purview` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `model` varchar(30) NOT NULL COMMENT '控制模型',
  `method` varchar(30) NOT NULL COMMENT '控制函数',
  `cid` varchar(30) DEFAULT NULL COMMENT 'column id 参数',
  `uri` varchar(64) NOT NULL COMMENT '权限地址md5(model/method)',
  `title` varchar(50) NOT NULL COMMENT '权限名称',
  `status` int(1) NOT NULL DEFAULT '0' COMMENT '是否使用权限',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=455 DEFAULT CHARSET=utf8 COMMENT='用户组权限';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_manager_purview`
--

LOCK TABLES `boc_manager_purview` WRITE;
/*!40000 ALTER TABLE `boc_manager_purview` DISABLE KEYS */;
INSERT INTO `boc_manager_purview` (`id`, `model`, `method`, `cid`, `uri`, `title`, `status`) VALUES
  (313, 'configs', 'index', '', 'fddc215a132fa97ca3c193f1cae5cf9f', '配置查看', 1),
  (314, 'configs', 'set', '', 'a155574e57e9a8a0d0c6ecb1c511da68', '配置修改', 1),
  (315, 'columns', 'index', '', 'bfc0ef3829e8d84dfc8d31e5edc26d0f', '栏目列表', 1),
  (316, 'columns', 'create', '', 'ff2fa0336fe8fbc6a51c4707aa47c3e3', '栏目添加', 1),
  (317, 'columns', 'edit', '', '7afb566e83d3dca2d8a47c8cc29e7e36', '栏目修改', 1),
  (318, 'columns', 'delete', '', '4115dd2b6affc9e3626c695e398f335a', '栏目删除', 1),
  (319, 'modules', 'index', '', 'c54e594684ebf2862c75ba29d83f71be', '模型查看', 1),
  (320, 'modules', 'create', '', '048c50d364a23dfcec0a87aa49e19eb8', '模型添加', 1),
  (321, 'modules', 'edit', '', 'dbc10e6bbc54c0ea6f49e604839f5526', '模型修改', 1),
  (322, 'modules', 'delete', '', 'bbff3957029793ef5163df61fbe018a5', '删除模型', 1),
  (323, 'manager_purview', 'index', '', '4141c0f8e6a977cd7048cd9d751af350', '权限管理', 1),
  (324, 'manager_purview', 'create', '', 'a3c8c3d444880bda2a553b8f3eb6695b', '权限添加', 1),
  (325, 'manager_purview', 'edit', '', 'efdb91a0f150375b423d8361d254241f', '权限修改', 1),
  (326, 'manager_purview', 'delete', '', '35845fea21044129353364ba21f144a0', '权限删除', 1),
  (327, 'manager_group', 'index', '', 'e537f9c0308cbfeb6ee40b4e4c344947', '用户组查看', 1),
  (328, 'manager_group', 'create', '', '5341fd0c5de128ab7979a7414b2e586a', '用户组添加', 1),
  (329, 'manager_group', 'edit', '', 'a2756c433a39a2319e61bcd68a758265', '用户组修改', 1),
  (330, 'manager_group', 'delete', '', '7d5101dc315695e13463ffdf708b5865', '用户组删除', 1),
  (334, 'upload', 'uploado', '', '3345e3e48188396dc21242fb119ba6b1', '上传', 0);
/*!40000 ALTER TABLE `boc_manager_purview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_modules`
--

DROP TABLE IF EXISTS `boc_modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_modules` (
  `id` int(2) NOT NULL AUTO_INCREMENT COMMENT '模型标识',
  `sort_id` int(2) NOT NULL,
  `title` varchar(50) NOT NULL COMMENT '显示名称',
  `controller` varchar(50) NOT NULL COMMENT '控制器名称',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='栏目模型';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_modules`
--

LOCK TABLES `boc_modules` WRITE;
/*!40000 ALTER TABLE `boc_modules` DISABLE KEYS */;
INSERT INTO `boc_modules` VALUES (1,0,'链接','links'),(3,0,'文章','article'),(6,0,'清单','lists'),(7,3,'期刊','gallery'),(8,1,'单页','page'),(9,4,'产品','product'),(10,0,'招聘','recruit');
/*!40000 ALTER TABLE `boc_modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_msgs`
--

DROP TABLE IF EXISTS `boc_msgs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_msgs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `title` varchar(100) NOT NULL COMMENT '标题',
  `msg` tinytext NULL COMMENT '提示消息',
  `level` int(1) NULL DEFAULT '1' COMMENT '类型: 1notie 2info 3 success 4error',
  `timeline` int(11) NOT NULL COMMENT '时间',
  `markread` int(1) NOT NULL COMMENT '是否阅读',
  `notify` int(1) NULL DEFAULT '0' COMMENT '是否提示过',
  `byer` int(6) NOT NULL DEFAULT '0' COMMENT '发送者 mid system is 0',
  `toer` int(6) NOT NULL COMMENT '接受者 mid',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='消息提示';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_msgs`
--

LOCK TABLES `boc_msgs` WRITE;
/*!40000 ALTER TABLE `boc_msgs` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_msgs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_page`
--

DROP TABLE IF EXISTS `boc_page`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_page` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一编号',
  `cid` int(4) DEFAULT NULL COMMENT '栏目id',
  `ccid` int(11) DEFAULT '0' COMMENT '栏目条目ID伪栏目',
  `sort_id` int(11) DEFAULT '0' COMMENT '排序编号',
  `audit` int(1) DEFAULT '0' COMMENT '审核',
  `title` tinytext NULL COMMENT '标题',
  `title_seo` tinytext,
  `intro` varchar(500) DEFAULT NULL COMMENT '简介(200汉字)',
  `tags` tinytext COMMENT '标签',
  `content` text COMMENT '内容',
  `photo` varchar(200) DEFAULT NULL COMMENT '图片组',
  `thumb` varchar(200) DEFAULT NULL COMMENT '缩略图',
  `template` varchar(200) DEFAULT NULL COMMENT '模板',
  `timeline` int(10) DEFAULT NULL COMMENT '发布/修改时间',
  `attachment` tinytext COMMENT '附件',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='单页表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_page`
--

LOCK TABLES `boc_page` WRITE;
/*!40000 ALTER TABLE `boc_page` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_page` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_product`
--

DROP TABLE IF EXISTS `boc_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) DEFAULT NULL COMMENT '栏目id',
  `sort_id` int(11) DEFAULT '1' COMMENT '排序编号',
  `ccid` int(11) NOT NULL DEFAULT '0' COMMENT '栏目条目ID伪栏目',
  `audit` int(1) DEFAULT '0' COMMENT '0/1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `ctype` int(4) NOT NULL DEFAULT '0' COMMENT '默认分类',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `title_seo` varchar(255) DEFAULT NULL COMMENT '优化标题',
  `intro` varchar(500) DEFAULT NULL COMMENT '简介',
  `tags` varchar(255) DEFAULT NULL COMMENT '标签',
  `content` mediumtext COMMENT '内容',
  `photo` varchar(255) DEFAULT NULL COMMENT '图片',
  `thumb` varchar(255) DEFAULT NULL COMMENT '缩略图',
  `show` tinyint(1) DEFAULT '1' COMMENT '是否显示',
  `click` int(11) DEFAULT '0' COMMENT '点击量',
  `timeline` int(11) DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='产品';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_product`
--

LOCK TABLES `boc_product` WRITE;
/*!40000 ALTER TABLE `boc_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_product_child`
--

DROP TABLE IF EXISTS `boc_product_child`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_product_child` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sort_id` int(11) DEFAULT NULL COMMENT '排序编号',
  `type_id` int(11) DEFAULT NULL COMMENT '分类',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `photo` varchar(255) DEFAULT NULL COMMENT '图片',
  `thumb` varchar(255) DEFAULT NULL COMMENT '缩略图',
  `show` int(11) DEFAULT '1' COMMENT '是否显示',
  `timeline` int(11) DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_product_child`
--

LOCK TABLES `boc_product_child` WRITE;
/*!40000 ALTER TABLE `boc_product_child` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_product_child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_product_type`
--

DROP TABLE IF EXISTS `boc_product_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_product_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) DEFAULT '1',
  `parent_id` int(11) DEFAULT NULL,
  `depth` int(11) DEFAULT '0',
  `path` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `intro` varchar(1000) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `thumb` varchar(255) DEFAULT NULL,
  `order_id` int(11) DEFAULT '0',
  `timeline` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `path_index` (`path`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_product_type`
--

LOCK TABLES `boc_product_type` WRITE;
/*!40000 ALTER TABLE `boc_product_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_product_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_province`
--

DROP TABLE IF EXISTS `boc_province`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_province` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `title` varchar(50) DEFAULT NULL COMMENT '标题',
  `entitle` varchar(50) DEFAULT NULL COMMENT '英文标题',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=utf8 COMMENT='省级列表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_province`
--

LOCK TABLES `boc_province` WRITE;
/*!40000 ALTER TABLE `boc_province` DISABLE KEYS */;
INSERT INTO `boc_province` VALUES (1,'北京市','BeiJing'),(2,'天津市','Tianjin'),(3,'河北省','Hebei'),(4,'山西省','Shanxi'),(5,'辽宁省','Liaoning'),(6,'吉林省','Jilin'),(7,'上海市','Shanghai'),(8,'江苏省','Jiangsu'),(9,'浙江省','Zhejiang'),(10,'安徽省','Anhui'),(11,'福建省','Fujian'),(12,'江西省','Jiangxi'),(13,'山东省','Shandong'),(14,'河南省','Henan'),(15,'内蒙古','Neimenggu'),(16,'黑龙江省','Heilongjiang'),(17,'湖北省','Hubei'),(18,'湖南省','Hunan'),(19,'广东省','Guangdong'),(20,'广西省','Guangxi'),(21,'海南省','Hainan'),(22,'四川省','Sichuan'),(23,'重庆市','Chongqing'),(24,'台湾省','Taiwan'),(25,'贵州省','Guizhou'),(26,'云南省','Yunnan'),(27,'西藏','Xizang'),(28,'陕西省','Shanxi'),(29,'甘肃省','Gansu'),(30,'青海省','Qinghai'),(31,'宁夏','Ningxia'),(32,'新疆','Xinjiang'),(33,'香港','xianggang'),(34,'澳门','aomen'),(35,'钓鱼岛','Diaoyudao');
/*!40000 ALTER TABLE `boc_province` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_province_city`
--

DROP TABLE IF EXISTS `boc_province_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_province_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `province_id` int(11) NOT NULL DEFAULT '0' COMMENT '省级id',
  `title` varchar(50) DEFAULT NULL COMMENT '标题',
  `entitle` varchar(50) DEFAULT NULL COMMENT '英文标题',
  `weather` varchar(11) DEFAULT NULL COMMENT '国家天气ID',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=384 DEFAULT CHARSET=utf8 COMMENT='城市列表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_province_city`
--

LOCK TABLES `boc_province_city` WRITE;
/*!40000 ALTER TABLE `boc_province_city` DISABLE KEYS */;
INSERT INTO `boc_province_city` VALUES (1,1,'北京',NULL,'101010100'),(2,2,'天津',NULL,'101030100'),(3,3,'石家庄',NULL,'101090101'),(4,3,'保定',NULL,'101090201'),(5,3,'沧州',NULL,'101090701'),(6,3,'承德',NULL,'101090402'),(7,3,'邯郸',NULL,'101091001'),(8,3,'衡水',NULL,'101090801'),(9,3,'廊坊',NULL,'101090601'),(10,3,'秦皇岛',NULL,'101091101'),(11,3,'唐山',NULL,'101090501'),(12,3,'邢台',NULL,'101090901'),(13,3,'张家口',NULL,'101090301'),(14,4,'太原',NULL,'101100101'),(15,4,'长治',NULL,'101100501'),(16,4,'大同',NULL,'101100201'),(17,4,'晋城',NULL,'101100601'),(18,4,'晋中',NULL,'101100401'),(19,4,'临汾',NULL,'101100701'),(20,4,'吕梁',NULL,'101101101'),(21,4,'朔州',NULL,'101100901'),(22,4,'忻州',NULL,'101101001'),(23,4,'阳泉',NULL,'101100301'),(24,4,'运城',NULL,'101100801'),(25,5,'沈阳',NULL,'101070101'),(26,5,'大连',NULL,'101070201'),(27,5,'鞍山',NULL,'101070301'),(28,5,'本溪',NULL,'101070501'),(29,5,'朝阳',NULL,'101071201'),(30,5,'丹东',NULL,'101070601'),(31,5,'抚顺',NULL,'101070401'),(32,5,'阜新',NULL,'101070901'),(33,5,'葫芦岛',NULL,'101071401'),(34,5,'锦州',NULL,'101070701'),(35,5,'辽阳',NULL,'101071001'),(36,5,'盘锦',NULL,'101071301'),(37,5,'铁岭',NULL,'101071101'),(38,5,'营口',NULL,'101070801'),(39,6,'长春',NULL,'101060101'),(40,6,'吉林',NULL,'101060201'),(41,6,'白城',NULL,'101060601'),(42,6,'白山',NULL,'101060901'),(43,6,'辽源',NULL,'101060701'),(44,6,'四平',NULL,'101060401'),(45,6,'松原',NULL,'101060801'),(46,6,'通化',NULL,'101060501'),(47,6,'延边朝鲜族自治州',NULL,NULL),(48,7,'上海',NULL,'101020100'),(49,8,'南京',NULL,'101190101'),(50,8,'常州',NULL,'101191101'),(51,8,'淮安',NULL,'101190901'),(52,8,'连云港',NULL,'101191001'),(53,8,'南通',NULL,'101190501'),(54,8,'苏州',NULL,'101190401'),(55,8,'宿迁',NULL,'101191301'),(56,8,'泰州',NULL,'101191201'),(57,8,'无锡',NULL,'101190201'),(58,8,'徐州',NULL,'101190801'),(59,8,'盐城',NULL,'101190701'),(60,8,'扬州',NULL,'101190601'),(61,8,'镇江',NULL,'101190301'),(62,9,'杭州',NULL,'101210101'),(63,9,'湖州',NULL,'101210201'),(64,9,'嘉兴',NULL,'101210301'),(65,9,'金华',NULL,'101210901'),(66,9,'丽水',NULL,'101210801'),(67,9,'宁波',NULL,'101210401'),(68,9,'绍兴',NULL,'101210501'),(69,9,'台州',NULL,'101210601'),(70,9,'温州',NULL,'101210701'),(71,9,'舟山',NULL,'101211101'),(72,9,'衢州',NULL,'101211001'),(73,10,'合肥',NULL,'101220101'),(74,10,'安庆',NULL,'101220601'),(75,10,'蚌埠',NULL,'101220201'),(76,10,'巢湖',NULL,'101221601'),(77,10,'池州',NULL,'101221701'),(78,10,'滁州',NULL,'101221101'),(79,10,'阜阳',NULL,'101220801'),(80,10,'淮北',NULL,'101221201'),(81,10,'淮南',NULL,'101220401'),(82,10,'黄山',NULL,NULL),(83,10,'六安',NULL,'101221501'),(84,10,'马鞍山',NULL,'101220501'),(85,10,'宿州',NULL,'101220701'),(86,10,'铜陵',NULL,'101221301'),(87,10,'芜湖',NULL,'101220301'),(88,10,'宣城',NULL,'101221401'),(89,10,'亳州',NULL,NULL),(90,11,'福州',NULL,'101230101'),(91,11,'厦门',NULL,'101230201'),(92,11,'龙岩',NULL,'101230701'),(93,11,'南平',NULL,'101230901'),(94,11,'宁德',NULL,'101230301'),(95,11,'莆田',NULL,'101230401'),(96,11,'泉州',NULL,'101230501'),(97,11,'三明',NULL,'101230801'),(98,11,'漳州',NULL,'101230601'),(99,12,'南昌',NULL,'101240101'),(100,12,'抚州',NULL,'101240401'),(101,12,'赣州',NULL,'101240701'),(102,12,'吉安',NULL,'101240601'),(103,12,'景德镇',NULL,'101240801'),(104,12,'九江',NULL,'101240201'),(105,12,'萍乡',NULL,'101240901'),(106,12,'上饶',NULL,'101240301'),(107,12,'新余',NULL,'101241001'),(108,12,'宜春',NULL,'101240501'),(109,12,'鹰潭',NULL,'101241101'),(110,13,'济南',NULL,'101120101'),(111,13,'青岛',NULL,'101120201'),(112,13,'烟台',NULL,'101120501'),(113,13,'滨州',NULL,'101121101'),(114,13,'德州',NULL,'101120401'),(115,13,'东营',NULL,'101121201'),(116,13,'菏泽',NULL,'101121001'),(117,13,'济宁',NULL,'101120701'),(118,13,'莱芜',NULL,'101121601'),(119,13,'聊城',NULL,'101121701'),(120,13,'临沂',NULL,'101120901'),(121,13,'日照',NULL,'101121501'),(122,13,'泰安',NULL,'101120801'),(123,13,'威海',NULL,'101121301'),(124,13,'潍坊',NULL,'101120601'),(125,13,'枣庄',NULL,'101121401'),(126,13,'淄博',NULL,'101120301'),(127,14,'郑州',NULL,'101180101'),(128,14,'洛阳',NULL,'101180901'),(129,14,'开封',NULL,'101180801'),(130,14,'安阳',NULL,'101180201'),(131,14,'鹤壁',NULL,'101181201'),(132,14,'济源',NULL,NULL),(133,14,'焦作',NULL,'101181101'),(134,14,'南阳',NULL,'101180701'),(135,14,'平顶山',NULL,'101180501'),(136,14,'三门峡',NULL,'101181701'),(137,14,'商丘',NULL,'101181001'),(138,14,'新乡',NULL,'101180301'),(139,14,'信阳',NULL,'101180601'),(140,14,'许昌',NULL,'101180401'),(141,14,'周口',NULL,'101181401'),(142,14,'驻马店',NULL,'101181601'),(143,14,'漯河',NULL,'101181501'),(144,14,'濮阳',NULL,'101181301'),(145,15,'呼和浩特',NULL,'101080101'),(146,15,'包头',NULL,'101080201'),(147,15,'赤峰',NULL,'101080601'),(148,15,'鄂尔多斯',NULL,'101080701'),(149,15,'呼伦贝尔',NULL,'101081001'),(150,15,'阿拉善盟',NULL,NULL),(151,15,'巴彦淖尔盟',NULL,NULL),(152,15,'通辽',NULL,'101080501'),(153,15,'乌海',NULL,'101080301'),(154,15,'乌兰察布盟',NULL,NULL),(155,15,'锡林郭勒盟',NULL,NULL),(156,15,'兴安盟',NULL,NULL),(157,16,'哈尔滨',NULL,'101050101'),(158,16,'大庆',NULL,'101050901'),(159,16,'大兴安岭',NULL,'101050701'),(160,16,'鹤岗',NULL,'101051201'),(161,16,'黑河',NULL,'101050601'),(162,16,'鸡西',NULL,'101051101'),(163,16,'佳木斯',NULL,'101050401'),(164,16,'牡丹江',NULL,'101050301'),(165,16,'七台河',NULL,'101051002'),(166,16,'齐齐哈尔',NULL,'101050201'),(167,16,'双鸭山',NULL,'101051301'),(168,16,'绥化',NULL,'101050501'),(169,16,'伊春',NULL,'101050801'),(170,17,'武汉',NULL,'101200101'),(171,17,'鄂州',NULL,'101200301'),(172,17,'黄冈',NULL,'101200501'),(173,17,'黄石',NULL,'101200601'),(174,17,'荆门',NULL,'101201401'),(175,17,'荆州',NULL,'101200801'),(176,17,'潜江',NULL,NULL),(177,17,'十堰',NULL,'101201101'),(178,17,'随州',NULL,'101201301'),(179,17,'天门',NULL,NULL),(180,17,'仙桃',NULL,NULL),(181,17,'咸宁',NULL,'101200701'),(182,17,'襄樊',NULL,NULL),(183,17,'孝感',NULL,'101200401'),(184,17,'宜昌',NULL,'101200901'),(185,17,'恩施土家族苗族自治州',NULL,NULL),(186,17,'神农架林区',NULL,NULL),(187,18,'长沙',NULL,'101250101'),(188,18,'益阳',NULL,'101250701'),(189,18,'湘潭',NULL,'101250201'),(190,18,'常德',NULL,'101250601'),(191,18,'郴州',NULL,'101250501'),(192,18,'衡阳',NULL,'101250401'),(193,18,'怀化',NULL,'101251201'),(194,18,'娄底',NULL,'101250801'),(195,18,'邵阳',NULL,'101250901'),(196,18,'永州',NULL,'101251401'),(197,18,'岳阳',NULL,'101251001'),(198,18,'张家界',NULL,'101251101'),(199,18,'株洲',NULL,'101250301'),(200,18,'湘西土家族苗族自治州',NULL,NULL),(201,19,'广州',NULL,'101280101'),(202,19,'深圳',NULL,'101280601'),(203,19,'珠海',NULL,'101280701'),(204,19,'湛江',NULL,'101281001'),(205,19,'惠州',NULL,'101280301'),(206,19,'江门',NULL,'101281101'),(207,19,'潮州',NULL,'101281501'),(208,19,'汕头',NULL,'101280501'),(209,19,'东莞',NULL,'101281601'),(210,19,'佛山',NULL,'101280800'),(211,19,'河源',NULL,'101281201'),(212,19,'揭阳',NULL,'101281901'),(213,19,'茂名',NULL,'101282001'),(214,19,'梅州',NULL,'101280401'),(215,19,'清远',NULL,'101281301'),(216,19,'汕尾',NULL,'101282101'),(217,19,'韶关',NULL,'101280201'),(218,19,'阳江',NULL,'101281801'),(219,19,'云浮',NULL,'101281401'),(220,19,'肇庆',NULL,'101280901'),(221,19,'中山',NULL,'101281701'),(222,20,'南宁',NULL,'101300101'),(223,20,'桂林',NULL,'101300501'),(224,20,'北海',NULL,'101301301'),(225,20,'百色',NULL,'101301001'),(226,20,'崇左',NULL,'101300201'),(227,20,'防城港',NULL,'101301401'),(228,20,'贵港',NULL,'101300801'),(229,20,'河池',NULL,'101301201'),(230,20,'贺州',NULL,'101300701'),(231,20,'来宾',NULL,'101300401'),(232,20,'柳州',NULL,'101300301'),(233,20,'钦州',NULL,'101301101'),(234,20,'梧州',NULL,'101300601'),(235,20,'玉林',NULL,'101300901'),(236,21,'海口',NULL,'101310101'),(237,21,'三亚',NULL,'101310201'),(238,21,'白沙黎族自治县',NULL,NULL),(239,21,'保亭黎族苗族自治县',NULL,NULL),(240,21,'昌江黎族自治县',NULL,NULL),(241,21,'澄迈县',NULL,NULL),(242,21,'定安县',NULL,NULL),(243,21,'东方',NULL,NULL),(244,21,'乐东黎族自治县',NULL,NULL),(245,21,'临高县',NULL,NULL),(246,21,'陵水黎族自治县',NULL,NULL),(247,21,'琼海',NULL,NULL),(248,21,'琼中黎族苗族自治县',NULL,NULL),(249,21,'屯昌县',NULL,NULL),(250,21,'万宁',NULL,NULL),(251,21,'文昌',NULL,'101310212'),(252,21,'五指山',NULL,NULL),(253,21,'儋州',NULL,'101310205'),(254,22,'成都',NULL,'101270101'),(255,22,'绵阳',NULL,'101270401'),(256,22,'巴中',NULL,'101270901'),(257,22,'达州',NULL,'101270601'),(258,22,'德阳',NULL,'101272001'),(259,22,'广安',NULL,'101270801'),(260,22,'广元',NULL,'101272101'),(261,22,'乐山',NULL,'101271401'),(262,22,'眉山',NULL,'101271501'),(263,22,'南充',NULL,'101270501'),(264,22,'内江',NULL,'101271201'),(265,22,'攀枝花',NULL,'101270201'),(266,22,'遂宁',NULL,'101270701'),(267,22,'雅安',NULL,'101271701'),(268,22,'宜宾',NULL,'101271101'),(269,22,'资阳',NULL,'101271301'),(270,22,'自贡',NULL,'101270301'),(271,22,'泸州',NULL,'101271001'),(272,22,'甘孜藏族自治州',NULL,NULL),(273,22,'阿坝藏族羌族自治州',NULL,NULL),(274,22,'凉山彝族自治州',NULL,NULL),(275,23,'重庆',NULL,'101040100'),(276,24,'台北',NULL,'101340102'),(277,24,'高雄',NULL,'101340201'),(278,24,'台中',NULL,NULL),(279,24,'台南',NULL,NULL),(280,24,'新北',NULL,NULL),(281,24,'基隆',NULL,NULL),(282,24,'新竹',NULL,NULL),(283,24,'嘉义',NULL,NULL),(284,24,'桃园县',NULL,NULL),(285,24,'新竹县',NULL,NULL),(286,24,'苗栗县',NULL,NULL),(287,24,'彰化县',NULL,NULL),(288,24,'南投县',NULL,NULL),(289,24,'云林县',NULL,NULL),(290,24,'嘉义县',NULL,NULL),(291,24,'屏东县',NULL,NULL),(292,24,'宜兰县',NULL,NULL),(293,24,'花莲县',NULL,NULL),(294,24,'台东县',NULL,NULL),(295,24,'澎湖县',NULL,NULL),(296,24,'金门县',NULL,NULL),(297,24,'连江县',NULL,NULL),(298,25,'贵阳',NULL,'101260101'),(299,25,'六盘水',NULL,'101260801'),(300,25,'遵义',NULL,'101260201'),(301,25,'安顺',NULL,'101260301'),(302,25,'毕节',NULL,'101260701'),(303,25,'铜仁',NULL,'101260601'),(304,25,'黔东南苗族侗族自治州',NULL,NULL),(305,25,'黔南布依族苗族自治州',NULL,NULL),(306,25,'黔西南布依族苗族自治州',NULL,NULL),(307,26,'昆明',NULL,'101290101'),(308,26,'丽江',NULL,'101291401'),(309,26,'保山',NULL,'101290501'),(310,26,'楚雄彝族自治州',NULL,NULL),(311,26,'大理白族自治州',NULL,NULL),(312,26,'德宏傣族景颇族自治州',NULL,NULL),(313,26,'迪庆藏族自治州',NULL,NULL),(314,26,'红河哈尼族彝族自治州',NULL,NULL),(315,26,'临沧',NULL,'101291101'),(316,26,'怒江傈傈族自治州',NULL,NULL),(317,26,'曲靖',NULL,'101290401'),(318,26,'思茅',NULL,'101290901'),(319,26,'文山壮族苗族自治州',NULL,NULL),(320,26,'西双版纳傣族自治州',NULL,NULL),(321,26,'玉溪',NULL,'101290701'),(322,26,'昭通',NULL,'101291001'),(323,27,'拉萨',NULL,'101140101'),(324,27,'日喀则',NULL,'101140201'),(325,27,'阿里',NULL,'101140701'),(326,27,'昌都',NULL,'101140501'),(327,27,'林芝',NULL,'101140401'),(328,27,'那曲',NULL,'101140601'),(329,27,'山南',NULL,'101140301'),(330,28,'西安',NULL,'101110101'),(331,28,'宝鸡',NULL,'101110901'),(332,28,'咸阳',NULL,'101110200'),(333,28,'延安',NULL,'101110300'),(334,28,'榆林',NULL,'101110401'),(335,28,'安康',NULL,'101110701'),(336,28,'汉中',NULL,'101110801'),(337,28,'商洛',NULL,'101110601'),(338,28,'铜川',NULL,'101111001'),(339,28,'渭南',NULL,'101110501'),(340,29,'兰州',NULL,'101160101'),(341,29,'白银',NULL,'101161301'),(342,29,'定西',NULL,'101160201'),(343,29,'嘉峪关',NULL,NULL),(344,29,'金昌',NULL,'101160601'),(345,29,'酒泉',NULL,'101160801'),(346,29,'陇南',NULL,NULL),(347,29,'平凉',NULL,'101160301'),(348,29,'庆阳',NULL,'101160401'),(349,29,'天水',NULL,'101160901'),(350,29,'武威',NULL,'101160501'),(351,29,'张掖',NULL,'101160701'),(352,29,'临夏回族自治州',NULL,NULL),(353,29,'甘南藏族自治州',NULL,NULL),(354,30,'西宁',NULL,'101150101'),(355,30,'果洛藏族自治州',NULL,NULL),(356,30,'海北藏族自治州',NULL,NULL),(357,30,'海东',NULL,'101150201'),(358,30,'海南藏族自治州',NULL,NULL),(359,30,'海西蒙古族藏族自治州',NULL,NULL),(360,30,'黄南藏族自治州',NULL,NULL),(361,30,'玉树藏族自治州',NULL,NULL),(362,31,'银川',NULL,'101170101'),(363,31,'固原',NULL,'101170401'),(364,31,'石嘴山',NULL,'101170201'),(365,31,'吴忠',NULL,'101170301'),(366,32,'乌鲁木齐',NULL,'101130101'),(367,32,'吐鲁番',NULL,'101130501'),(368,32,'阿克苏',NULL,'101130801'),(369,32,'阿拉尔',NULL,NULL),(370,32,'巴音郭楞蒙古自治州',NULL,NULL),(371,32,'博尔塔拉蒙古自治州',NULL,NULL),(372,32,'昌吉回族自治州',NULL,NULL),(373,32,'哈密',NULL,'101131201'),(374,32,'和田',NULL,'101131301'),(375,32,'喀什',NULL,'101130901'),(376,32,'克拉玛依',NULL,'101130201'),(377,32,'克孜勒苏柯尔克孜自治州',NULL,NULL),(378,32,'石河子',NULL,'101130301'),(379,32,'图木舒克',NULL,NULL),(380,32,'五家渠',NULL,NULL),(381,32,'伊犁哈萨克自治州',NULL,NULL),(382,33,'香港',NULL,'101320101'),(383,34,'澳门',NULL,'101330101');
/*!40000 ALTER TABLE `boc_province_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_sessions_adminer`
--

DROP TABLE IF EXISTS `boc_sessions_adminer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_sessions_adminer` (
  `session_id` varchar(40) NOT NULL DEFAULT '0',
  `ip_address` varchar(45) NOT NULL DEFAULT '0',
  `user_agent` varchar(120) NOT NULL,
  `last_activity` int(10) unsigned NOT NULL DEFAULT '0',
  `user_data` text NOT NULL,
  PRIMARY KEY (`session_id`),
  KEY `last_activity_idx` (`last_activity`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='会话保存';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_sessions_adminer`
--

LOCK TABLES `boc_sessions_adminer` WRITE;
/*!40000 ALTER TABLE `boc_sessions_adminer` DISABLE KEYS */;
INSERT INTO `boc_sessions_adminer` VALUES ('8dc04c3fa0ec0b4c6837f93a9e2702aa','127.0.0.1','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36',1397099170,'a:6:{s:9:\"user_data\";s:0:\"\";s:3:\"mid\";s:1:\"1\";s:5:\"uname\";s:9:\"superuser\";s:8:\"nickname\";s:12:\"超级用户\";s:8:\"login_ip\";s:9:\"127.0.0.1\";s:3:\"gid\";s:1:\"1\";}');
/*!40000 ALTER TABLE `boc_sessions_adminer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_sessions_site`
--

DROP TABLE IF EXISTS `boc_sessions_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_sessions_site` (
  `session_id` varchar(40) NOT NULL DEFAULT '0',
  `ip_address` varchar(45) NOT NULL DEFAULT '0',
  `user_agent` varchar(120) NOT NULL,
  `last_activity` int(10) unsigned NOT NULL DEFAULT '0',
  `user_data` text NOT NULL,
  PRIMARY KEY (`session_id`),
  KEY `last_activity_idx` (`last_activity`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='会话保存';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_sessions_site`
--

LOCK TABLES `boc_sessions_site` WRITE;
/*!40000 ALTER TABLE `boc_sessions_site` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_sessions_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_upload`
--

DROP TABLE IF EXISTS `boc_upload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_upload` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '文件名',
  `size` int(11) DEFAULT NULL COMMENT '大小',
  `type` varchar(255) DEFAULT NULL COMMENT '类型',
  `url` varchar(100) DEFAULT NULL COMMENT '地址',
  `thumb` varchar(100) DEFAULT NULL COMMENT '缩略图',
  `deleteUrl` varchar(150) DEFAULT NULL COMMENT '删除',
  `alt` varbinary(30) DEFAULT NULL COMMENT '提示',
  `title` varbinary(100) DEFAULT NULL COMMENT '标题',
  `text` tinytext COMMENT '简介内容',
  `timeline` int(11) DEFAULT NULL COMMENT '时间线',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='文件上传';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_upload`
--

LOCK TABLES `boc_upload` WRITE;
/*!40000 ALTER TABLE `boc_upload` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_upload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_video`
--

DROP TABLE IF EXISTS `boc_video`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(4) DEFAULT NULL COMMENT '栏目id',
  `sort_id` int(11) DEFAULT '0' COMMENT '排序',
  `audit` int(1) DEFAULT '0' COMMENT '0/1审核',
  `flag` int(1) NOT NULL DEFAULT '0' COMMENT '0:1推荐',
  `title` tinytext COMMENT '标题',
  `title_seo` tinytext COMMENT 'seo标题',
  `intro` varchar(500) DEFAULT NULL COMMENT '简介',
  `tags` tinytext COMMENT '标签',
  `content` text COMMENT '内容',
  `url` tinytext COMMENT '外链',
  `video` tinytext COMMENT '视频地址',
  `photo` tinytext COMMENT '封面',
  `thumb` tinytext COMMENT '封面缩略图',
  `show` int(1) DEFAULT '1' COMMENT '是否显示',
  `timeline` int(11) DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='视频';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_video`
--

LOCK TABLES `boc_video` WRITE;
/*!40000 ALTER TABLE `boc_video` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_video` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_recruit`
--

DROP TABLE IF EXISTS `boc_recruit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_recruit` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一编号',
  `sort_id` int(11) DEFAULT '1' COMMENT '排序编号',
  `cid` int(11) DEFAULT NULL COMMENT '类型',
  `ccid` int(11) DEFAULT '0',
  `title` tinytext NOT NULL COMMENT '标题',
  `title_seo` tinytext,
  `intro` tinytext COMMENT '简介',
  `tags` tinytext,
  `content` mediumtext COMMENT '内容',
  `timeline` int(11) DEFAULT NULL COMMENT '发布/修改时间',
  `expiretime` int(11) DEFAULT NULL COMMENT '公告过期时间',
  `click` int(11) DEFAULT '0' COMMENT '浏览次数',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '显隐状态',
  `flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '推荐到分类门户的页面显示',
  `audit` tinyint(1) NOT NULL DEFAULT '0' COMMENT '突显状态/颜色',
  `show` tinyint(1) NOT NULL DEFAULT '1',
  `photo` varchar(255) DEFAULT NULL COMMENT '相关图片',
  `thumb` varchar(255) DEFAULT NULL COMMENT '图片缩略图',
  `attachment` varchar(255) DEFAULT NULL COMMENT '相关文件',
  `country` varchar(50) DEFAULT NULL,
  `province` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `county` varchar(50) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `require` varchar(50) DEFAULT NULL COMMENT '职称要求',
  `amount` int(11) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `gender` tinyint(1) NOT NULL DEFAULT '0',
  `age` smallint(6) DEFAULT NULL,
  `age_max` smallint(6) DEFAULT NULL,
  `edu` varchar(50) DEFAULT NULL,
  `major` varchar(50) DEFAULT NULL,
  `experience` varchar(50) DEFAULT NULL,
  `requirement` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='人才招聘';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_recruit`
--

LOCK TABLES `boc_recruit` WRITE;
/*!40000 ALTER TABLE `boc_recruit` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_recruit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boc_recruit_apply`
--

DROP TABLE IF EXISTS `boc_recruit_apply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_recruit_apply` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一编号',
  `sort_id` int(11) DEFAULT '1' COMMENT '排序编号',
  `type_id` int(11) DEFAULT NULL COMMENT '类型',
  `recruit_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL COMMENT '应聘标题',
  `intro` varchar(1000) DEFAULT NULL COMMENT '简介',
  `content` mediumtext COMMENT '内容',
  `answer` mediumtext,
  `timeline_answer` int(11) DEFAULT NULL,
  `timeline` int(11) DEFAULT NULL COMMENT '发布/修改时间',
  `expire` int(11) DEFAULT NULL COMMENT '公告过期时间',
  `solve` int(1) DEFAULT '0',
  `click` int(11) DEFAULT '0' COMMENT '浏览次数',
  `show` tinyint(4) DEFAULT '1' COMMENT '显隐状态',
  `recommend` tinyint(4) DEFAULT '0' COMMENT '推荐到分类门户的页面显示',
  `color` tinyint(4) DEFAULT '0' COMMENT '突显状态/颜色',
  `audit` tinyint(1) DEFAULT '0' COMMENT '审核状态',
  `photo` varchar(255) DEFAULT NULL COMMENT '相关图片',
  `thumb` varchar(255) DEFAULT NULL COMMENT '图片缩略图',
  `file` varchar(255) DEFAULT NULL COMMENT '相关文件',
  `ip` varchar(100) DEFAULT NULL,
  `ex1` varchar(255) DEFAULT '' COMMENT '其他标签（预留）',
  `ex2` varchar(255) DEFAULT '',
  `ex3` varchar(255) DEFAULT '',
  `ex4` varchar(255) DEFAULT '',
  `x` varchar(255) DEFAULT '',
  `y` varchar(255) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `province` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `county` varchar(50) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL COMMENT '部门',
  `name` varchar(50) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `marriage` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `tel` varchar(100) DEFAULT NULL,
  `mobile` varchar(100) DEFAULT NULL,
  `qq` varchar(100) DEFAULT NULL,
  `msn` varchar(100) DEFAULT NULL,
  `wangwang` varchar(100) DEFAULT NULL,
  `nation` varchar(50) DEFAULT NULL COMMENT '民族',
  `birthday` varchar(20) DEFAULT NULL,
  `politic` varchar(50) DEFAULT NULL COMMENT '政治面貌',
  `birthplace` varchar(50) DEFAULT NULL COMMENT '籍贯',
  `school` varchar(100) DEFAULT NULL,
  `major` varchar(50) DEFAULT NULL COMMENT '专业',
  `graduation` varchar(20) DEFAULT NULL COMMENT '毕业时间',
  `language` varchar(50) DEFAULT NULL COMMENT '外语水平',
  `position` varchar(100) DEFAULT NULL COMMENT '应聘职位',
  `age` smallint(6) DEFAULT NULL,
  `edu` varchar(50) DEFAULT NULL,
  `experience` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='在线应聘';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boc_recruit`
--

LOCK TABLES `boc_recruit_apply` WRITE;
/*!40000 ALTER TABLE `boc_recruit_apply` DISABLE KEYS */;
/*!40000 ALTER TABLE `boc_recruit_apply` ENABLE KEYS */;
UNLOCK TABLES;



DROP TABLE IF EXISTS `boc_coltypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_coltypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '标识',
  `sort_id` int(11) NOT NULL COMMENT '排序id',
  `fid` int(11) NOT NULL COMMENT '父类型',
  `depth` int(3) NOT NULL COMMENT '深度',
  `cid` int(4) NOT NULL DEFAULT '0' COMMENT '栏目ID',
  `name` varchar(30) NOT NULL DEFAULT 'ctype' COMMENT '表单名称，分类标志，单个栏目多个类型时',
  `title` varchar(30) NOT NULL COMMENT '标题类型',
  `identify` varchar(30) NOT NULL COMMENT '标记',
  `photo` varchar(30) NOT NULL COMMENT '图片',
  `thumb` varchar(200) NOT NULL COMMENT '缩略图',
  `show` int(1) NOT NULL DEFAULT '1' COMMENT '显示',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `boc_tags`
--

DROP TABLE IF EXISTS `boc_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(30) NOT NULL COMMENT '标签',
  `en` varchar(60) DEFAULT NULL COMMENT '拼音|英语',
  `len` int(3) DEFAULT '0' COMMENT '长度',
  `count` int(11) DEFAULT '0' COMMENT '计数',
  `type` int(1) DEFAULT '0' COMMENT '分类,0:tags,1:title,2:intro,3:content',
  PRIMARY KEY (`id`),
  KEY `record_index` (`id`,`tag`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='标签表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `boc_tags_list`
--

DROP TABLE IF EXISTS `boc_tags_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `boc_tags_list` (
  `tid` int(11) NOT NULL DEFAULT '0' COMMENT 'tag id',
  `cid` int(11) NOT NULL DEFAULT '0' COMMENT 'col id',
  `aid` int(11) NOT NULL DEFAULT '0' COMMENT 'col''s aritcle id',
  `type` int(1) NOT NULL DEFAULT '0' COMMENT '分类,0:tags,1:title,2:intro,3:content',
  `timeline` int(11) NOT NULL COMMENT '时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='标签使用表';
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-04-10 13:49:00
