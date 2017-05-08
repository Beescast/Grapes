<?php include_once 'inc_modules_path.php'; ?>

<h3>  <i class="fa fa-pencil"></i>  <?php echo $title; ?></h3>

<?php include_once 'inc_form_errors.php'; ?>

<div class="boxed">
	<?php echo form_open(site_urlc($this->class.'/edit'), array('class' => 'form-horizontal', 'id' => 'frm-edit')); ?>

		<input class="hide" type="text" id="p-title" name="title" value="<?php echo set_value('title',$seo['title']) ?>">
		<input class="hide" type="text" id="p-title_seo" name="title_seo" value="<?php echo set_value('title_seo',$seo['title_seo']) ?>">
		<input class="hide" type="text" id="p-tags" name="tags" value="<?php echo set_value('tags',$seo['tags']) ?>">
		<textarea class="hide" id='p-intro' name="intro" rows='8' class='span4'><?php echo set_value('intro',$seo['intro']) ?></textarea>

		<div class="boxed-inner seamless">
<?php if(in_array($_GET['c'],array(1))){?>
	
			<div class="control-group">
				<label for="title" class="control-label">房间号</label>
				<div class="controls">
					<input type="number" name="rid" id="rid"  value="<?php echo set_value('rid',$it['rid']); ?>"  required=1>
					<span class="help-inline"></span>
				</div>
			</div>
			<div class="control-group">
				<label for="title" class="control-label">信息内容</label>
				<div class="controls">
					<input type="text" name="msg" id="msg"  value="<?php echo set_value('msg',$it['msg']); ?>"  required=1>
					<span class="help-inline"></span>
				</div>
			</div>
			<div class="control-group">
				<label for="title" class="control-label">重复次数</label>
				<div class="controls">
					<input type="number" name="repeat" id="repeat"  value="<?php echo set_value('repeat',$it['repeat']); ?>"  required=1>
					<span class="help-inline"></span>
				</div>
			</div>
			<!-- switch demo -->
		<div class="control-group">
			<label class="control-label" for="status">弹幕卡</label>
			<div class="controls">
					<?php
    $color = array(
        array(
            'title' => "默认",
            'value' => '0'
        )
        ,array(
            'title' => "红",
            'value' => '1'
        )
,array(
    'title' => "蓝",
    'value' => '2'
)
,array(
    'title' => "绿",
    'value' => '3'
)
,array(
    'title' => "橙",
    'value' => '4'
)
,array(
    'title' => "紫",
    'value' => '5'
)
,array(
    'title' => "粉",
    'value' => '6'
)
    );
    echo ui_btn_switch('color', $it['color'], $color);
    ?>
					<span class="help-inline"></span>
			</div>
		</div>
			
<?php }?>		
<?php if(!in_array($_GET['c'],array(1))){?>
			<div class="control-group uefull">
				<textarea id="editor_id" name="content" > <?php echo set_value('content',$it['content']); ?></textarea>
				<!-- <span class="help-inline"></span> -->
			</div>

			<!-- 图片上传 -->
			<div class="control-group">
				<label for="img" class="control-label">图片：</label>
				<div class="controls">
					<div class="btn-group">
						<span class="btn btn-success">
							<i class="fa fa-upload"></i>
							<span> <?php echo lang('upload_file') ?> </span>
							<input class="fileupload" type="file" accept="" data-for="photo" multiple="multiple">
						</span>
						<input type="hidden" name="photo" class="form-upload" data-more="1" value="<?php echo $it['photo'] ?>">
						<input type="hidden" name="thumb" class="form-upload-thumb" value="<?php echo $it['thumb'] ?>">
					</div>
				</div>
			</div>

			<div id="js-photo-show" class="js-img-list-f">
				<!-- 模板 #tpl-img-list -->
			</div>

			<div class="clear"></div>
<?php }?>
		</div>

		<div class="boxed-footer">
			<input type="hidden" name="cid" value="<?php echo $this->cid ?>">
			<input type="hidden" name="id" value="<?php echo $it['id']?>">
			<input type="submit" value="<?php echo lang('submit') ?>" class="btn btn-primary">
			<input type="reset" value="<?php echo lang('reset') ?>" class="btn btn-danger">
		</div>
	</form>
</div>

<?php include_once 'inc_ui_media.php'; ?>

<script type="text/javascript">
require(['jquery','adminer/js/ui','adminer/js/media'],function($,ui,media){
	ui.editor_create('editor_id');
	var page_photos = <?php echo json_encode(list_upload($it['photo'])) ?>;
	media.init();
	media.show(page_photos,'photo');
	media.sort('photo');
	$("#js-photo-show" ).sortable().disableSelection();
});
</script>
<?php //echo static_file('adminer/js/page.js'); ?>
