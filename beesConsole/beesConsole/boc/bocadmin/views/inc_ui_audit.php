<?php //TODO:检测权限 ?>
<?php if(isset($_GET['c'])&&in_array($_GET['c'],array(2,3))){?>

<?php if ($v['audit']): ?>
	<a href="#"  title="关闭机器人"  class='btn btn-primary btn-small btn-ajax-audit' data-id="<?php echo $v['id'] ?>" data-audit="0">  <i class="fa fa-thumbs-up"></i> </a>
<?php else: ?>
	<a href="#" title="启动机器人" class='btn btn-small btn-ajax-audit' data-id="<?php echo $v['id'] ?>" data-audit="1"> <i class="fa fa-thumbs-down"></i> </a>
<?php endif ?>

<?php }else{?>

<?php if ($v['audit']): ?>
	<a href="#"  title="<?php echo lang('audit_remove') ?>"  class='btn btn-primary btn-small btn-ajax-audit' data-id="<?php echo $v['id'] ?>" data-audit="0">  <i class="fa fa-thumbs-up"></i> </a>
<?php else: ?>
	<a href="#" title="<?php echo lang('audit') ?>" class='btn btn-small btn-ajax-audit' data-id="<?php echo $v['id'] ?>" data-audit="1"> <i class="fa fa-thumbs-down"></i> </a>
<?php endif ?>

<?php }?>


