<?php
session_start();
$adminmi = $_SESSION["login"]["type"];
if(time()-$_SESSION["login"]["time"] >3600 && $adminmi != "Admin")   //Sezon 60dk ( 3600sn ) sonra sonlanır.
{ 
	session_unset(); 
	session_destroy(); 
	echo "<script type='text/javascript'> document.location ='../index.php'; </script>";
}
if(!isset($_SESSION["login"]["username"])){
	echo "<script type='text/javascript'> document.location ='../index.php'; </script>";
exit(); }

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// DB credentials.
include('../../inc/db.php');

# Build SQL SELECT statement including x and y columns
$sql = 'SELECT isim,soyisim,tckimlik,email,mobil,meslek,myil,mprogram,fakulte,facebook,fbcheck, twcheck, twitter, lnkcheck, linkedin, instagram, inscheck, emcheck, mobilcheck, resimcheck, bolum, latInput AS y, lngInput AS x FROM user ORDER BY fakulte asc';
// $sql = 'SELECT *, latInput AS y, lngInput AS x FROM user';

# Try query or error
$rs = $dbh->query($sql);
if (!$rs) {
    echo 'An SQL error occured.\n';
    exit;
}

function replace_tr($text) {
   $text = trim($text);
   $search = array('Ç','ç','Ğ','ğ','ı','İ','Ö','ö','Ş','ş','Ü','ü');
   $replace = array('c','c','g','g','i','i','o','o','s','s','u','u');
   $new_text = str_replace($search,$replace,$text);
   return $new_text;
} 


# Build GeoJSON feature collection array
$geojson = array(
   'type'      => 'FeatureCollection',
   'features'  => array()
);

# Loop through rows to build feature arrays
while ($row = $rs->fetch(PDO::FETCH_ASSOC)) {
    $properties = $row;
    # Remove x and y fields from properties (optional)
    unset($properties['x']);
    unset($properties['y']);
	if (!empty($row['facebook']) && $row['fbcheck'] == 1 || $adminmi == "Admin" ) { $facebook = $row['facebook']; } else { $facebook = "[Gizli]"; }
	if (!empty($row['twitter']) && $row['twcheck'] == 1  || $adminmi == "Admin" ) { $twitter = $row['twitter']; } else { $twitter = "[Gizli]"; }
	if (!empty($row['linkedin']) && $row['lnkcheck'] == 1  || $adminmi == "Admin" ) { $linkedin = $row['linkedin']; } else { $linkedin = "[Gizli]"; }
	if (!empty($row['instagram']) && $row['inscheck'] == 1  || $adminmi == "Admin" ) { $instagram = $row['instagram']; } else { $instagram = "[Gizli]"; }
	if (!empty($row['email']) && $row['emcheck'] == 1  || $adminmi == "Admin" ) { $email = $row['email']; } else { $email = "[Gizli]"; }
	if (!empty($row['mobil']) && $row['mobilcheck'] == 1  || $adminmi == "Admin" ) { $mobil = $row['mobil']; } else { $mobil = "[Gizli]"; }
	$isim = $row['isim'];
	$tckisa = substr($row['tckimlik'], 0, 5);
	$isim= $isim." ".$row['soyisim'];
	$isim = replace_tr($isim);
	$isim = strtolower(preg_replace('/\s+/','',$isim));
    $resim =$isim.".".$tckisa;
	$resdir = realpath($_SERVER["DOCUMENT_ROOT"])."/mezun/";
    $resdir = $resdir."userimg/".$resim;
	if (!file_exists($resdir) && $row['resimcheck'] == 0) {
	$resim = "<center><img src='../userimg/nophoto.nopht' width='200px' height='200px' class='upload-preview'></center>"; }
		elseif ($adminmi== "Admin" || $row['resimcheck'] == 1 ) {
			$resim = "<center><img src='../userimg/$resim' width='200px' height='200px' class='upload-preview'></center>";} 			
else {
$resim = "<center><img src='../userimg/nophoto.nopht' width='200px' height='200px' class='upload-preview'></center>";
}
	unset($properties['password']);	
    $feature = array(
        'type' => 'Feature',
        'geometry' => array(
            'type' => 'Point',
            'coordinates' => array(
                $row['x'],
                $row['y']
            )
        ), 
        'properties' => array(
				'isim'=> $row['isim'],
				'soyisim' => $row['soyisim'],
				'email' => $email,
                'mobil' => $mobil,
				'meslek' => $row['meslek'],
                'myil' => $row['myil'],
				'mprogram' => $row['mprogram'],
				'fakulte' => $row['fakulte'],
				'bolum' => $row['bolum'],
				'facebook' => $facebook,
				'twitter' => $twitter,
				'linkedin' => $linkedin,
				'instagram'=> $instagram,
				'resim' => $resim
				)
    );
    # Add feature arrays to feature collection array
    array_push($geojson['features'], $feature);
}

header('Content-type: application/json');
echo json_encode($geojson, JSON_NUMERIC_CHECK);
$dbh = NULL;
?>