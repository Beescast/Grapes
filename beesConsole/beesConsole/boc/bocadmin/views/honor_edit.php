
<div class="btn-group">
	<a href="<?=site_urlc($this->class.'/index')?>" class='btn'> <i class="fa fa-arrow-left"></i> 返回列表</a>
</div>

<?php include_once 'inc_form_errors.php'; ?>

<div class="boxed">

	<h3> 添加 <span class="badge badge-success pull-right"><?php echo $title; ?></span></h3>
	<?php echo form_open(current_urlc(),array("class"=>"form-horizontal","id"=>"frm-create")); ?>

		<div class="boxed-inner seamless">
			<div class="control-group">
				<label class="control-label" for="title">标题</label>
				<div class="controls">
					<input type="text" id="title" name="title" value="<?php echo set_value('title',$it['title']) ?>" x-webkit-speech>
					<a href="#seo-modal" role="button" class="btn btn-info" data-toggle="modal">SEO</a>
					<span class="help-inline"></span>
				</div>
			</div>

			<?php if($this->cid==24){ ?>
			<div class="control-group">
				<label class="control-label" for="url">链接地址:</label>
				<div class="controls">
					<input type="text" id="url" name="url" value="<?php echo set_value('url',$it['url']) ?>">
				</div>
			</div>
			<?php } ?>

			<!-- 弹出 -->
			<div id="seo-modal" class="modal hide fade">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="fa fa-times"></i></button>
					<h3> <i class="fa fa-info-circle"></i> SEO优化</h3>
				</div>
				<div class="modal-body seamless">

					<div class="control-group">
						<label for="title_seo" class="control-label">标题优化</label>
						<div class="controls">
							<input type="text" id="title_seo" name="title_seo" value="<?php echo set_value('title_seo',$it['title_seo']) ?>" x-webkit-speech>
							<span class="help-inline"></span>
						</div>
					</div>

					<div class="control-group">
						<label class="control-label" for="tag">标签</label>
						<div class="controls">
							<input type="text" id="tags" name="tags" value="<?php echo set_value('tags',$it['tags']) ?>" >
							<span class="help-inline">使用英文标点`,`隔开</span>
						</div>
					</div>

					<div class="control-group">
						<label for="intro"  class="control-label">简介</label>
						<div class="controls">
							<textarea name="intro" rows='8' class='span4'><?php echo set_value('intro',$it['intro']) ?></textarea>
							<span class="help-inline"></span>
						</div>
					</div>

				</div>
				<div class="modal-footer">
					<a href="#"  data-dismiss="modal" aria-hidden="true" class="btn">Close</a>
				</div>
			</div>

			<!-- 图片上传 -->
			<div class="control-group">
				<label for="img" class="control-label">图片：</label>
				<div class="controls">
					<div class="btn-group">
						<span class="btn btn-success">
							<i class="fa fa-upload"></i>
							<span> 上传图片(<?php if($this->cid==6){ echo '195*135';}else{ echo '202*120';} ?>) </span>
							<input class="fileupload" type="file" accept="">
							<!-- <input class="fileupload" type="file"  accept="" multiple=""> -->
						</span>
						<input type="hidden" name="photo" class="form-upload" data-more="0" value="<?php echo $it['photo'] ?>">
						<input type="hidden" name="thumb" class="form-upload-thumb" value="<?php echo $it['thumb'] ?>">
						<!-- <input type="hidden" name="photo" class="form-upload" data-more='1' value="<?php echo $it['photo'] ?>">
						<input type="hidden" name="thumb" class="form-upload-thumb" value="<?php echo $it['thumb'] ?>"> -->
					</div>
				</div>
			</div>

			<div id="js-photo-show" class="js-img-list-f">
				<!-- 模板 #tpl-img-list -->
			</div>
			<div class="clear"></div>

		</div>

		<div class="boxed-footer">
			<?php if ($this->ccid): ?>
			<input type="hidden" name="ccid" value="<?php echo $this->ccid ?>">
			<?php endif ?>
			<input type="hidden" name="cid" value="<?php echo $this->cid ?>">
			<input type="hidden" name="id" value="<?php echo $it['id'] ?>">
			<input type="submit" value=" <?php echo lang('submit'); ?> " class='btn btn-primary'>
			<input type="reset" value=' <?php echo lang('reset'); ?> ' class="btn btn-danger">
		</div>

	</form>
</div>

<!-- 注意加载顺序 -->
<?php include_once 'inc_ui_media.php'; ?>
<script>
require(['media'],function(media){
	var honor_photos =  <?php echo json_encode(list_upload(set_value('photo',$it['photo']))) ?>;
	// 加载图片
	media.init();
	media.show(honor_photos,'photo');
});
</script>
<?php echo static_file('adminer/js/honor.js'); ?>
