<?php
//hemi %3A00%0A
$type = $_GET['type'];
$dt = $_GET['dt'];

//$dt = '2021-01-02-12:17';
//$dt = '2020-08-05-00:50';
require_once __DIR__ . '/vendor/autoload.php';
$token = 'AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA';
$disk = new Arhitector\Yandex\Disk($token);
//2021-01-02-12:17
$date_power = date('Y-m-d');
$date_aurora = gmdate('Y-m-d-H:i');

function isexists($disk, $path)
{
    $resource = $disk->getResource($path);
    $result = null;
    if ($resource->has()) {
        $result = 1;
    } else {
        $result = 0;
    }
    return $result;
}


$resource = '';
if ($type == 'power') {
    $date_power = $dt;//gmdate('Y-m-d-H:i');
    $date_p = substr($date_power, 0, 10);
    $year = substr($date_p, 0, 4);
    $name_power = 'a_pow_' . $date_p;
    $file = 'disk:/Aurora-forecast/Power/' . $year . '/' . $name_power . '
.txt';
//echo $file;
    $resource = $disk->getResource($file);
} else {
    $date_aurora = $dt;//gmdate('Y-m-d-H:i');
    $date = substr($date_aurora, 0, 10);
    $year = substr($date, 0, 4);
    $path = 'disk:/Aurora-forecast/Map/' . $year . '/' . $date . '/' . 'a_map_';

//
    if ($date < '2020-10-29') {
        $test = isexists($disk, 'disk:/Aurora-forecast/Map/' . $year . '/' . $date . '/');

        if ($test != 0) {
            $hour = substr($date_aurora, 11, 2);
            $min = substr($date_aurora, 14, 2);
            $time = $hour . ':' . $min;
            //echo $time; echo "<br/>";

            $wholedate = $date . '-' . $time;
            //echo $wholedate; echo "<br/>";

            if ($min < 5) {
                $min = substr($min, 0, 1) . '0';
            } else {
                $min = substr($min, 0, 1) . '5';
            }
            $time = $hour . ':' . $min;
            $wholedate = $date . '-' . $time;
            //echo $wholedate; echo "<br/>";

            $path_corr = $path . $wholedate . '
.txt';
            $check = isexists($disk, $path_corr);


            if ($check == 0) {
                $exists = 0;//isexists($disk,$path);
                while ($exists < 1) {
                    $wholedate = gmdate("Y-m-d-H:i", strtotime("-5 minutes", strtotime($wholedate)));
                    $path_test = $path . $wholedate . '
.txt';
//echo $path_test;echo "<br/>";
                    $exists = isexists($disk, $path_test);
                    break;

                }

                $path_corr = $path_test;
            } else {

            }

#$resource = $disk->getResource($path_corr);   
            $existsw = isexists($disk, $path_corr);
//echo $existsw;
            if ($existsw > 0) {
                $resource = $disk->getResource($path_corr);

            } else {
                $resource = $disk->getResource('https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt');
            }
        } else {
            $resource = $disk->getResource('https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt');
        }

//
    } else {
        $path_corr = 'none';
        //  echo $path;
        //$resource = $disk->getResource('https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt');
        $hour = substr($date_aurora, 11, 2);
        //echo $date_aurora;
        $min = substr($date_aurora, 14, 2);
        $time = $hour . ':' . $min;
        // echo $time; echo "<br/>";
        $min_dec = substr($min, 0, 1);
        $min_dig = substr($min, 1, 1);
        // echo $min_dig;

        $wholedate = $date . '-' . $time;

        $path_corr = $path . $wholedate . '.txt';
        // echo $path_corr;
        $check = isexists($disk, $path_corr);

        //2021-01-02-09:13
        if ($check == 0) {

            $s = $date . ' ' . $time;
//echo $s; echo "<br/>";


            $time_check = strtotime($s);


            $midnight_0 = strtotime($date . ' ' . '00:00');
            $midnight_1 = strtotime($date . ' ' . '23:59');
            $path_togo = "";
            $try = 0;
            if ($time_check > $midnight_0) {
                while ($time_check > $midnight_0) {

                    $time_check = $time_check - (1 * 60);
                    $new_date = date('Y-m-d-H:i', $time_check);
                    $path_corr = $path . $new_date . '.txt';
                    // echo $path_corr; echo "<br/>";

                    $try = isexists($disk, $path_corr);
                    // echo $try; echo "<br/>";
                    if ($try != 0) {
                        break;
                    }
                }

            }
//echo $try;
            if ($try == 0) {

                $time_check = strtotime($s);
                if ($time_check < $midnight_1) {
                    while ($time_check < $midnight_1) {

                        $time_check = $time_check + (1 * 60);
                        $new_date = date('Y-m-d-H:i', $time_check);
                        $path_corr = $path . $new_date . '.txt';
                        //echo $path_corr; echo "<br/>";

                        $try = isexists($disk, $path_corr);
                        //echo $try; echo "<br/>";
                        if ($try != 0) {
                            break;
                        }
                    }
                }
            }
// echo $path_corr; 
            $resource = $disk->getResource($path_corr);
        } else {
            $resource = $disk->getResource($path_corr);
        }


    }
}


if ($resource->has()) {
    // echo "ok";
    if (!$resource->isPublish()) {
        $resource->setPublish(true);
    }
    $t = $resource->public_url;


    $fp = fopen('php://memory', 'r+b');

    $resource->download($fp);

    fseek($fp, 0);

    $contents = array();
    $txt = '';
    $u = 0;
    while ($line = trim(fgets($fp))) {
        if (strpos($line, '#') === false) {
//$line = $line.'x';
            array_push($contents, $line);
        }

    }
    //echo count($contents);

    if ($type == 'power') {
        $yy = json_encode($contents);
    } else {
        // $yy = implode($contents,'');
        $yy = implode($contents, PHP_EOL);

    }
    echo $yy;
} else {

    echo 'none';
}


?>