<?php if ( ! defined('BASEPATH')) exit('No direct script access allowed');

class Upload extends CI_Controller {
		function __construct() {
			parent::__construct();
			$this->load->helper('form','url');
		}

		function index() {
			$this->load->view('templates/header.php');
			$this->load->view('upload_view',array('error' => ''));
		}

		function runScript($file) {
  			$command = "python /var/www/glitchit/uploads/multithread.py " . $file;
			  $pid = popen( $command,"r");
			  while( !feof( $pid ) ) {
			  	echo fread($pid, 256);
			  	flush();
			  	ob_flush();
			  	usleep(100000);
			  }
			  pclose($pid);
		}

		function do_upload() {

			$config['upload_path']='./uploads/';
			$config['allowed_types']='jpg|png';
			$config['max_size']=200;


			$this->load->library('upload',$config);

			if (!$this->upload->do_upload()) {
				$error = array('error' => $this->upload->display_errors());
				$this->load->view('templates/header.php','FAIL');
				$this->load->view('upload_view', $error);
			}else {
				$data = array('upload_data' => $this->upload->data());
				$data['title']='success';

				$filename=$data['upload_data']['file_name'];

				$this->runscript($filename);
				
				$this->load->view('templates/header.php',$data);
				$this->load->view('upload_success', $data);
			}

		}
}

?>