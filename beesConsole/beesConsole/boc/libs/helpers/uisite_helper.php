<?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');

// TODO：舍弃 查看 data_helper one_page
// 获取单页信息
if(!function_exists('tag_single'))
{
	function tag_single($cid,$column='content',$strcut=-1)
	{
		static $a=array();
		$cid=intval($cid);
		if(is_int($column)){
			$strcut=$column;
			$column='content';
		}
		if(!isset($a[$cid])){
			$CI=&get_instance();
			$CI->load->database();
			$a[$cid]=$CI->db->get_where('page',array('cid'=>$cid));
			if($a[$cid]->num_rows()<1){
				$a[$cid]=array();
			}else{
				$a[$cid]=$a[$cid]->row_array();
			}
		}
		if(isset($a[$cid][$column])){
			if($strcut>-1){
				return strcut(strip_tags(nl2br($a[$cid][$column])),$strcut);
			}
			return $a[$cid][$column];
		}
		return '';
	}
}

// TODO：舍弃 查看 data_helper one_upload/list_upload
// 获取图片
if(!function_exists('tag_photo'))
{
	function tag_photo($id,$column='url')
	{
		static $a=array();
		$id=intval($id);
		if(!isset($a[$id])){
			$CI=&get_instance();
			$CI->load->database();
			$a[$id]=$CI->db->get_where('upload',array('id'=>$id));
			if($a[$id]->num_rows()<1){
				$a[$id]=array();
			}else{
				$a[$id]=$a[$id]->row_array();
			}
		}
		if(isset($a[$id][$column])){
			return $a[$id][$column];
		}
		return '';
	}
}

// TODO：舍弃 查看 data_helper ctype相关
// 获取分类
if(!function_exists('tag_types'))
{
	function tag_types($id,$cid,$column='title')
	{
		static $a=array();
		$id=intval($id);
		if(!isset($a[$id])){
			$CI=&get_instance();
			$CI->load->database();
			$a[$id]=$CI->db->get_where('coltypes',array('id'=>$id,'cid'=>$cid));
			if($a[$id]->num_rows()<1){
				$a[$id]=array();
			}else{
				$a[$id]=$a[$id]->row_array();
			}
		}
		if(isset($a[$id][$column])){
			return $a[$id][$column];
		}
		return '';
	}
}

// TODO：舍弃 查看 data_helper 栏目相关
// 获取栏目名称
if(!function_exists('tag_columns'))
{
	function tag_columns($id,$column='title')
	{
		static $a=array();
		$id=intval($id);
		if(!isset($a[$id])){
			$CI=&get_instance();
			$CI->load->database();
			$a[$id]=$CI->db->get_where('columns',array('id'=>$id));
			if($a[$id]->num_rows()<1){
				$a[$id]=array();
			}else{
				$a[$id]=$a[$id]->row_array();
			}
		}
		if(isset($a[$id][$column])){
			return $a[$id][$column];
		}
		return '';
	}
}

function htmlchars($string){
	$string = preg_replace("/\s(?=\s)/", '', trim(strip_tags($string)));
	return str_replace("&nbsp;","",$string);
}

function myEscape($str){
	preg_match_all("/[\xc2-\xdf][\x80-\xbf]+|[\xe0-\xef][\x80-\xbf]{2}|[\xf0-\xff][\x80-\xbf]{3}|[\x01-\x7f]+/e",$str,$r);
	$str=$r[0];
	$l=count($str);
	for($i=0;$i<$l;$i++){
		$value=ord($str[$i][0]);
		if($value<223){
			$str[$i]=rawurlencode(utf8_decode($str[$i]));
			//先将utf8编码转换为ISO-8859-1编码的单字节字符，urlencode单字节字符.
			//utf8_decode()的作用相当于iconv("UTF-8","CP1252",$v)。
		//}else{
		//	$str[$i]="%u".strtoupper(bin2hex(iconv("UTF-8","UCS-2",$str[$i])));
		//}

		}else if(DIRECTORY_SEPARATOR!='/'){
        	//red hat和一些linux服务器要注释掉下面一行，否则js getcookiex乱码
        	$str[$i] = "%u".strtoupper(bin2hex(iconv("UTF-8","UCS-2",$str[$i])));
        }
	}
	return join("",$str);
}

function myUnescape($str){
	$ret='';
	$len=strlen($str);
	for($i=0;$i<$len;$i++){
		if($str[$i]=='%'&&$str[$i+1]=='u'){
			$val=hexdec(substr($str,$i+2,4));
			if($val<0x7f)$ret.=chr($val);
			elseif($val<0x800)$ret.=chr(0xc0|($val>>6)).chr(0x80|($val&0x3f));
			else $ret.=chr(0xe0|($val>>12)).chr(0x80|(($val>>6)&0x3f)).chr(0x80|($val&0x3f));
			$i+=5;
		}elseif($str[$i]=='%'){
			$ret.=urldecode(substr($str,$i,3));
			$i+=2;
		}else $ret.=$str[$i];
	}
	return $ret;
}

//符合 uri segment 标准的64编码
//在 javascript 端请用 $.base64.decodex() 解码
function myBase64Encode($s,$in_charset='UTF-8'){
	if(strtoupper($in_charset)!='UTF-8')
		$s=iconv($in_charset,'UTF-8',$s);
	return str_replace('/','|',base64_encode($s));
}

//符合 uri segment 标准的64解码
//在 javascript 端请用 $.base64.encodex() 编码
function myBase64Decode($s, $out_charset='UTF-8'){
	$s=base64_decode(str_replace('|','/',$s));
	if(strtoupper($out_charset)!='UTF-8')
		$s=iconv('UTF-8',$out_charset,$s);
	return $s;
}

//文件下载
function download_files($file_addr,$file_name){
	if (file_exists($file_addr)){
		$filesize = filesize($file_addr);
		header("Expires: Thu, 12 Apr 2012 14:00:00 GMT");
		header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
		header("Cache-Control: no-store, no-cache, must-revalidate");
		header("Cache-Control: post-check=0, pre-check=0", false);
		header("Pragma: ");
		header("Cache-control: private");
		header("Content-Length: " . $filesize);

		if(strpos($_SERVER['HTTP_USER_AGENT'], 'MSIE') !== FALSE){
			header("Content-Disposition: attachment;filename=".urlencode($file_name));
		}else{
			header("Content-Disposition: attachment;filename=".$file_name);
		}

		if (preg_match('#Opera(/| )([0-9].[0-9]{1,2})#', getenv('HTTP_USER_AGENT')) or preg_match('#MSIE ([0-9].[0-9]{1,2})#', getenv('HTTP_USER_AGENT'))) {
		  header("Content-Type: application/octetstream; charset=utf-8");
		} else {
		  header("Content-Type: application/octet-stream; charset=utf-8");
		}
		readfile($file_addr);
	}else{
		return 'err';
	}
}

//下载大文件
function download_bigfiles($file_addr,$file_name){
	if (file_exists($file_addr)){
		ob_start();
		ini_set('memory_limit','1200M');
		set_time_limit(0);
		$filesize = filesize($file_addr);
		header("Expires: Thu, 12 Apr 2012 14:00:00 GMT");
		header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
		header("Cache-Control: no-store, no-cache, must-revalidate");
		header("Cache-Control: post-check=0, pre-check=0", false);
		header("Pragma: no-cache");
		header('Content-Description: File Transfer');
		header("Cache-control: private");
		header("Content-Length: " . $filesize);

		if(strpos($_SERVER['HTTP_USER_AGENT'], 'MSIE') !== FALSE){
			header("Content-Disposition: attachment;filename=".urlencode($file_name));
		}else{
			header("Content-Disposition: attachment;filename=".$file_name);
		}

		if (preg_match('#Opera(/| )([0-9].[0-9]{1,2})#', getenv('HTTP_USER_AGENT')) or preg_match('#MSIE ([0-9].[0-9]{1,2})#', getenv('HTTP_USER_AGENT'))) {
		  header("Content-Type: application/octetstream; charset=utf-8");
		} else {
		  header("Content-Type: application/octet-stream; charset=utf-8");
		}
		ob_clean();
		flush();
		readfile($file_addr);
		exit;
	}else{
		return 'err';
	}
}

function goto_message($message,$uri=-1,$toSiteUrl=true){
	$message=addslashes($message);
	if(is_int($uri))$uri='history.go('.$uri.');';
	else if($toSiteUrl)$uri='location.href="'.site_url($uri).'";';
	header("Content-type:text/html;Charset=utf-8");
	exit('<script>alert("'.$message.'");'.$uri.'</script>');
}

/**
 * @desc  通过photo取得对应图片的数组 包含全路径(图片id,用于upload做查询)
 */
function separate_pictures($photo,$whetherNeed=true){
	if (empty($photo)) {
		$img='';
	}else {
		$img=array();
		if(strstr($photo,',')){
			$img_id=explode(",",$photo);
			foreach ($img_id as $k=>$v){
				$img_one=tag_photo($v);
				if (is_file(UPLOAD_PATH.$img_one)) {
					if ($whetherNeed==true) {
						$img[$k]['url']=UPLOAD_URL.$img_one;
						$img[$k]['id']=$v;
					}else{
						$img[]=UPLOAD_URL.$img_one;
					}
				}
			}
		}else {
			$img_one=tag_photo($photo);
			if (is_file(UPLOAD_PATH.$img_one)) {
				if ($whetherNeed==true) {
					$img['0']['url']=UPLOAD_URL.$img_one;
					$img['0']['id']=$photo;
				}else{
					$img['0']=UPLOAD_URL.$img_one;
				}
			}
		}
	}
	return $img;
}

/**
 * @desc  get_one方法 同时返回上一条和下一条
 * @param array $where where条件 数组
 * @param string $fields 要查询的字段
 * @param string $additional_where 附加的查询上下条的条件  如 ctype,cid
 * @param string $table 表名  默认新闻表
 */
function get_one_hq($where, $fields = "*",$additional_where=false,$table="article")
{
	$CI = &get_instance ();
	$CI->db->select($fields)->from($table);
	if(!is_numeric($where))
	{
		$CI->db->where($where);
	} else {
		$CI->db->where('id',$where);
	}
	$query = $CI->db->get();
	$row = $query->row_array();

	if($row)
	{
		$wherePerv=array('cid'=>$row['cid'],'audit'=>1,'sort_id >'=>$row['sort_id'],'status'=>1);
		if ($additional_where!=false) {
			if(strstr($additional_where,',')){
				$additionalArray=explode(",",$additional_where);
				foreach ($additionalArray as $key => $value) {
					$wherePerv=array_merge($wherePerv,array($value=>$row[$value]));
				}
			}else{
				$wherePerv=array_merge($wherePerv,array($additional_where=>$row[$additional_where]));
			}
		}
		$perv = $CI->db->select('id,title')
		->from($table)
		->where($wherePerv)
		->order_by('sort_id','asc')
		->limit(1)->get()->row_array();

		if($perv)
		{
			$row['prev_id'] = $perv['id'];
			$row['prev_title'] = $perv['title'];
		}
		$whereNext=array('cid'=>$row['cid'],'audit'=>1,'sort_id <'=>$row['sort_id'],'status'=>1);
		if ($additional_where!=false) {
			if(strstr($additional_where,',')){
				$additionalArray=explode(",",$additional_where);
				foreach ($additionalArray as $key => $value) {
					$whereNext=array_merge($whereNext,array($value=>$row[$value]));
				}
			}else{
				$whereNext=array_merge($whereNext,array($additional_where=>$row[$additional_where]));
			}
		}
		$next = $CI->db->select('id,title')
		->from($table)
		->where($whereNext)
		->order_by('sort_id','desc')
		->limit(1)->get()->row_array();

		if($next)
		{
			$row['next_id'] = $next['id'];
			$row['next_title'] = $next['title'];
		}
	}

	return $row;
}
/**
 * @desc  对数据进行trim处理
 * @param string and array     $data  需要处理的数据  字符串或者数组
 *
 */
function doTrim($data)
{
	if (is_array($data)) {
		foreach ($data as $k => $val) {
			$data[$k] = trim($val);
		}
	} else {
		$data = trim($data);
	}
	return $data;
}
/**
 * @desc  CI跳转简写
 * @param string $url 跳转url段  默认为空  跳转到首页
 *
 */
function H($url=''){
	header("Location:". site_url($url));
	exit;
}
/**
 * @desc 二维数字排序
 * @param array $arrUsers 需要排序的数组
 * @param string $sort 如何排序  默认 'SORT_ASC'
 * @param string $field 排序的关键字段  默认 false   但是false会返回false   例: 'id'
 */
function TwoDimensionalArraySort($arrUsers,$sort='SORT_ASC',$field=false){
	if ($field==false) {
		return false;
	}
	$sort = array(
			'direction' => $sort, //排序顺序标志 SORT_DESC 降序；SORT_ASC 升序
			'field'     => $field,       //排序字段
	);
	$arrSort = array();
	foreach($arrUsers AS $uniqid => $row){
		foreach($row AS $key=>$value){
			$arrSort[$key][$uniqid] = $value;
		}
	}
	if($sort['direction']){
		array_multisort($arrSort[$sort['field']], constant($sort['direction']), $arrUsers);
	}

	return $arrUsers;
}
/**
 * @desc 根据两点间的经纬度计算距离
 * @param float $lat 纬度值
 * @param float $lng 经度值
 */
function getDistance($lat1, $lng1, $lat2, $lng2)
{
	$earthRadius = 6367000;

	$lat1 = ($lat1 * pi() ) / 180;
	$lng1 = ($lng1 * pi() ) / 180;

	$lat2 = ($lat2 * pi() ) / 180;
	$lng2 = ($lng2 * pi() ) / 180;

	$calcLongitude = $lng2 - $lng1;
	$calcLatitude = $lat2 - $lat1;
	$stepOne = pow(sin($calcLatitude / 2), 2) + cos($lat1) * cos($lat2) * pow(sin($calcLongitude / 2), 2);
	$stepTwo = 2 * asin(min(1, sqrt($stepOne)));
	$calculatedDistance = $earthRadius * $stepTwo;

	return round($calculatedDistance);
}
/**
 * @desc 转义
 * @param string $string 需要转换的字符串
 *
 */
function dhtmlspecialchars($string, $flags = null) {
	if(is_array($string)) {
		foreach($string as $key => $val) {
			$string[$key] = dhtmlspecialchars($val, $flags);
		}
	} else {
		if($flags === null) {
			$string = str_replace(array('&', '"', '<', '>'), array('&amp;', '&quot;', '&lt;', '&gt;'), $string);
			if(strpos($string, '&amp;#') !== false) {
				//过滤掉类似&#x5FD7的16进制的html字符
				$string = preg_replace('/&amp;((#(\d{3,5}|x[a-fA-F0-9]{4}));)/', '&\\1', $string);
			}
		} else {
			if(PHP_VERSION < '5.4.0') {
				$string = htmlspecialchars($string, $flags);
			} else {
				if(strtolower(CHARSET) == 'utf-8') {
					$charset = 'UTF-8';
				} else {
					$charset = 'ISO-8859-1';
				}
				$string = htmlspecialchars($string, $flags, $charset);
			}
		}
	}
	return $string;
}
/**
 * @desc 数字转英文月份
 * @param int  $num  需要转换的数字     1 - 12
 */
function number2EnglishMonth($num = '') {
	if ($num < 1 || $num > 13 || $num == '' || !is_numeric($num)) {
		return date ( 'M' );
	}
	switch ($num) {
		case 1 :
			return "January";
			break;
		case 2 :
			return "February";
			break;
		case 3 :
			return "March";
			break;
		case 4 :
			return "April";
			break;
		case 5 :
			return "May";
			break;
		case 6 :
			return "June";
			break;
		case 7 :
			return "July";
			break;
		case 8 :
			return "August";
			break;
		case 9 :
			return "September";
			break;
		case 10 :
			return "October";
			break;
		case 11 :
			return "November";
			break;
		case 12 :
			return "December";
			break;
		default :
			return date ( 'M' );
	}
}
function checkJurisdiction(){
    $CI=&get_instance();
    $adminGid = $CI->session->userdata('gid');
    // 检测是否有权限，提示添加,未添加到组的权限
    if ($adminGid != 1) {
        $vdata = array('status'=>0,'msg'=>'您并没有权限访问此页面！如需权限，请联系管理员！');
        if ($CI->input->is_ajax_request()) {
            // 此处不用 output 因为不会去执行控制器方法
            header('HTTP/1.1 500 Internal Server Error');
            // 使用 ajax error接收
            json_echo($vdata);
            exit();
            return false;
        }else{
            $str =$CI->load->view('msg',$vdata);
        }
    }
}


