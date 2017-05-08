<?php

function getRoomStatus($rid)
{
    $st = '未知';
    $rdata['threads_num'] = '未知';
    $url = roominfo_url($rid);
    $get_data = curl_request($url);
    $get_data = object2array(json_decode($get_data));
    
    if (isset($get_data) && $get_data) {
        if (isset($get_data['ss'])) {
            if ($get_data['ss'] == 1) {
                $st = '直播中';
            } else {
                $st = '未直播';
            }
        }
    }
    
    if(isset($get_data['threads_num'])){
        $rdata['threads_num']=$get_data['threads_num'];
    }
    
    $rdata['st']=$st;
    return $rdata;
}
?>
<div class="btn-group">
	<a href="<?php echo site_urlc('room/create')?>" class='btn btn-primary'>
		<i class="fa fa-plus"></i> <?php echo $title; ?> </a>
</div>

<?php //include_once 'inc_modules_path.php'; ?>

<?php include_once 'inc_room_search.php'; ?>

<?php include_once 'inc_ctype_index.php'; ?>

<div class="clearfix">
	<p></p>
</div>

<div class="boxed">
	<div class="boxed-inner seamless">

		<table class="table table-striped table-hover select-list">
			<thead>
				<tr>
					<th class="width-small"><input id='selectbox-all' type="checkbox"></th>
					<th>ID</th>
					<th>房间号</th>
					<th>房间状态</th>
					
					<th>主播名</th>
					<th>帐号数量</th>
					<th>登录间隔</th>
					<th>说话最大间隔</th>
	
			
			
			<?php if(in_array($this->cid,array(0))){?>
			<?php if (!$this->ccid): ?>
			<th>伪子栏目</th>
			<?php endif ?>
			<?php }?>
			<th>更新时间</th>
					<th>详细信息</th>
					<th class="span1">操作</th>
				</tr>
			</thead>
			<tbody class="sort-list">
		<?php foreach ($list as $v):?>
		<tr data-id="<?php echo $v['id'] ?>"
					data-sort="<?php echo $v['sort_id'] ?>">
					<td><input class="select-it" type="checkbox"
						value="<?php echo $v['id']; ?>"></td>
					<td>
				<?php echo $v['id']?>
			 </td>
					<td><input type="text" class="sortid"
						value="<?php echo $v['sort_id']?>"
						data-id="<?php echo $v['id'] ?>"> <a
						href="https://www.douyu.com/<?php echo $v['title'] ?>"
						target="_blank"><?php echo $v['title'] ?></a></td>
					<td><?php
					$roomInfo=getRoomStatus($v['title']);
    echo $roomInfo['st'];
    ?></td>
					<td><?php echo $v['nickname']?></td>
					<td><?php echo $roomInfo['threads_num']?></td>
					<td><?php echo $v['LoginInterval']?></td>
					<td><?php echo $v['SpeechInterval']?></td>
			
			
			<?php if(in_array($this->cid,array(0))){?>
			<?php if (!$this->ccid): ?>
			<td><a href="<?php echo site_url('room/index?c=5&cc='.$v['id']) ?>">
							伪子栏目文章 </a> | <a
						href="<?php echo site_url('links/index?c=5&cc='.$v['id']) ?>">
							伪子栏目链接 </a> | <a
						href="<?php echo site_url('lists/index?c=5&cc='.$v['id']) ?>">
							伪子栏目清单 </a> | <a
						href="<?php echo site_url('gallery/index?c=5&cc='.$v['id']) ?>">
							伪子栏目画廊 </a></td>
			<?php endif ?>
			<?php }?>

			<td> <?php echo date("Y/m/d H:i:s",$v['timeline']); ?> </td>
					<td><a href="#info" role="button" class="btn btn-info"
						data-toggle="modal"
						onclick="getRoomInfo('<?php echo $v['title']?>');">详细信息</a></td>
					<td>
						<div class="btn-group">
							<!--<?php include 'inc_ui_flag.php'; ?>-->
					<?php if(ENVIRONMENT=="development"){ ?>
					<!--  <a class='btn  btn-small btn-ajax-copy' data-id="<?php echo $v['id'] ?>" href="#"  title="复制"> 复制</a>-->
					<?php } ?>
					
					
					<?php include 'inc_ui_audit.php'; ?>
					<a class='btn btn-small'
								href=" <?php echo site_urlc( $this->router->class.'/edit/'.$v['id']) ?> "
								title="<?php echo lang('edit') ?>"> <i class="fa fa-pencil"></i> <?php // echo lang('edit') ?></a>
							<a class='btn btn-danger btn-small btn-del'
								data-id="<?php echo $v['id'] ?>" href="#"
								title="<?php echo lang('del') ?>"> <i class="fa fa-times"></i> <?php // echo lang('del') ?></a>
						</div>
					</td>
				</tr>
		<?php endforeach;?>
	</tbody>
		</table>

		<!-- INFO -->

	</div>
</div>

<div class="btn-group">
	<a id='select-all' class='btn' href="#"> <i class=""></i> <?php echo lang('select_all') ?> </a>
	<a id='unselect-all' class='btn hide' href="#"> <i class=""></i> <?php echo lang('unselect') ?> </a>
	<a id="btn-del" class='btn btn-danger' href="#"> <i class="fa fa-times"></i> <?php echo lang('del') ?> </a>
	<a id="btn-audit" class='btn' href="#" data-audit='1'>开启</a> <a
		id="btn-audit" class='btn' href="#" data-audit='0'>关闭</a>
</div>
<div id="info" class="modal hide fade">
	<div class="modal-header">
		<button type="button" class="close" data-dismiss="modal"
			aria-hidden="true">
			<i class="fa fa-times"></i>
		</button>
		<h3>
			<i class="fa fa-info-circle"></i>详细信息
		</h3>
	</div>
	<div class="modal-body seamless">


		<div class="boxed">
			<div class="boxed-inner seamless">
				<table class="table table-striped table-hover select-list">
					<thead>
						<tr>
							<th>昵称</th>
							<th>状态</th>
							<th>最大发送</th>
							<th>已发送</th>
						</tr>
					</thead>
					<tbody id="show_tr">

					</tbody>
				</table>
			</div>
		</div>

	</div>
	<div class="modal-footer">
		<a href="#" data-dismiss="modal" aria-hidden="true"
			class="btn btn-danger"> <?php echo lang('close') ?></a>
	</div>
</div>
<!-- end modal -->


<?php echo $pages; ?>

<script>
require(['adminer/js/ui'],function(ui){
	var article = {
		url_del: "<?php echo site_urlc('room/delete'); ?>"
		,url_audit: "<?php echo site_urlc('room/audit'); ?>"
		,url_flag: "<?php echo site_urlc('room/flag'); ?>"
		,url_sortid: "<?php echo site_urlc('room/sortid'); ?>"
		,url_sort_change: "<?php echo site_urlc('room/sort_change'); ?>"
		,url_copy: "<?php echo site_urlc('room/copypro'); ?>" 
	};
	
	ui.fancybox_img();
	ui.btn_delete(article.url_del);		// 删除
	ui.btn_audit(article.url_audit);	// 审核
	ui.btn_flag(article.url_flag);		// 推荐
	ui.sortable(article.url_sortid);	// 排序  拖动排序和序号排序在firefox中有bug
	ui.sort_change(article.url_sort_change); // input 排序
	ui.btn_copy(article.url_copy);    // 热门审核	
});
function getRoomInfo(rid){
	var su='<?php echo site_urlc('room/getRoomInfo'); ?>';
	
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
		$("#show_rid").html('房间号:'+rid);
		var x = eval("(" + data + ")");
		$("#show_tr").empty();   
		if(typeof x.threads !="undefined"){
		    if(x.threads != '' || x.threads != null){
		    	for(var i=0;i<x.threads.length;i++){
		    		x.threads[i]['pause'] = '激活'; 
			    	if(x.threads[i]['pause'] == false){
			    		x.threads[i]['pause'] = '未激活'; 
				    }
			    	var text = '<tr class="js-get-one"><td>'+x.threads[i]['nickname']+'</td><td>'+x.threads[i]['pause']+'</td><td>'+x.threads[i]['max_send']+'</td><td>'+x.threads[i]['send_count']+'</td></tr>';
			    	$("#show_tr").prepend(text);
			    }
			}
		}
		
		console.log(data);
	})
	.fail(function(data) {
		$("#show_msg").html(data);
	})		   	   
}
</script>
