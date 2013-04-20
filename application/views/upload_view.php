<?php echo $error;?>
<?php $this->load->helper('form','url'); ?>
<?php echo form_open_multipart('upload/do_upload');?>

<input type="file" name="userfile" size="20" />

<input type="submit" value="upload" />

</form>