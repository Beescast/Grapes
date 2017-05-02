<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');
/**
 * Class Recruit extends CI_Model
 * @author yincast
 */
class Recruit_model extends MY_Model
{
    protected $table = 'recruit';

	public function get_list($limit=15,$start=0,$order=false,$where=false,$fields="*"){
		$this->db
			->select($fields)
			->from($this->table)
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
			if ($this->db->field_exists('sort_id',$this->table)) {
				$this->db->order_by('sort_id','desc');
			}elseif ($this->db->field_exists('timeline',$this->table)) {
				$this->db->order_by('timeline','desc');
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
		$query = $this->db->get();
		return $query->result_array();
	}
}
