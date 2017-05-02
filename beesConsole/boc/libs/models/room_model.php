<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Room_model extends MY_Model {
	protected $table = 'room';	

	//获取房间号
	public function get_title($where){
		if (!$where) {
			return FALSE;
		}
		$array=array();
		foreach ($where as $key => $value) {
			$data=$this->db->select('title')->where(array('id' => $value))->get($this->table)->row_array();
			if($data['title']){
				$array[]=$data['title'];
			}
		}
		return $array;
	}
	
	/**
	 * 删除
	 */
	public function delRoom($ids,$where=FALSE,$table=FALSE)
	{
		if (!$table) {
			$table = $this->table;
		}
		$this->db->delete($table, array('in' => array('id',$where)));
		return $this->db->affected_rows();
	}
	//获取房间信息 数据库中
	public function get_info($id){
	    return $this->db->select('*')->where(array('id'=>$id))->get($this->table)->row_array();
	}
	
	//获取所有信息
	public function get_all(){
	    return $this->db->select('*')->where(array('cid'=>2))->get($this->table)->result_array();
	}
}
