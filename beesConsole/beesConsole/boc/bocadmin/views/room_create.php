
<!-- 
<?php if(in_array($_GET['c'],array(0))){?>
<?php }?>
-->
<div class="btn-group">
	<a href="<?php echo site_urlc('room/index')?>" class='btn'> <i
		class="fa fa-arrow-left"></i> <?php echo lang('back_list')?></a>
</div>

<?php include_once 'inc_form_errors.php'; ?>

<div class="boxed">
	<h3>
		<i class="fa fa-plus"></i> <span
			class="badge badge-success pull-right"><?php echo $title; ?></span> <?php echo lang('add') ?></h3>
	<?php echo form_open(current_urlc(),array("class"=>"form-horizontal","id"=>"frm-create")); ?>

		<div class="boxed-inner seamless">

		<!-- 弹出 -->
		<div id="seo-modal" class="modal hide fade">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"
					aria-hidden="true">
					<i class="fa fa-times"></i>
				</button>
				<h3>
					<i class="fa fa-info-circle"></i>帐号类型
				</h3>
			</div>
			<div class="modal-body seamless" id="types_div">

				<!--                  <div class="control-group">
						<label for="title_seo" class="control-label">1</label>
						<div class="controls">
							<input type="number" id="1" name="1" value="" required=1>
							<span class="help-inline"></span>
						</div>
					</div>  
-->
			</div>
			<div class="modal-footer">
				<a href="#" data-dismiss="modal" aria-hidden="true" class="btn">Close</a>
			</div>
		</div>

		<div class="control-group">
			<label class="control-label" for="title">房间号</label>
			<div class="controls">
				<input type="number" id="title" name="title"
					value="<?php echo set_value("title") ?>" required=1
					onchange="changeACCDiv();">
				<!--  -->

			</div>
		</div>

		<div class="control-group">
			<label for="title" class="control-label">时间</label>
			<div class="controls">
				<div class="input-append date timepicker">
					<input type="text"
						value="<?php echo date("Y-m-d H:i:s",set_value('timeline',now())); ?>"
						id="timeline" name="timeline"
						data-date-format="yyyy-mm-dd hh:ii:ss"> <span class="add-on"><i
						class="icon-th"></i></span>
				</div>
			</div>
		</div>
		<!-- 			<div class="control-group">
				<label for="title" class="control-label">帐号数量</label>
				<div class="controls">
					<input type="number" name="AccountNumber" id="AccountNumber" value="<?php echo set_value('AccountNumber'); ?>"   required=1>
					<a href="#seo-modal" role="button" class="btn btn-info" data-toggle="modal" onclick="getTypes();">帐号类型</a>
					<span class="help-inline"></span>
				</div>
			</div>
 -->
		<div class="control-group">
			<label for="title" class="control-label"><?php echo ACC0 ?></label>
			<div class="controls">
				<input type="number" name="ACC0" id="ACC0"
					value="<?php echo set_value('ACC0'); ?>" required=1> <span
					class="help-inline" id="ACC0_span"></span>
			</div>
		</div>
		<div class="control-group">
			<label for="title" class="control-label"><?php echo ACC1 ?></label>
			<div class="controls">
				<input type="number" name="ACC1" id="ACC1"
					value="<?php echo set_value('ACC1'); ?>" required=1> <span
					class="help-inline" id="ACC1_span"></span>
			</div>
		</div>
		<div class="control-group">
			<label for="title" class="control-label"><?php echo ACC2 ?></label>
			<div class="controls">
				<input type="number" name="ACC2" id="ACC2"
					value="<?php echo set_value('ACC2'); ?>" required=1> <span
					class="help-inline" id="ACC2_span"></span>
			</div>
		</div>
		<div class="control-group">
			<label for="title" class="control-label"><?php echo ACC3 ?></label>
			<div class="controls">
				<input type="number" name="ACC3" id="ACC3"
					value="<?php echo set_value('ACC3'); ?>" required=1> <span
					class="help-inline" id="ACC3_span"></span>
			</div>
		</div>

		<div class="control-group">
			<label for="title" class="control-label">帐号登录间隔</label>
			<div class="controls">
				<input type="number" name="LoginInterval" id="LoginInterval"
					value="<?php echo set_value('LoginInterval'); ?>" required=1> <span
					class="help-inline">秒</span>
			</div>
		</div>
		<div class="control-group">
			<label for="title" class="control-label">同帐号说话最大间隔</label>
			<div class="controls">
				<input type="number" name="SpeechInterval" id="SpeechInterval"
					value="<?php echo set_value('SpeechInterval'); ?>" required=1> <span
					class="help-inline">秒</span>
			</div>
		</div>
		<!-- switch demo -->
		<div class="control-group">
			<label class="control-label" for="status">所有帐号状态</label>
			<div class="controls">
					<?php
    $status = array(
        array(
            'title' => "不讲话",
            'value' => '0'
        ),
        array(
            'title' => "讲话",
            'value' => '1'
        )
    );
    echo ui_btn_switch('audit', 1, $status);
    ?>
					<span class="help-inline"></span>
			</div>
		</div>




	</div>

	<div class="boxed-footer">
		<input type="hidden" name="cid" value="<?php echo $this->cid ?>">
			<?php if ($this->ccid): ?>
			<input type="hidden" name="ccid" value="<?php echo $this->ccid ?>">
			<?php endif ?>
			<input type="submit" value=" <?php echo lang('submit'); ?> "
			class='btn btn-primary'> <input type="reset"
			value=' <?php echo lang('reset'); ?> ' class="btn btn-danger">
	</div>
	</form>
</div>

<!-- 多图上传修改
<input class="fileupload" type="file" accept="" multiple="multiple" data-for="photo" data-size="">
data-more="1"
list_upload
-->

<?php include_once 'inc_ui_media.php'; ?>

<script type="text/javascript">
require(['adminer/js/ui','adminer/js/media','bootstrap-datetimepicker.zh'],function(ui,media){
	// timepick
	$('.timepicker').datetimepicker({'language':'zh-CN','format':'yyyy/mm/dd hh:ii:ss','todayHighlight':true});
	// ueditor处理
	
});

function getTypes(){
	var su='<?php echo site_urlc('room/getTypes'); ?>';
	var rid=document.getElementById("title").value;  
	
	$.ajax({
	url: su,
	type: 'POST',
	dataType: 'JSON',
	data: {
		_cfs:$.cookie('_cfc'),
		rid:rid
	}   
	})
	.done(function(data) {
		$("#types_div").empty();
		if(data[0] != "undefined"){
			var text = '最大值:'+data[0];
			$("#ACC0_span").empty();
			$("#ACC0_span").html(text);
		}
		if(data[1] != "undefined"){
			var text = '最大值:'+data[1];
			$("#ACC1_span").empty();
			$("#ACC1_span").html(text);
		}   
		if(data[2] != "undefined"){
			var text = '最大值:'+data[2];
			$("#ACC2_span").empty();
			$("#ACC2_span").html(text);
		}   
		if(data[3] != "undefined"){
			var text = '最大值:'+data[3];
			$("#ACC3_span").empty();
			$("#ACC3_span").html(text);
		}      
	})
	.fail(function(data) {
		alert('获取失败');
	})		   	   
}
function changeACCDiv(){
	getTypes();
}
</script>
