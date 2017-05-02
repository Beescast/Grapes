<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class News_model extends MY_Model {

	protected $table = 'article';

	public function get_one($where, $fields = "*")
	{
		$this->db->select($fields)->from($this->table);
		if(!is_numeric($where))
		{
			$this->db->where($where);
		} else {
			$this->db->where('id',$where);
		}
		$query = $this->db->get();
		$row = $query->row_array();

		if($row)
		{
			$perv = $this->db->select('id,title')
							 ->from($this->table)
							 ->where(array('cid'=>$row['cid'],'audit'=>1,'sort_id >'=>$row['sort_id']))
							 ->order_by('sort_id','asc')
							 ->limit(1)->get()->row_array();

			if($perv)
			{
				$row['prev_id'] = $perv['id'];
				$row['prev_title'] = $perv['title'];
			}

			$next = $this->db->select('id,title')
							 ->from($this->table)
							 ->where(array('cid'=>$row['cid'],'audit'=>1,'sort_id <'=>$row['sort_id']))
							 ->order_by('sort_id','desc')
							 ->limit(1)->get()->row_array();

			if($next)
			{
				$row['next_id'] = $next['id'];
				$row['next_title'] = $next['title'];
			}
		}

		return $row;
	}

}