<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

/**
 * Class Article extends CI_Controller
 * @author
 * 信息类
 */
class Article extends Modules_Controller
{

	function __construct()
	{
		parent::__construct();

		$this->rules = array(
			"rule" => array(
				array(
					"field" => "title",
					"label" => lang('title'),
					"rules" => "trim"
				)
				,array(
					"field" => "timeline",
					"label" => lang('time'),
					"rules" => "trim|strtotime"
				)
				,array(
					"field" => "content",
					"label" => lang('conent'),
					"rules" => "trim"
					// link_create tag 生成
				)
				,array(
					"field" => "photo",
					"label" => lang('photo'),
					"rules" => "trim"
				)
			)
		);

	}
	public function copypro()
    {
        $ids = $this->input->post('ids');
       
        $rs=$this->model->get_one($ids);

        unset($rs['id']);
        unset($rs['sort_id']);
        unset($rs['timeline']);
        
        $id = $this->model->create($rs);
        if ($id) {
            $vdata['msg'] = '复制成功，请刷新查看';
            $vdata['status'] = 1;
        }else{
            $vdata['msg'] = '复制失败，请刷新后重试';
            $vdata['status'] = 0;
        }
        $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
    }

}
