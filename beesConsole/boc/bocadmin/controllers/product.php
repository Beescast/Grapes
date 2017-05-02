<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

/**
 * Class Product extends Modules_Controller
 * @author
 */
class Product extends Modules_Controller{
    protected $rules = array(
        "rule" => array(
            array(
                "field" => "title",
                "label" => "标题",
                "rules" => "trim|required|min_length[6]"
            )
            ,array(
                "field" => "content",
                "label" => "内容",
                "rules" => "trim"
            )
        )
    );

    public function __construct(){
        parent::__construct();
        $this->load->model('Upload_model','mupload');
    }

    public function _edit_data()
    {
        $form=$this->input->post();
        $form['timeline'] = time();
        return $form;
    }

    // 删除条目时删除文件
    protected function _rm_file($ids)
    {
        $fids = array() ;
        if (is_numeric($ids)) {
            $tmp = $this->model->get_one($ids,'photo');
            $fids = explode(',',$tmp['photo']);
        }else if(is_array($ids)){
            // 使用 字符串where时
            $tmp = $this->model->get_all("`id` in (".implode(',', $ids).")",'photo');
            foreach ($tmp as $key => $v) {
                $fids = array_merge($fids, explode(',',$v['photo']));
            }
        }
        // adminer funs helpers
        unlink_upload($fids);
    }
}
