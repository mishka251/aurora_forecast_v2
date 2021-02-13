<?php
require_once __DIR__.'/vendor/autoload.php';
require_once __DIR__.'/vendor/autoload.php';
$token='AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA';
$disk = new Arhitector\Yandex\Disk($token);
$url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt';
$file_name = basename($url);
repeat($url, $file_name, $disk);

function repeat($url, $file_name, $disk){

    $lines = file($url);
    $new_line = $lines[3];
    $current_date = (string) substr($new_line,24,10);
    $top = substr($current_date,0,4);
    $current_time = 'a_map_'.$current_date.'-'.substr($new_line,35);
    
    rename($file_name,$current_time.'.txt');
    
    $dir_path = 'disk:/Aurora-forecast/Map/'.$top.'/'.$current_date;
    $dirContent=$disk->getResource($dir_path);
    if($dirContent->has()){
      //  echo "exists";
    }
    else{
        $dirContent->create();
    }
    if(!($disk->getResource($dir_path.'/'.$current_time.'.txt')->has())){
    $disk->getResource($dir_path.'/'.$current_time.'.txt')->upload($url,true);    
    }
    

}
?>