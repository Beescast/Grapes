<div class="btn-group">
	<a href="<?php echo site_urlc($this->class.'/create') ?>" id="btn-create" class='btn btn-primary' >  <i class="fa fa-plus"></i> <?php echo $title ?> </a>
</div>

<?php include_once 'inc_modules_path.php'; ?>

<div class="boxed">
	<div class="boxed-inner">
	<h3> <input id='selectbox-all' type="checkbox"> <?php echo $title ?> </h3>
	<ul class="boxed-list select-list sort-list">
	<?php foreach ($list as $v):?>
		<li data-id="<?php echo $v['id'] ?>" data-sort="<?php echo $v['sort_id'] ?>">
		<span> <input class="select-it" type="checkbox" value="<?php echo $v['id']; ?>" > </span>
		 <span>
		 	<a class="fancybox-img" href="<?php echo UPLOAD_URL. str_replace('thumbnail/', '', $v['thumb']); ?>" title="<?php echo $v['title'] ?>">
		 		<img src="<?php echo UPLOAD_URL.$v['thumb'] ?>" alt="<?php echo $v['title'];?>">
		 	</a>
		 </span>

		 <span>
		 	<?php echo $v['title']; ?>
		 </span>

		 <div class="btn-group pull-right">
		 	<?php include 'inc_ui_audit.php'; ?>
		 	<a class='btn btn-small' href=" <?php echo site_urlc( $this->router->class.'/edit/'.$v['id']) ?> " title="<?php echo lang('edit') ?>"> <i class="fa fa-pencil"></i> <?php // echo lang('edit') ?></a>
		 	<a class="btn btn-danger btn-small btn-del" href="#" title="<?php echo lang('del') ?>" data-id="<?php echo $v['id'] ?>"> <i class="fa fa-times"></i></a>
		 </div>
		 </li>
	<?php endforeach; ?>
	</ul>
	</div>
</div>

<div class="btn-group">
	<a id='select-all' class='btn' href="#"> <i class=""></i> <?php echo lang('select_all') ?> </a>
	<a id='unselect-all' class='btn hide' href="#"> <i class=""></i> <?php echo lang('unselect') ?> </a>
	<a id="btn-del" class='btn btn-danger' href="#"> <i class="fa fa-times"></i> <?php echo lang('del') ?> </a>
</div>

<?php echo $pages; ?>

<script>
require(['adminer/js/ui'],function(ui){

	var gallery = {
		del: "<?php echo site_urlc('gallery/delete'); ?>"
		,audit: "<?php echo site_urlc('gallery/audit'); ?>"
		,url_sort: "<?php echo site_urlc('gallery/sortid'); ?>"
	};

	ui.fancybox_img();
	ui.btn_delete(gallery.del);		// 删除
	ui.btn_audit(gallery.audit);	// 审核
	ui.sortable(gallery.url_sort);	// 排序
});
</script>
