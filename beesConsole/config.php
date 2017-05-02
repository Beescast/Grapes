<?php


# Tag
define('BOCTAG','0.9');

# 数据库
// define('DB_TYPE'   , 'mysqli');
// define('DB_HOST'   , '127.0.0.1');
// define('DB_USER'   , 'root');
// define('DB_PASS'   , 'root');
// define('DB_NAME'   , 'beesconsole');
// define('DB_PREFIX' , 'bees_');

define('DB_TYPE'   , 'mysqli');
define('DB_HOST'   , '192.168.3.56');
define('DB_USER'   , 'superbird');
define('DB_PASS'   , 'Bees@0831');
define('DB_NAME'   , 'beesconsole');
define('DB_PREFIX' , 'bees_');

# 全局URL路径
// 主域名 保留最后的 /
define('GLOBAL_URL'  , 'http://'.$_SERVER['HTTP_HOST'].'/beesConsole/out/');
//define('GLOBAL_URL'  , 'http://localhost:9003/');
// 提供给后台做链接用的
define('STATIC_URL'  , GLOBAL_URL.'static/');
define('UPLOAD_URL'  , GLOBAL_URL.'upload/');
// 对应APP
define('SITE_URL'  ,   GLOBAL_URL.'index.php/');
define('ADMINER_URL' , GLOBAL_URL.'houtai/');
define('MOBILE_URL'  , GLOBAL_URL.'mobile/');

// define('GLOBAL_URL'  , 'http://localhost:9000/');
// define('STATIC_URL'  , 'http://localhost:9001/');
// define('UPLOAD_URL'  , 'http://localhost:9002/');
// define('ADMINER_URL' , 'http://localhost:9003/');
// define('MOBILE_URL'  , 'http://localhost:9004/');

// // 快捷提供给JS
define('IMG_URL'     , STATIC_URL.'img/');

# 引用绝对路径PATH定义
define('ROOT'        , __DIR__.'/');
define('LIBS_PATH'   , ROOT.'boc/libs/');
define('CI_PATH'     , ROOT.'boc/libs/ci/');
define('STATIC_PATH' , ROOT.'out/static/');
define('UPLOAD_PATH' , ROOT.'out/upload/');
define('SITE_PATH'   , ROOT.'boc/site');
define('ADMIN_PATH'  , ROOT.'boc/bocadmin');

# 可忽略 当css|js改变时替换本地缓存,将false 替换为 'v[1,2...]'
define('STATIC_V','v3');

# 密钥设置;设置多个 用于 md5/sha1(hmac.value.time) 外部数据输入输出
# 提供给 app 的config 的 encryption_key
define('HMACPWD','SA1S2D3F4G5H6J7K8L9'); // PASSWD and cookie
define('HMAC','SA1S2D3F4G5H6J7K8L8');    // 提供第三方API验证使用

/*
 * 开发模式
 * 配置项目运行的环境，该配置会影响错误报告的显示和配置文件的读取。
 * development
 * testing
 * production
 * 使用 error_reporting();
 */
define('ENVIRONMENT', 'development');
// 有些服务器不支持调试，需要开启错误调试
// error_reporting(E_ALL);
// ini_set("display_errors", 1);
// ini_set("error_reporting", 1);

// PHP 5 尝试加载未定义的类
// 挂载本地库 其他 core Controller
// 使用第三方报错工具可能会出现未加载的现象出现使
 function BocLoader($class)
 {
 	if(strpos($class, 'CI_') !== 0)
 	{
 		if (file_exists(APPPATH . 'core/'. $class . EXT)) {
 			@include_once( APPPATH . 'core/'. $class . EXT );
 		}elseif(file_exists(LIBS_PATH . 'core/'. $class . EXT)) {
 			@include_once( LIBS_PATH . 'core/'. $class . EXT );
 		}
 	}
 }
//注册自动加载,解决与其他自动加载第三方插件冲突
spl_autoload_register('BocLoader');

function v($str){
	echo "<pre>";
	print_r($str);
	echo "</pre>" ;
}
//参数1：访问的URL，参数2：post数据(不填则为GET)，参数3：提交的$cookies,参数4：是否返回$cookies
 function curl_request($url,$post='',$cookie='', $returnCookie=0){
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)');
        curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
        curl_setopt($curl, CURLOPT_REFERER, "http://XXX");
        if($post) {
            curl_setopt($curl, CURLOPT_POST, 1);
            curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
        }
        if($cookie) {
            curl_setopt($curl, CURLOPT_COOKIE, $cookie);
        }
        curl_setopt($curl, CURLOPT_HEADER, $returnCookie);
        curl_setopt($curl, CURLOPT_TIMEOUT, 10);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
        $data = curl_exec($curl);
        if (curl_errno($curl)) {
            return curl_error($curl);
        }
        curl_close($curl);
        if($returnCookie){
            list($header, $body) = explode("\r\n\r\n", $data, 2);
            preg_match_all("/Set\-Cookie:([^;]*);/", $header, $matches);
            $info['cookie']  = substr($matches[1][0], 1);
            $info['content'] = $body;
            return $info;
        }else{
            return $data;
        }
}
//添加房间
function addroom_url($rid){
	return 'http://192.168.3.108:5000/tornado/addroom?rid='.$rid;
}
//删除文件
function delroom_url($rid){
	return 'http://192.168.3.108:5000/tornado/delroom?rid='.$rid;
}
//发送消息
function sendmsg_url($rid,$msg,$repeat='1'){
	return 'http://192.168.3.108:5000/tornado/testmsg?rid='.$rid.'&msg='.$msg.'&repeat='.$repeat;
}
//设置房间参数
function setroom_url($rid,$num,$interval,$pause,$freq){
	return 'http://192.168.3.108:5000/tornado/setroom?rid='.$rid.'&num='.$num.'&interval='.$interval.'&pause='.$pause.'&freq='.$freq;
}
//查看房间参数
function roominfo_url($rid){
    return 'http://192.168.3.108:5000/tornado/roominfo?rid='.$rid;
}
//查看房间参数
function roominfo_All(){
    return 'http://192.168.3.108:5000/tornado/roominfo';
}