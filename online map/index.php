<!DOCTYPE html>
<html lang="tr">
<head>
<title>Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorunun Belirlenmesi</title>
	<link rel="icon" type="image/png" href="../dist/img/logo.svg"/>

    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
	<!---------------------------------------------------------------------------------------------->
	<!------------------------------------ JS Alanı ------------------------------------------------>
	<!---------------------------------------------------------------------------------------------->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <!-----<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>----->
	<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
  integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
  crossorigin=""></script>
	<script src="https://cdn.jsdelivr.net/npm/leaflet.locatecontrol/dist/L.Control.Locate.min.js" charset="utf-8"></script>
	<script src="https://unpkg.com/leaflet-geosearch/dist/geosearch.umd.js"></script>
	<script type="text/javascript" src="./js/position.js"></script>
	<script type="text/javascript" src="./js/leaflet-ajax.js"></script>
	<script type="text/javascript" src="./js/spin.js"></script>
	<script type="text/javascript" src="./js/leaflet.spin.js"></script>
	<script type="text/javascript" src="./js/leaflet-sidebar.js"></script>
	<script type="text/javascript" src="./js/leaflet-easybutton.js"></script>
	<script type="text/javascript" src="./js/leaflet-bing-layer.js"></script>
	<script type="text/javascript" src="./js/label/Leaflet.label.js"></script>
	<script type="text/javascript" src="./js/label/Leaflet.label.js"></script>
	<script src="./js/label/BaseMarkerMethods.js"></script>
	<script src="./js/label/Marker.Label.js"></script>
	<script src="./js/label/CircleMarker.Label.js"></script>
	<script src="./js/label/Path.Label.js"></script>
	<script src="./js/label/Map.Label.js"></script>
	<script src="./js/label/FeatureGroup.Label.js"></script>
	<link rel="stylesheet" href="./css/leaflet-search.css" />
	<script src="./js/leaflet-search.js"></script>
	<link rel="stylesheet" href="./css/MarkerCluster.css" />
	<link rel="stylesheet" href="./css/MarkerCluster.Default.css" />
	<script src="./js/leaflet.markercluster-src.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js"></script>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css">
	<!---------------------------------------------------------------------------------------------->
	<!------------------------------------ CSS Alanı ----------------------------------------------->
	<!---------------------------------------------------------------------------------------------->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
  integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
  crossorigin=""/>  
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet.locatecontrol/dist/L.Control.Locate.min.css" />
	<link rel="stylesheet" href="https://unpkg.com/leaflet-geosearch@3.2.1/dist/geosearch.css" />
    <link rel="stylesheet" href="./css/leaflet-sidebar.min.css" />
    <link rel="stylesheet" href="css/style.css" />
    <link rel="stylesheet" href="./css/leaflet-easybutton.css" rel="stylesheet"/>
<link rel="stylesheet" href="https://ppete2.github.io/Leaflet.PolylineMeasure/Leaflet.PolylineMeasure.css" />
<script src="https://ppete2.github.io/Leaflet.PolylineMeasure/Leaflet.PolylineMeasure.js"></script>
<style>
.selectie {
  padding: 6px 6px;
  display: none;
  font: 12px Arial, Helvetica, sans-serif roboto;
  background: white;
  background: rgba(255, 255, 255, 0.8);
  /*box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);*/
  /*border-radius: 5px;*/
  line-height: 24px;
  color: #555;
}
.legend {
  padding: 6px 8px;
  font: 14px Arial, Helvetica, sans-serif;
  background: white;
  background: rgba(255, 255, 255, 0.8);
  /*box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);*/
  /*border-radius: 5px;*/
  line-height: 24px;
  color: #555;
}
.legend h4 {
  text-align: center;
  font-size: 16px;
  margin: 2px 12px 8px;
  color: #777;
}

.legend span {
  position: relative;
  bottom: 3px;
}

.legend i {
  width: 18px;
  height: 18px;
  float: left;
  margin: 0 8px 0 0;
  opacity: 0.7;
}

.legend i.icon {
  background-size: 18px;
  background-color: rgba(255, 255, 255, 1);
}
</style>
</head>
<body>
    <div id="sidebar" class="sidebar collapsed">
        <!-- Nav tabs -->
        <div class="sidebar-tabs">
            <ul role="tablist">
                <li><a href="#home" role="tab" title="Bilgilendirme"><i class="fa fa-bars"></i></a></li>
                <li><a href="#profile" role="tab" title="Bilgi Sistemi"><i class="fa fa-info"></i></a></li>
                <li><a href="https://www.tahayasin.com" title="Coder Web Page!" role="tab" target="_blank"><i class="fa fa-university"></i></a></li>
            </ul>

            <ul role="tablist">
				<li><a href="" class="logout" title="Çıkış"><i class="fa fa-sign-out"></i></a></li>
            </ul>
        </div>

        <!-- Tab panes -->
        <div class="sidebar-content">
            <div class="sidebar-pane" id="home">
                <h1 class="sidebar-header">
                    Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorunun Belirlenmesi
                    <span class="sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>

                <div style="text-align: justify;"><p>Merhaba! </p>
				
				<p>Bu çalışmada, orman yolları ile orman varlığı arasındaki ilişki ve sistematik bir ağ olan orman yollarının birbirleri ile olan ilişkileri incelenmiştir. Kamu kaynakları kullanılarak planlanan ve inşa edilen orman yollarının farklı girdi ve farklı çıktılar kullanılarak Veri Zarflama Analizi ile etkinliklerinin ölçülmesi amaçlanmıştır. Bu planlama ve yapım sürecinin etkin ve verimli olarak kullanımı hedeflenmektedir. Bu etkinlik skorlarının değerlendirilmesi ile mevcut orman yollarının daha sağlıklı hale getirilmesi konusunda çalışmalar güncel tutulacaktır. Ayrıca, plancılar için kılavuz niteliğinde bir paket program ortaya konarak, programlama tabanlı olarak GIS aplikasyonları için Python programlama ile program modülü oluşturulmuştur. <a href="https://github.com/ArresT-AnarchY">github</a> </p>
				<p>Orman yolları, 292 sayılı Orman Yolları Planlaması, Yapımı ve Bakımı tebliğinde yer alan teknik ve geometrik standartlara göre planlanmakta ve yapılmaktadır. Odun üretimi fonksiyonuna bağlı olarak planlanan ve inşa edilen orman yolları, bu çalışma sonucunda farklı orman fonksiyonlarına göre değerlendirilebilecektir. Kamu kaynaklarının daha tutarlı kullanımının önünü açabilecek öncü bir model olacaktır.
</p>
				
				<p>Bu sistem <a href="http://tahayasin.com">Arş. Gör. Taha Yasin HATAY </a> tarafından kodlanmıştır. Orman yollarının ekolojik, ekonomik, sosyal ve teknik fonksiyon senaryolarına göre, belirli değişkenlere göre veri zarflama analizi yardımıyla etkinlik skorları belirlenmiştir. Detaylı bilgi için; <a href="https://github.com/ArresT-AnarchY">github</a> üzerinden python ve arcgis tabanlı veri zarflama analizine ulaşabilirsiniz.</p></div>

            </div>

            <div class="sidebar-pane" id="profile">
                <h1 class="sidebar-header">Bilgi Sistemi<span class="sidebar-close"><i class="fa fa-caret-left"></i></span></h1>
				        <div class="msg"><br><br>Merhaba! <b></b><br><br>Bu alan orman yollarının etkinlik değerleri, mevcut değerleri ve projeksiyon değerlerinin sunulduğu sekmedir. Orman yolunun üzerine tıkladığınızda <b>"Etkinlik Değerlerine Bak!"</b> yazısına tıklayın. Bilgi sistemi açılacaktır.</div>
            </div>
        </div>
    </div>
    <div id="map" class="sidebar-map"></div>

	<script type="text/javascript" src="./optmap/map.ana.js"></script>
	<script type="text/javascript" src="./optmap/map.sidebar.opt.js"></script>
	<script type="text/javascript" src="./optmap/map.profil.layer.js"></script>
	<script type="text/javascript" src="./optmap/map.location-search-mouse.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>

<script>
$(document).ready(function(e){
	$(".logout").click(function(e){
		var url = "index.php";
		var data = { logout : "logout"}
		$.post(url, data)
});
});
$(".year").datepicker({
    format: "yyyy",
    viewMode: "years", 
    minViewMode: "years",
}).on('changeDate', function(e){
    $(this).datepicker('hide');
	$('#dmprogram').show();
}).attr("autocomplete", "off");
</script>
</body>
</html>