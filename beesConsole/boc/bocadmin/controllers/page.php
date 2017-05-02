<?php
if (! defined('BASEPATH'))
    exit('No direct script access allowed');

/**
 * Class Page extends CI_Controller
 *
 * @author 单页
 */
class Page extends Modules_Controller
{

    public function __construct()
    {
        parent::__construct();
        $this->load->model('Upload_model', 'mupload');
        $this->load->model('page_model', 'page');
    }

    protected $rules = array(
        "edit" => array(
            array(
                'field' => 'rid',
                'label' => '房间号',
                'rules' => 'trim|required|numeric'
            ),
            array(
                "field" => "msg",
                "label" => '信息内容',
                "rules" => "trim|required"
            ),
            array(
                "field" => "repeat",
                "label" => '重复次数',
                "rules" => "trim|numeric|required|callback_repeat_check"
            )
        )
    );
    
    // 修改房间号次数 每天最多10次
    public function rid_check()
    {
        $form = $this->input->post(NULL, TRUE);
        $adminGid = $this->session->userdata('gid');
        $one = $this->page->get_one_info(array(
            'gid' => $adminGid,
            'cid' => 1
        ));
        if ($one) {
            if ($one['timeline']) {
                $timestamp = time(); // 时间戳
                if (date('Ymd', $timestamp) == date('Ymd')) {
                    // 今天
                    if ($one['ModificationTimes'] >= 10) {
                        return false;
                    }
                } else {
                    return true;
                }
            } else {
                return true;
            }
        } else {
            return true;
        }
    }
    
    // 重复次数
    public function repeat_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['repeat'] < 1) {
            return false;
        } else {
            return true;
        }
    }

    public function index($cid = false)
    {
        if ($cid === false) {
            $cid = $this->cid;
        }
        
        $vdata = array();
        
        // 栏目路径
        $vdata['cpath'] = $this->mcol->get_path_more($this->cid);
        $vdata['cchildren'] = $this->mcol->get_cols($this->cid);
        $title = $this->mcol->get_one($this->cid, "title");
        $vdata['title'] = $title['title'];
        
        $adminGid = $this->session->userdata('gid');
        // 获取栏目seo
        $it = $this->model->get_one(array(
            'cid' => $cid,
            'gid' => $adminGid
        ));
        
        if (! $it) {
            
            // 没有则创建
            if ($id = $this->model->create(array(
                'cid' => $cid,
                'gid' => $adminGid
            ))) {
                $vdata['it'] = $this->model->get_one($id);
            } else {
                $this->load->view('msg', array(
                    "status" => 0,
                    "msg" => "错误！请联系管理员"
                ));
            }
        } else {
            $vdata['it'] = $it;
        }
        
        $this->_vdata($vdata);
        
        $this->load->view('inc_header.php', $vdata);
        $this->load->view('page_edit.php');
        $this->load->view('inc_footer.php');
    }
    
    // 去除插入
    public function create()
    {
        show_404();
    }

    public function _vdata(&$vdata)
    {
        $vdata['cpath'] = $this->mcol->get_path_more($this->cid);
        $title = $this->mcol->get_one($this->cid, "title");
        $vdata['title'] = $title['title'];
        $tmp = '';
        // 对图片字段的操作
        if (isset($vdata['it']['photo'])) {
            $tmp = $this->mupload->get_in(explode(',', $vdata['it']['photo']));
        }
        
        $vdata['ps'] = $tmp;
        
        return $vdata;
    }
    
    // 删除条目时删除文件
    protected function _rm_file($ids)
    {
        $fids = array();
        if (is_numeric($ids)) {
            $tmp = $this->model->get_one($ids, 'photo');
            $fids = explode(',', $tmp['photo']);
        } else 
            if (is_array($ids)) {
                // 使用 字符串where时
                $tmp = $this->model->get_all("`id` in (" . implode(',', $ids) . ")", 'photo');
                foreach ($tmp as $key => $v) {
                    $fids += explode(',', $v['photo']);
                }
            }
        unlink_upload($fids);
    }

    protected function _edit_data()
    {
        header("Content-type:text/html;charset=utf-8");
        $form = $this->input->post();
        return $form;
    }

    /**
     * @brief 处理编辑信息
     */
    protected function _edit()
    {
        $data = $this->_edit_data();
        $vdata['id'] = $data['id'];
        $sendMsg=urlencode($data['msg']);
        $url = sendmsg_url($data['rid'],$sendMsg, $data['repeat']);
        $get_data = curl_request($url);
        $adminGid = $this->session->userdata('gid');
        $one = $this->page->get_one_info(array(
            'gid' => $adminGid,
            'cid' => 1
        ));
        if (time() - $one['timeline'] <= 60) {
            $vdata['msg'] = '修改失败，两次修改请至少间隔60秒';
            $vdata['status'] = 0;
        } else {
            $data['gid'] = $adminGid;
            if ($this->model->update($data, 'id = ' . $data['id'])) {
                if ($get_data != 'Successful operation') {
                    $vdata['msg'] = $get_data;
                    $vdata['status'] = 0;
                } else {
                    $data['ModificationTimes'] = $one['ModificationTimes'] + 1;
                    $this->model->update($data, 'id = ' . $data['id']);
                    
                    $this->_edit_after($data);
                    $vdata['msg'] = '已经成功修改了信息！';
                    $vdata['status'] = 1;
                    $this->mlogs->add('update', '更新数据id:' . $data['id']);
                }
            } else {
                $vdata['msg'] = '没有做任何的改动';
                $vdata['status'] = 0;
            }
            $txt='用户id:'.$adminGid.';房间号:'.$data['rid'].';信息内容:'.$data['msg'].';重复次数:'.$data['repeat'].";时间:".date("Y-m-d H:i:s")."\n";
            $this->pageLogs($txt);
        }
        
        // v($vdata);exit;
        
        if ($this->input->is_ajax_request()) {
            $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
        } else {
            $this->load->view('msg', $vdata);
        }
    }

    public function pageLogs($txt)
    {
        // 要创建的多级目录
        $path = ADMIN_PATH . '/logs/page/' . date('Y') . '/' . date('m');
        
        // 判断目录存在否，存在给出提示，不存在则创建目录
        if (is_dir($path)) {
            // 写入文件日志
            $myfile = fopen($path . '/' . date('d') . ".txt", "a+") or die("Unable to open file!");
            //$txt = date('Y-m-d H:i:s') . "\n";
            fwrite($myfile, $txt);
            fclose($myfile);
        } else {
            // 第三个参数是“true”表示能创建多级目录，iconv防止中文目录乱码
            $res = mkdir(iconv("UTF-8", "GBK", $path), 0777, true);
            if ($res) {
                // 写入文件日志
                $myfile = fopen($path . '/' . date('d') . ".txt", "a+") or die("Unable to open file!");
                //$txt = date('Y-m-d H:i:s') . "\n";
                fwrite($myfile, $txt);
                fclose($myfile);
            }
        }
    }
}

