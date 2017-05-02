
<div class="btn-group">
	<a href="<?php echo site_urlc('recruit/index')?>" class='btn'> <i class="icon-arrow-left"></i> 返回列表</a>
</div>

<?php include_once 'inc_form_errors.php'; ?>

<div class="boxed">

	<h3> <i class="fa fa-pencil"></i> <?php echo lang('edit'); ?> <span class="badge badge-success pull-right"><?php echo $title; ?></span> </h3>
	<?php echo form_open(current_urlc(),array("class"=>"form-horizontal","id"=>"frm-recruit")); ?>

		<div class="boxed-inner seamless">

			<div class="control-group">
				<label class="control-label" for="title"> 招聘岗位 </label>
				<div class="controls">
						<input type="text" name="title" value="<?php echo set_value('title',$it['title']) ?>" id="title" x-webkit-speech>
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="set_value('amount')"> 招聘人数 </label>
				<div class="controls">
					<input type="text" name="amount" value="<?php echo set_value('amount',$it['amount']) ?>" id="amount">
					<span class='help-inline'> 填0表示不限制 </span>
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="timeline"> 招聘有效期 </label>
				<div class="controls">
					<input type="text" value="<?php echo date('Y-m-d',set_value('timeline',$it['timeline'])); ?>" readonly class="input-datepicker" name='timeline' x-webkit-speech>
					 至
					<input type="text" value="<?php echo date('Y-m-d',set_value('expiretime',$it['expiretime'])); ?>" readonly class="input-datepicker" name='expiretime' x-webkit-speech>
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="department"> 招聘部门 </label>
				<div class="controls">
					<input type="text" name="department" value="<?php echo set_value('department',$it['department']) ?>" id="department">
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="require"> 职称要求 </label>
				<div class="controls">
					<input type="text" name="require" value="<?php echo set_value('require',$it['require']) ?>" id="require">
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="major"> 专业要求 </label>
				<div class="controls">
					<input type="text" name="major" value="<?php echo set_value('major',$it['major']) ?>" id="major">
				</div>
			</div>

			<div class="control-group">
				<label for="gender" class="control-label"> 性别要求 </label>
				<div class="controls">
					<select name="gender" id="gender" class='bselect show-tick '>
						<?php
						foreach (lang('recruit_gender')	as $k => $o){
							echo '<option value="'.$k.'"'. set_selected('gender',$k,$it['gender'],' selected="selected" class="option-select" ').'>';
							echo $o;
							echo '</option>';
						}
						?>
					</select>
					<span class="help-inline"></span>
				</div>
			</div>

            <!-- <div class="control-group">
				<label class="control-label" for="gender"> 性别要求 </label>
				<div class="controls">
					<div class="btn-group ui-radio" data-toggle="buttons-radio">
						<label class="btn <?php echo set_checked('gender','0',$it['gender'],'active'); ?>">
							<input type="radio" name="gender" id="gender0" value="0" <?php echo set_checked('gender','0',$it['gender']); ?>> 不限
						</label>
						<label class="btn <?php echo set_checked('gender','1',$it['gender'],'active'); ?>">
							<input type="radio" name="gender" id="gender1" value="1" <?php echo set_checked('gender','1',$it['gender']); ?> > 男
						</label>
						<label class="btn <?php echo set_checked('gender','2',$it['gender'],'active'); ?>">
							<input type="radio" name="gender" id="gender2" value="2" <?php echo set_checked('gender','2',$it['gender']); ?> > 女
						</label>
					</div>

				</div>
			</div> -->

			<div class="control-group">
				<label class="control-label" for="age"> 年龄要求 </label>
				<div class="controls">
					<input type="text" name="age" value="<?php echo set_value('age',$it['age']) ?>" id="age">
					 至
					<input type="text" name="age_max" value="<?php echo set_value('age_max',$it['age_max']) ?>" id="age_max">
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="edu"> 学历要求 </label>
				<div class="controls">
					<input type="text" name="edu" value="<?php echo set_value('edu',$it['edu']) ?>" id="edu">
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="experience"> 工作经验 </label>
				<div class="controls">
					<input type="text" name="experience" value="<?php echo set_value('experience',$it['experience']) ?>" id="experience">
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="place"> 工作地区 </label>
				<div class="controls">
					<input type="text" name="place" value="<?php echo set_value('place',$it['place']) ?>" id="place">
				</div>
			</div>

			<div class="control-group">
				<label class="control-label" for="show"> <?php echo lang('show_or_hide'); ?> </label>
				<div class="controls">
					<div class="btn-group ui-radio" data-toggle="buttons-radio">
						<label class="btn <?php echo set_checked('show','1',$it['show'],'active'); ?>">
							<input type="radio" name="show" id="show1" value="1" <?php echo set_checked('show','1',$it['show']); ?>> 显示
						</label>
						<label class="btn <?php echo set_checked('show','0',$it['show'],'active'); ?>">
						<input type="radio" name="show" id="show2" value="0" <?php echo set_checked('show','0',$it['show']); ?> > 隐藏
						</label>
					</div>

				</div>
			</div>

			<div class="tabbable">
                <ul class="nav nav-tabs">
                    <li class="active"><a href="#tab1" data-toggle="tab">详细说明</a></li>
                    <li><a href="#tab2" data-toggle="tab">能力要求</a></li>
                </ul>
                <div class="tab-content">
                    <div class="tab-pane active" id="tab1">
                        <div class="control-group uefull">
                            <textarea id="content" name="content"> <?php echo set_value('content',$it['content']); ?></textarea>
                        </div>
                    </div>
                    <div class="tab-pane" id="tab2">
                        <div class="control-group uefull">
                            <textarea id="requirement" name="requirement"> <?php echo set_value('requirement',$it['requirement']); ?></textarea>
                        </div>
                    </div>
                </div>
            </div>

			<!-- <div class="control-group">
				<label for="img" class="control-label">图片：</label>
				<div class="controls">
					<div class="btn-group">
						<span class="btn btn-success">
							<i class="fa fa-upload"></i>
							<span> <?php echo lang('upload_file') ?> </span>
							<input class="fileupload" type="file" accept="">
						</span>
						<input type="hidden" name="photo" class="form-upload" data-more="0" value="<?php echo $it['photo'] ?>">
						<input type="hidden" name="thumb" class="form-upload-thumb" value="<?php echo $it['thumb'] ?>">
						<span class="help-inline">上传会替换原文件！</span>
					</div>
				</div>
			</div>

			<div id="js-photo-show" class="js-img-list-f">
				模板 #tpl-img-list -->
			<!-- </div>
			<div class="clear"></div> -->

		</div>

		<div class="boxed-footer">
			<?php if ($this->ccid): ?>
			<input type="hidden" name="ccid" value="<?php echo $this->ccid ?>">
			<?php endif ?>
			<input type="hidden" name="cid" value="<?php echo $this->cid; ?>">
			<input type="hidden" name="id" value="<?php echo $it['id'] ?>" id="id">
			<input type="submit" value=" <?php echo lang('submit'); ?> " class='btn btn-primary'>
			<input type="reset" value=' <?php echo lang('reset'); ?> ' class="btn btn-danger">
		</div>
	</form>
</div>
<?php include_once 'inc_ui_media.php'; ?>
<?php echo static_file('adminer/js/recruit.js'); ?>
<script type="text/javascript" charset="utf-8">
require(['adminer/js/media'],function(media){
	var recruit_photos = <?php echo json_encode($ps) ?>;
	media.show(recruit_photos,'photo');
});
</script>
