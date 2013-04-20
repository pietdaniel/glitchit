<?php

class Index extends CI_Controller {
	public function __construct() {
		parent::__construct();

	}
	public function index() {
		$this->load->helper('file');

		$data['title'] = "Glitchi it";

		$data['files']=get_filenames('./uploads');

		$this->load->view('templates/header', $data);
		$this->load->view('upload_view',array('error' => ''));
		$this->load->view('images',$data);	

	}

	public function display() {

		$this->load->view('templates/header');


	}


}