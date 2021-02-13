<?php
//hemi %3A00%0A
$type = $_GET['type'];

require_once __DIR__.'/vendor/autoload.php';
$token='AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA';
$disk = new Arhitector\Yandex\Disk($token);

$date_power = date('Y-m-d');
$date_aurora = gmdate('Y-m-d-H:i');

function isexists($disk,$path){
    $resource = $disk->getResource($path);
$result = null;
if($resource->has()){
    $result=1;
} else{
    $result=0;
}
return $result;
}


$resource = '';
if($type=='power'){
$name_power = 'a_pow_'.$date_power;
$file = 'disk:/Aurora-forecast/Power/2020/'.$name_power.'
.txt';
$resource = $disk->getResource($file);
}

else{
    $date_aurora = gmdate('Y-m-d-H:i');
    $date = substr($date_aurora,0,10);
    $year = substr($date,0,4);
    $path='disk:/Aurora-forecast/Map/'.$year.'/'.$date.'/'.'a_map_';
    
//
if($date < '2020-10-29')
{
  $test = isexists($disk,'disk:/Aurora-forecast/Map/'.$year.'/'.$date.'/');
  
    if($test != 0)
    {
    $hour=substr($date_aurora,11,2);
    $min=substr($date_aurora,14,2);
    $time= $hour.':'.$min;
    //echo $time; echo "<br/>";
    
    $wholedate=$date.'-'.$time;
    //echo $wholedate; echo "<br/>";
    
    if($min < 5){
        $min = substr($min,0,1).'0';
    }else{
        $min = substr($min,0,1).'5';
    }
    $time= $hour.':'.$min;
    $wholedate=$date.'-'.$time;
    //echo $wholedate; echo "<br/>";
    
    $path_corr = $path.$wholedate.'
.txt';
$check = isexists($disk,$path_corr);


if($check == 0){
    $exists = 0;//isexists($disk,$path);
    while($exists<1){
        $wholedate = gmdate("Y-m-d-H:i", strtotime("-5 minutes", strtotime($wholedate)));
 $path_test = $path.$wholedate.'
.txt';  
//echo $path_test;echo "<br/>";
        $exists = isexists($disk,$path_test);
        break;
       
    }    

     $path_corr =  $path_test;
}
else{
    
}

#$resource = $disk->getResource($path_corr);   
$existsw = isexists($disk,$path_corr);
echo $existsw;
if($existsw>0){
    $resource = $disk->getResource($path_corr); 
    
}
else{
    $resource = $disk->getResource('https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt');   
}
    }
    else{
        $resource = $disk->getResource('https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt');   
    }

//
}
else {
    //$resource = $disk->getResource('https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt'); 
    $hour=substr($date_aurora,11,2);
    $min=substr($date_aurora,14,2);
    $time= $hour.':'.$min;
   // echo $time; echo "<br/>";
    $min_dec = substr($min,0,1);
    $min_dig = substr($min,1,1);
   // echo $min_dig;
    
    $wholedate=$date.'-'.$time;
    
    $path_corr = $path.$wholedate.'
    .txt';
   // echo $path_corr;
    $check = isexists($disk,$path_corr);
   // echo $path_corr;
    if($check == 0){
        $arr1 = array();
        echo $min_dec;
        for($i = 0; $i < 10; $i++)
        {
            $wholedate1=$date.'-'.$hour.':'.$min_dec.$i;
            $testpath = $path.$wholedate1.'.txt';
          //  echo $testpath; echo "<br/>";
         //   echo isexists($disk,$testpath); echo "<br/>";
            if(isexists($disk,$testpath) == 1){
                array_push($arr1,$i);
            }
            else{
                echo $path.$wholedate1.'.txt';echo "<br/>";
                //echo $date.'-'.$hour.':'.$min_dec;

            }
        }
        for($i = $min_dig+1; $i < 10; $i++)
        {
            $wholedate1=$date.'-'.$hour.':'.$min_dec.$i;
            $testpath = $path.$wholedate1.'.txt';
            //echo $testpath; echo "<br/>";
           // echo isexists($disk,$testpath); echo "<br/>";
            if(isexists($disk,$testpath) == 1){
                array_push($arr1,$i);
            }
        }
        $arr2 = array();
        for($i=0;$i<count($arr1);$i++){
            array_push($arr2,abs($arr1[$i]-$min_dig));
        }
        
        $index = 0;
        for($i=1;$i<count($arr2);$i++){
            if($arr2[$i] < $arr2[$i-1]){
                $index = $i;
            }
        }
        $wholedate2=$date.'-'.$hour.':'.$min_dec.$arr1[$index];
        $testpath2 = $path.$wholedate2.'.txt';
        //echo implode($arr1);
        $resource = $disk->getResource($testpath2); 
    }
    
    
}
}


if($resource->has()){
    echo "ok";
    if ( ! $resource->isPublish())
    {
      $resource->setPublish(true);
    }
    $t = $resource->public_url;
    
    
    $fp = fopen('php://memory', 'r+b');
    
    $resource->download($fp);
    
    fseek($fp, 0);
    
          $contents = array();
          $txt ='';
          $u = 0;
          while ($line = trim(fgets($fp))) {
              if(strpos($line, '#')===false)
              {
//$line = $line.'x';
             array_push($contents,$line);              
              }
    
          }
    //echo count($contents);
    
    if($type=='power'){
    $yy = json_encode($contents);
    }
    else{
   // $yy = implode($contents,'');
    $yy = implode($contents,PHP_EOL);
        
    }
    echo $yy;
}
else{

    echo 'none';
}









?>