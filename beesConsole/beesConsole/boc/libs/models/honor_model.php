<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Honor_model extends MY_Model {
	protected $table = 'honor';	

	public function get_lists($limit=5,$start=0,$order=false,$where=false,$wherein=false,$fields="*",$table=FALSE){
		if (!$table) {
			$table = $this->table;
		}

		$this->db
			->select($fields)
			->from($table)
			->limit($limit,$start);
		if ($order) {
			if (is_array($order)) {
				foreach ($order as $k => $v){
					$this->db->order_by($k,$v);
				}
			}else if(is_string($order)){
				$this->db->order_by($order);
			}
		}else{
			if ($this->db->field_exists('sort_id',$table)) {
				$this->db->order_by('sort_id','desc');
			}else{
				$this->db->order_by('id','desc');
			}
		}
		if ($where) {
			if (is_string($where)) {
				$where = ' '.$where.' ';
			}elseif (is_array($where)) {
				$this->db->where($where);
			}
		}
		if ($wherein) {
			//echo $wherein;exit;
			$this->db->where_in('cid',$wherein);
		}
		$query = $this->db->get();
		return $query->result_array();
	}
}
