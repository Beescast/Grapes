<?php 
$status_array=array(
        '2'=>array('id'=>2,'title'=>'全部'),
		'0'=>array('id'=>0,'title'=>'没讲话'),
		'1'=>array('id'=>1,'title'=>'讲话')
		
);

?>
<br><p></p>
<!-- 检索 -->
<form class="form-inline" action="<?php echo site_urlc($this->class.'/search/'.$this->cid); ?>" method="GET">
<input type="text" name="title" width="50px" value="<?php echo isset($_GET['title'])?$_GET['title']:''?>" placeholder="房间号"/>
<?php 
if (isset($_GET['audit'])) {
	echo ui_btn_select('audit',set_value("audit",$_GET['audit']),$status_array);
}else{
	echo ui_btn_select('audit',2,$status_array);
}

?>
<input class="btn" type="submit" value="检索">
</form>

<!-- 检索 -->
<script type="text/javascript">
require(['adminer/js/ui','adminer/js/media','bootstrap-datetimepicker.zh'],function(ui,media){
    // timepick
    $('.timepicker').datetimepicker({'language':'zh-CN','format':'yyyy/mm/dd hh:ii:ss','todayHighlight':true});
});
</script>

