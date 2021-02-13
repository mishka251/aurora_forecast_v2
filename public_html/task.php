<?php
//hemi
require_once __DIR__.'/vendor/autoload.php';
$token='AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA';
$disk = new Arhitector\Yandex\Disk($token);
$url = 'https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt';
$lines = file($url);
$new_line = $lines[3];
$current_date = (string) substr($new_line,30,11);
$year = (string) substr($current_date,0,4);

$file = 'disk:/Aurora-forecast/Power/'.$year.'/a_pow_'.$current_date.'.txt';
$resource = $disk->getResource($file);
if($resource->has()){
    $resource->delete(true);
}
$resource = $disk->getResource($file)->upload($url,true,true);    
//aurora
$token='AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA';
$disk = new Arhitector\Yandex\Disk($token);

$url = 'https://services.swpc.noaa.gov/json/ovation_aurora_latest.json';
$string = file_get_contents($url);
$json=json_decode($string,true);
$fdate = $json['Forecast Time'];

$day =substr($fdate,0,10);
$time = substr($fdate,11,5);

$current_time = 'a_map_'.$day.'-'.$time;
$top = substr($fdate,0,4);
//echo $top;
$dir_path = 'disk:/Aurora-forecast/Map/'.$top;
$current_date=$day;
$dirContent=$disk->getResource($dir_path);
    if($dirContent->has()){
      //  echo "exists";
    }
    else{
        $dirContent->create();
    }

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

//$url = 'https://services.swpc.noaa.gov/json/ovation_aurora_latest.json';
//$string = file_get_contents($url);
//$json=json_decode($string,true);


/*
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
    
    $dir_path = 'disk:/Aurora-forecast/Map/'.$top;
    $dirContent=$disk->getResource($dir_path);
    if($dirContent->has()){
      //  echo "exists";
    }
    else{
        $dirContent->create();
    }
    
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
    

}*/
?>