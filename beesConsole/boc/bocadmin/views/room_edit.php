
<!-- 
<?php if(in_array($_GET['c'],array(0))){?>
<?php }?>
-->
<?php //v($_GET);?>
<div class="btn-group"><a href="<?php echo site_urlc('room/index');?>" class="btn"> <i class="fa fa-arrow-left"></i> <?php echo lang('back_list')?> </a></div>

<?php include_once 'inc_form_errors.php'; ?>

<div class="boxed">
	<h3> <i class="fa fa-pencil"></i> 编辑 <span class="badge badge-success pull-right"><?php echo $title; ?></span></h3>
	<?php echo form_open(current_urlc(), array('class' => 'form-horizontal', 'id' => 'frm-edit')); ?>

		<div class="boxed-inner seamless">

			<div class="control-group">
				<label for="title" class="control-label">房间号</label>
				<div class="controls">
					<input type="number" name="title" id="title" value="<?php echo set_value('title',$it['title']); ?>"  readonly="true" required=1>
					
					<span class="help-inline"></span>
				</div>
			</div>
			<div class="control-group">
				<label for="title" class="control-label">时间</label>
				<div class="controls">
					<div class="input-append date timepicker">
						<input type="text" value="<?php echo date("Y/m/d H:i:s",set_value('timeline',$it['timeline'])); ?>" id="timeline" name="timeline">
						<span class="add-on"><i class="icon-th"></i></span>
					</div>
				</div>
			</div>
			<div class="control-group">
				<label for="title" class="control-label">帐号数量</label>
				<div class="controls">
					<input type="number" name="AccountNumber" id="AccountNumber" value="<?php echo set_value('AccountNumber',$it['AccountNumber']); ?>"   required=1>
					
					<span class="help-inline"></span>
				</div>
			</div>
			<div class="control-group">
				<label for="title" class="control-label">帐号登录间隔</label>
				<div class="controls">
					<input type="number" name="LoginInterval" id="LoginInterval" value="<?php echo set_value('LoginInterval',$it['LoginInterval']); ?>"   required=1>
					
					<span class="help-inline">秒</span>
				</div>
			</div>
			<div class="control-group">
				<label for="title" class="control-label">同帐号说话最大间隔</label>
				<div class="controls">
					<input type="number" name="SpeechInterval" id="SpeechInterval" value="<?php echo set_value('SpeechInterval',$it['SpeechInterval']); ?>"   required=1>
					
					<span class="help-inline">秒</span>
				</div>
			</div>
			
			
			
			<!-- <div class="control-group">
				<label for="title" class="control-label">重复弹幕次数</label>
				<div class="controls">
					<input type="number" name="RepeatBarrage" id="RepeatBarrage" value="<?php echo set_value('RepeatBarrage',$it['RepeatBarrage']); ?>"   required=1>
					
					<span class="help-inline"></span>
				</div>
			</div> -->
<!--  
			<div class="control-group">
				<label for="title" class="control-label">总弹幕频率</label>
				<div class="controls">
					<input type="number" name="BarrageFrequency" id="BarrageFrequency" value="<?php echo set_value('BarrageFrequency',$it['BarrageFrequency']); ?>"   required=1>
					
					<span class="help-inline">条/分钟</span>
				</div>
			</div>
			
			
			<div class="control-group">
				<label for="title" class="control-label">重复帐号的数量</label>
				<div class="controls">
					<input type="number" name="RepeatAccount" id="RepeatAccount" value="<?php echo set_value('RepeatAccount',$it['RepeatAccount']); ?>"   required=1>
					
					<span class="help-inline"></span>
				</div>
			</div>
-->			
			<!-- switch demo -->
			<div class="control-group">
				<label class="control-label" for="status">所有帐号状态</label>
				<div class="controls">
					<?php
					$status = array(
						array(
							'title' => "不讲话"
							,'value' => '0'
						)
						,array(
							'title' => "讲话"
							,'value' => '1'
						)
					);
					echo ui_btn_switch('audit',$it['audit'],$status);
					?>
					<span class="help-inline"></span>
				</div>
			</div>
			
			
		
		</div>
		<div class="boxed-footer">
			<?php if ($this->ccid): ?>
			<input type="hidden" name="ccid" value="<?php echo $this->ccid ?>">
			<?php endif ?>
			<input type="hidden" name="cid" value="<?php echo $this->cid ?>">
			<input type="hidden" name="id" value="<?php echo $it['id']?>">
			<input type="submit" value="<?php echo lang('submit') ?>" class="btn btn-primary">
			<input type="reset" value="<?php echo lang('reset') ?>" class="btn btn-danger">
		</div>
		
		
<!--  		<div class="boxed-inner seamless">
		<div class="control-group">
				<label for="title" class="control-label">消息内容</label>
				<div class="controls">
					<input type="text"  id="content" value="<?php echo set_value('content',$it['content']); ?>"  >
					
					<!--  <span class="help-inline">空则是不发信息，只设置</span>-->
<!-- 					重复弹幕次数
					<input type="number"  id="RepeatBarrage" value="<?php echo set_value('RepeatBarrage',$it['RepeatBarrage']); ?>"   required=1>
					<input type="button"  id="sendButton" value="发送" class="btn btn-primary">
				</div>
				
				
			</div>
		</div>
		-->
		
	</form>
</div>

<!-- 多图上传修改
<input class="fileupload" type="file" accept="" multiple="multiple" data-for="photo" data-size="">
data-more="1"
list_upload


$("#sendButton").click(function(){
		var su='<?php echo site_urlc('room/SendMsg'); ?>';
		
		$.ajax({
		url: su,
		type: 'POST',
		dataType: 'JSON',
		data: {
			content:$("#content").val(),
			RepeatBarrage:$("#RepeatBarrage").val(),
			_cfs:$.cookie('_cfc'),
			id:"<?php echo $_GET['p0'] ?>"
		}   
		})
		.done(function(data) {
			alert(data.msg);
		})
		.fail(function(data) {
			alert(data);
		})
	});
-->

<!-- 注意加载顺序 -->
<?php include_once 'inc_ui_media.php'; ?>
<script type="text/javascript">
require(['adminer/js/ui','adminer/js/media','bootstrap-datetimepicker.zh'],function(ui,media){
	$('.timepicker').datetimepicker({'language':'zh-CN','format':'yyyy/mm/dd hh:ii:ss','todayHighlight':true});

	
	
});
</script>
