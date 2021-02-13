<?php
require_once __DIR__.'/vendor/autoload.php';
$token='AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA';
$disk = new Arhitector\Yandex\Disk($token);
$url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt';
    $lines = file($url);
    $new_line = $lines[3];
    $current_date = (string) substr($new_line,30,11);
    $year = (string) substr($current_date,0,4);
echo $current_date;
echo $year;
$file = 'disk:/Aurora-forecast/Power/'.$year.'/a_pow_'.$current_date.'.txt';
$resource = $disk->getResource($file);
if($resource->has()){
$resource->delete(true);
}
//$resource->delete(true);
$resource = $disk->getResource($file)->upload($url,true,true);    


?>