<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

// 反馈
class feedback extends MY_Controller {

	protected $rules = array(
		"send" => array(
			array(
				"field" => "title",
				"label" => "标题",
				"rules" => "trim|required"
			)			
			,array(
				"field" => "content",
				"label" => "内容",
				"rules" => "trim|required"
			)
			,array(
				"field" => "username",
				"label" => "用户名",
				"rules" => "trim|required"
			)
			,array(
				"field" => "email",
				"label" => "邮箱帐号",
				"rules" => "trim|required|strtolower|valid_email"
			)			
			,array(
				"field" => "tel",
				"label" => "电话号码",
				"rules" => "trim|numeric"
			)		
			,array(
				"field" => "fax",
				"label" => "传真号码",
				"rules" => "trim|numeric"
			)
			,array(
				"field" => "captcha",
				"label" => "验证码",
				"rules" => "trim|callback_captchas_verify"
			)

		)
	);

	function __construct()
	{
        parent::__construct();
        $this->load->model('feedback_model','mfb');
        $this->model = & $this->mfb; // 处理model
    }

	// 用户反馈信息
	public function send_ajax()
	{
		if ($this->input->is_ajax_request()) {
			$this->form_validation->set_rules($this->rules['send']);
			$vdata = array( 'status' => 0, 'msg' => '未知错误！'); 
			if ($this->form_validation->run() == FALSE) {
				$vdata['msg'] = validation_errors();
			}else{
				// 处理下 应该引用form_validation处理后的数据
				unset($_POST['captcha']);
				$data = $this->input->post();
				$data['content'] = str_replace("\n","<br/>",$this->input->post('content',true));
				if ($this->model->create($data)) {
					$vdata['status'] = 1;
					$vdata['msg'] = "已经提交信息，我们会尽快回复您！";
				}
			}
			$this->output->set_content_type('application/json')->set_output(json_encode($vdata));
		}else{
			show_404();
		}
	}
}
