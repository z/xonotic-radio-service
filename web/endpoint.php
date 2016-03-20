<?php
header("Content-Type: text/plain");
$contents = file("endpoint_list.txt"); 
$line = $contents[rand(0, count($contents) - 1)];
echo $line;
?>
