<?php
$target = $_GET['t'];
$config = parse_ini_file("config/config.ini", true);
$endpoints = $config['endpoints'];
if ( array_key_exists($target, $endpoints) ) {
    $endpoint_file = $endpoints[$target];
} else {
    $endpoint_file = $endpoints['default'];
}
header("Content-Type: text/plain");
$contents = file($endpoint_file);
$line = $contents[rand(0, count($contents) - 1)];
echo $line;
?>

