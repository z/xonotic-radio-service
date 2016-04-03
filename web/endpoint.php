<?php
$target = $_GET['t'];
$config = parse_ini_file("sample.ini");
$endpoints = $config['endpoints'];
if ( array_key_exists($endpoints[$target] ) {
    $endpoint_file = $endpoints[$target];
} else {
    $endpoint_file = $endpoints['default'];
}
header("Content-Type: text/plain");
$contents = file($endpoint_file);
$line = $contents[rand(0, count($contents) - 1)];
echo $line;
?>
