

<?php
shuffle($files);
foreach (array_reverse($files) as $f_item):
	if (strcmp($f_item,"multithread.py")!==0) {
		echo '<p><img src="./uploads/'.$f_item.'" style="width:300px;"></p>';
	}
endforeach

?>