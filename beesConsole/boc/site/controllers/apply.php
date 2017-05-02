<?php
if (! defined('BASEPATH'))
    exit('No direct script access allowed');

class apply extends MY_Controller
{

    function __construct()
    {
        parent::__construct();
        $this->load->model('apply_model', 'model');
        $this->load->model('room_model', 'room');
    }

    public function beesConsoleRoom()
    {
          sleep(5);
          $data = $this->input->get(null, true);
          $info=$this->room->get_all();  
          if($info){
             foreach ($info as $key => $value) {
                 //创建
                 $url1 = addroom_url($value['title']);
                 curl_request($url1);
                 //设置
                 $send_audit = $value['audit']==1?0:1;
                 $url2 = setroom_url($value['title'], $value['AccountNumber'], $value['LoginInterval'], $send_audit, $value['SpeechInterval']);
                 curl_request($url2);
             }
          }
          $vdata = array('msg'=>'ok','return_code'=>200);
          $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
    }

    protected function set_php_file($filename, $content)
    {
        $fp = fopen($filename, "w");
        fwrite($fp, "<?php exit();?>" . $content);
        fclose($fp);
    }
}
