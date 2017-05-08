<?php
if (! defined('BASEPATH'))
    exit('No direct script access allowed');

/**
 * Class Article extends CI_Controller
 *
 * @author 信息类
 */
class Room extends Modules_Controller
{

    function __construct()
    {
        parent::__construct();
    }

    protected $rules = array(
        "create" => array(
            array(
                'field' => 'title',
                'label' => '房间号',
                'rules' => 'trim|required|numeric|callback_rid2_check'
            ),
            array(
                "field" => "timeline",
                "label" => '时间',
                "rules" => "trim|strtotime|required"
            ),
            // array(
            // "field" => "AccountNumber",
            // "label" => '帐号数量',
            // "rules" => "trim|numeric|required|callback_AccountNumber_check"
            // ),
            array(
                "field" => "ACC0",
                "label" => ACC0,
                "rules" => "trim|numeric|required|callback_ACC0_check"
            ),
            array(
                "field" => "ACC1",
                "label" => ACC1,
                "rules" => "trim|numeric|required|callback_ACC1_check"
            ),
            array(
                "field" => "ACC2",
                "label" => ACC2,
                "rules" => "trim|numeric|required|callback_ACC2_check"
            ),
            array(
                "field" => "ACC3",
                "label" => ACC3,
                "rules" => "trim|numeric|required|callback_ACC3_check"
            ),
            array(
                "field" => "LoginInterval",
                "label" => '帐号登录间隔',
                "rules" => "trim|numeric|required|callback_LoginInterval_check"
            ),
            array(
                "field" => "SpeechInterval",
                "label" => '同帐号说话间隔',
                "rules" => "trim|numeric|required|callback_SpeechInterval_check"
            )
        ),
        "edit" => array(
            array(
                'field' => 'title',
                'label' => '房间号',
                'rules' => 'trim|required|numeric'
            ),
            array(
                "field" => "timeline",
                "label" => '时间',
                "rules" => "trim|strtotime|required"
            ),
            array(
                "field" => "ACC0",
                "label" => ACC0,
                "rules" => "trim|numeric|required|callback_ACC0_check"
            ),
            array(
                "field" => "ACC1",
                "label" => ACC1,
                "rules" => "trim|numeric|required|callback_ACC1_check"
            ),
            array(
                "field" => "ACC2",
                "label" => ACC2,
                "rules" => "trim|numeric|required|callback_ACC2_check"
            ),
            array(
                "field" => "ACC3",
                "label" => ACC3,
                "rules" => "trim|numeric|required|callback_ACC3_check"
            ),
            array(
                "field" => "LoginInterval",
                "label" => '帐号登录间隔',
                "rules" => "trim|numeric|required|callback_LoginInterval_check"
            ),
            array(
                "field" => "SpeechInterval",
                "label" => '同帐号说话间隔',
                "rules" => "trim|numeric|required|callback_SpeechInterval_check"
            )
        )
        
    );
    // a0检查
    public function ACC0_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['ACC0'] > $this->session->userdata('ACC0')) {
            return false;
        } else {
            return true;
        }
    }
    // a1检查
    public function ACC1_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['ACC1'] > $this->session->userdata('ACC1')) {
            return false;
        } else {
            return true;
        }
    }
    // a2检查
    public function ACC2_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['ACC2'] > $this->session->userdata('ACC2')) {
            return false;
        } else {
            return true;
        }
    }
    // a3检查
    public function ACC3_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['ACC3'] > $this->session->userdata('ACC3')) {
            return false;
        } else {
            return true;
        }
    }
    
    // 判断房间号是否存在
    public function rid2_check()
    {
        $form = $this->input->post(NULL, TRUE);
        $noCount = $this->db->where(array(
            'title' => $form['title']
        ))
            ->from('room')
            ->count_all_results();
        
        if ($noCount > 0) {
            return false;
        } else {
            return true;
        }
    }
    // 帐户数量检查
    public function AccountNumber_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['AccountNumber'] <= 0) {
            return false;
        } else {
            return true;
        }
    }
    // 登录间隔检查
    public function LoginInterval_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['LoginInterval'] <= 0) {
            return false;
        } else {
            return true;
        }
    }
    // 说话间隔检查
    public function SpeechInterval_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['SpeechInterval'] < 5) {
            return false;
        } else {
            return true;
        }
    }
    // 重复弹幕次数
    public function RepeatBarrage_check()
    {
        $form = $this->input->post(NULL, TRUE);
        
        if ($form['RepeatBarrage'] <= 0) {
            return false;
        } else {
            return true;
        }
    }

    public function copypro()
    {
        $ids = $this->input->post('ids');
        
        $rs = $this->model->get_one($ids);
        
        unset($rs['id']);
        unset($rs['sort_id']);
        unset($rs['timeline']);
        
        $id = $this->model->create($rs);
        if ($id) {
            $vdata['msg'] = '复制成功，请刷新查看';
            $vdata['status'] = 1;
        } else {
            $vdata['msg'] = '复制失败，请刷新后重试';
            $vdata['status'] = 0;
        }
        $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
    }

    /**
     * @brief 处理创建信息
     */
    protected function _create()
    {
        $data = $this->_create_data();
        
        $url = addroom_url($data['title']);
        
        $get_data = curl_request($url);
        
        
        
        // v($data);exit;
        
        // if ($data['cid'] == 2) {
        // $data['audit'] = 1;
        // } else {
        // $data['audit'] = 0;
        // }
        
        if ($data['audit'] == 1) {
            $send_audit = 0;
        } else {
            $send_audit = 1;
        }
        
        if ($get_data != 'Successful operation') {
            $vdata['msg'] = $get_data;
            $vdata['status'] = 0;
            
            
        } else {
            
            $url = setroom_url($data['title'],'', $data['LoginInterval'], $send_audit, $data['SpeechInterval'], $data['ACC0'], $data['ACC1'], $data['ACC2'], $data['ACC3']);
            
            $get_data = curl_request($url);
            
            if ($get_data != 'Successful operation') {
                $vdata['msg'] = $get_data;
                $vdata['status'] = 0;
            } else {
                
                // 获取主播名字 nickname
                $room_data = $this->getRoomStatusFromDouYu($data['title']);
                
                if (isset($room_data['data']['owner_name'])) {
                    $data['nickname'] = $room_data['data']['owner_name'];
                } else {
                    $data['nickname'] = '';
                }
                
                if ($insert_id = $this->model->create($data)) {
                    $data['id'] = $insert_id;
                    $this->_create_after($data);
                    $vdata['msg'] = '成功添加了一条内容';
                    $vdata['status'] = 1;
                    $vdata['id'] = $insert_id;
                    $this->mlogs->add('create', '添加数据id:' . $insert_id);
                } else {
                    $vdata['msg'] = '没有添加成功!';
                    $vdata['status'] = 0;
                }
            }
        }
        
        if ($this->input->is_ajax_request()) {
            $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
        } else {
            if ($this->input->get('back_url')) {
                $vdata['back_url'] = $this->input->get('back_url');
            }
            $this->load->view('msg', $vdata);
        }
    }

    /**
     * @brief 删除
     *
     * @param $key 键值
     *            默认id
     * @return
     *
     *
     *
     *
     *
     *
     *
     *
     */
    public function delete($key = FALSE)
    {
        if (! $key and $this->input->get('ids')) {
            $key = explode(',', $this->input->get('ids'));
        } else {
            $vdata = array(
                'status' => 0,
                'msg' => "ID不存在"
            );
        }
        $id = $this->input->get('ids');
        
        // 加载model
        $this->load->model('room_model', 'room');
        
        $room_title = $this->room->get_title($key);
        
        if ($room_title) {
            foreach ($room_title as $value) {
                $url = delroom_url($value);
                $get_data = curl_request($url);
            }
        }
        
        if (1 == 2) {
            $vdata['msg'] = $get_data;
            $vdata['status'] = 0;
        } else {
            if (! isset($vdata['status'])) {
                $this->_rm_file($key);
                if ($this->model->del($key)) {
                    $vdata = array(
                        'status' => 1,
                        'msg' => "成功的删除数据！"
                    );
                    if (is_array($key)) {
                        $this->mlogs->add('delete', '删除数据id:' . $this->input->get('ids'));
                    } else {
                        $this->mlogs->add('delete', '删除数据id:' . $key);
                    }
                } else {
                    $vdata = array(
                        'status' => 0,
                        'msg' => "出错了，检查下选择的是否正确"
                    );
                }
            }
        }
        
        if (is_ajax()) {
            $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
        } else {
            $this->load->view('msg', $vdata);
        }
    }

    /**
     * @brief 处理编辑信息
     */
    protected function _edit()
    {
        $data = $this->_edit_data();
        
        $vdata['id'] = $data['id'];
        
        if ($data['audit'] == 1) {
            $send_audit = 0;
        } else {
            $send_audit = 1;
        }
        
        $url = setroom_url($data['title'],'', $data['LoginInterval'], $send_audit, $data['SpeechInterval'], $data['ACC0'], $data['ACC1'], $data['ACC2'], $data['ACC3']);
        
        $get_data = curl_request($url);
        
        if ($get_data != 'Successful operation') {
            $vdata['msg'] = $get_data;
            $vdata['status'] = 0;
        } else {
            
            if ($this->model->update($data, 'id = ' . $data['id'])) {
                $this->_edit_after($data);
                $vdata['msg'] = '已经成功修改了信息！';
                $vdata['status'] = 1;
                $this->mlogs->add('update', '更新数据id:' . $data['id']);
            } else {
                $vdata['msg'] = '没有做任何的改动';
                $vdata['status'] = 0;
            }
        }
        if ($this->input->is_ajax_request()) {
            $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
        } else {
            $this->load->view('msg', $vdata);
        }
    }

    /**
     * @发送信息ajax
     */
    protected function SendMsg()
    {
        $data = $this->input->post(null, true);
        
        if ($data['content'] == '') {
            $vdata['msg'] = '请输入信息内容';
            $vdata['status'] = 0;
            exit(json_encode($vdata));
        }
        if ($data['RepeatBarrage'] == '') {
            $vdata['msg'] = '请输入重复弹幕次数';
            $vdata['status'] = 0;
            exit(json_encode($vdata));
        }
        if ($data['RepeatBarrage'] < 1) {
            $vdata['msg'] = '重复弹幕次数不能小于1';
            $vdata['status'] = 0;
            exit(json_encode($vdata));
        }
        
        $this->model->update($data, 'id = ' . $data['id']);
        
        $vdata['msg'] = '信息发送成功';
        $vdata['status'] = 1;
        exit(json_encode($vdata));
    }
    
    // 审核 POST (对于开关类型字段，拷贝审核修改相应的audit字段即可使用)
    public function audit($key = FALSE)
    {
        if (! $key and $this->input->post('ids')) {
            $key = explode(',', $this->input->post('ids'));
        } else {
            $vdata = array(
                'status' => 0,
                'msg' => lang('modules_no_id')
            );
        }
        
        $where = FALSE;
        
        if ($this->input->get('c')) {
            $where = array(
                'cid' => $this->input->get('c')
            );
        } else {
            $vdata = array(
                'status' => 0,
                'msg' => lang('modules_no_col_id')
            );
        }
        
        $audit = $this->input->post('audit');
        
        if ($audit) {
            $audit = 1;
        } else {
            $audit = 0;
        }
        $msg = array(
            '关闭成功',
            '启动成功'
        );
        
        if (! isset($vdata['status'])) {
            if ($where) {
                $res = $this->model->audit($audit, $key, $where);
            } else {
                $res = $this->model->audit($audit, $key);
            }
            
            if ($res) {
                
                // 修改cid
                // $this->model->roomId($audit, $key);
                
                // 加载model
                $this->load->model('room_model', 'room');
                if ($key) {
                    foreach ($key as $value) {
                        // 获取房间在数据库中参数
                        $data = $this->room->get_info($value);
                        
                        if ($data['audit'] == 1) {
                            $send_audit = 0;
                        } else {
                            $send_audit = 1;
                        }
                        
                        $url = setroom_url($data['title'],'', $data['LoginInterval'], $send_audit, $data['SpeechInterval'], $data['ACC0'], $data['ACC1'], $data['ACC2'], $data['ACC3']);
                        $get_data = curl_request($url);
                    }
                }
                
                $vdata = array(
                    'status' => 1,
                    'msg' => $msg[$audit]
                );
                if (is_array($key)) {
                    $this->mlogs->add('audit', lang('modules_audit_id') . $this->input->post('ids') . lang('modules_audit_for') . $audit);
                } else {
                    $this->mlogs->add('audit', lang('modules_audit_id') . $key . lang('modules_audit_for') . $audit);
                }
            } else {
                $vdata = array(
                    'status' => 0,
                    'msg' => lang('modules_audit_err_select')
                );
            }
        }
        
        if ($this->input->is_ajax_request()) {
            $this->output->set_content_type('application/json')->set_output(json_encode($vdata));
        } else {
            $this->load->view('msg', $vdata);
        }
    }
    
    // 搜索
    public function search($cid = false, $page = 1)
    {
        $vdata['cpath'] = $this->mcol->get_path_more($this->cid);
        $vdata['cchildren'] = $this->mcol->get_cols($this->cid);
        $title = $this->mcol->get_one($this->cid, "title");
        $vdata['title'] = $title['title'];
        $limit = $this->page_limit;
        $this->input->get('limit', TRUE) and is_numeric($this->input->get('limit')) and $limit = $this->input->get('limit');
        $order = $this->input->get('order', TRUE) ? $this->input->get('order', TRUE) : FALSE;
        $order = 'id asc';
        $where = array();
        $where['cid'] = $this->cid;
        if ($wh = $this->_search_where()) {
            $where = array_merge($where, $wh);
        }
        
        // 房间号
        if ($this->input->get('title')) {
            $where = array_merge($where, array(
                'title like' => '%' . $this->input->get('title', TRUE) . '%'
            ));
        }
        // 房间号
        if ($this->input->get('audit') == 0) {
            $where = array_merge($where, array(
                'audit' => 0
            ));
        }
        if ($this->input->get('audit') == 1) {
            $where = array_merge($where, array(
                'audit' => $this->input->get('audit', TRUE)
            ));
        }
        
        $vdata['pages'] = $this->_pages(site_url($this->class . '/search/' . $this->cid . '/'), $limit, $where, 4);
        $vdata['list'] = $this->model->get_list($limit, $limit * ($page - 1), $order, $where);
        $this->_display($vdata, $this->class . '_index.php');
    }

    /**
     * @发送信息ajax
     */
    protected function getRoomInfo()
    {
        $data = $this->input->post(null, true);
        
        $url = roominfo_url($data['rid']);
        
        $get_data = curl_request($url);
        
        exit(json_encode($get_data));
    }

    function getRoomStatusFromDouYu($rid)
    {
        $room_data = curl_request('http://open.douyucdn.cn/api/RoomApi/room/' . $rid);
        $room_data = object2array(json_decode($room_data));
        return $room_data;
    }

    public function getTypes()
    {
        $data = $this->input->post(null, true);
        $url = ctypeinfo_url($data['rid']);
        $get_data = curl_request($url);
        $get_data = object2array(json_decode($get_data));
        
        if ($get_data) {
            foreach ($get_data as $key => $value) {
                $this->session->set_userdata('ACC' . $key, $value); // 设置
            }
        }
        exit(json_encode($get_data));
    }
}
