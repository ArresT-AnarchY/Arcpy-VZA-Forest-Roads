// Loader
(function() {

L.Control.Loader = L.Control.extend({
	onAdd: function(map) {
		this._map = map;
		this._container = L.DomUtil.create('div','leaflet-control-loader');
		this.hide();
		return this._container;
	},
	addTo: function (map) {
		this._container = this.onAdd(map);
		map.getContainer().appendChild(this._container);
		return this;
	},
	show: function() {
		this._container.style.display = 'block';
		return this;
	},
	hide: function() {
		this._container.style.display = 'none';
		return this;		
	}
});

L.Map.addInitHook(function () {
    if (this.options.loaderControl) {
        this.loaderControl = L.control.loader(this.options.loaderControl);
        this.addControl(this.loaderControl);
    }
});

L.control.loader = function (options) {
    return new L.Control.Loader(options);
};

}).call(this);
   
var controlLoader = L.control.loader().addTo(map);
	
	map.on('dragend',function() {
		controlLoader.show();
		setTimeout(function() {
			controlLoader.hide();
		},3000);
	});   
// End of Loader


// dış sınır  //

var sinirstyle = {
    "color": "#FFC0CB",
    "weight": 5,
    "opacity": 1,
	"fillOpacity": 0.1
};

var SınırLayer = L.geoJson(false, {
    style: sinirstyle,
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/macka_sinir.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		SınırLayer.addData(response).addTo(map);
    }
});



var etkinstyle = {
    "color": "#B0E0E6",
    "weight": 3,
    "opacity": 0.65
};

var notetkinstyle = {
    "color": "#ff0000",
    "weight": 3,
    "opacity": 0.65
};

function style(feature) {
    return {
        fillColor: '#E31A1C',
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// Ekolojik Etkin Yollar //

var EkoloEtkinLayer = L.geoJson(false, {
    style: etkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='green' >(ETKİN) &#x2714;</font></b><br></center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/ekolo1.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		EkoloEtkinLayer.addData(response).addTo(map);
		cluster.addLayer(EkoloEtkinLayer).addTo(map);
    }
});

// Ekolojik Etkin Olmayan Yollar //

var NotEkoloEtkinLayer = L.geoJson(false, {
    style: notetkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='red'>(ETKİN DEĞİL) &#33; &#33; &#33;	</font><br><br>Referans Aldığı Yollar<br> </b>"+ feature.properties.referans +"</center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/ekolo0.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		NotEkoloEtkinLayer.addData(response).addTo(map);
		cluster.addLayer(NotEkoloEtkinLayer);
    }
});

// Ekonomik Etkin Yollar //


var EkonoEtkinLayer = L.geoJson(false, {
    style: etkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='green' >(ETKİN) &#x2714;</font></b><br></center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/ekono1.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		EkonoEtkinLayer.addData(response);
    }
});

// Ekonomik Etkin Olmayan Yollar //

var NotEkonoEtkinLayer = L.geoJson(false, {
    style: notetkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='red'>(ETKİN DEĞİL) &#33; &#33; &#33;	</font><br><br>Referans Aldığı Yollar<br> </b>"+ feature.properties.referans +"</center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/ekono0.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		NotEkonoEtkinLayer.addData(response);
    }
});

// Sosyal Etkin Yollar //

var SosyoEtkinLayer = L.geoJson(false, {
    style: etkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='green' >(ETKİN) &#x2714;</font></b><br></center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/sosyal1.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		SosyoEtkinLayer.addData(response);
    }
});


// Sosyal Etkin Olmayan Yollar //

var NotSosyoEtkinLayer = L.geoJson(false, {
    style: notetkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='red'>(ETKİN DEĞİL) &#33; &#33; &#33;	</font><br><br>Referans Aldığı Yollar<br> </b>"+ feature.properties.referans +"</center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/sosyal0.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		NotSosyoEtkinLayer.addData(response);
    }
});


// Teknik Etkin Yollar //

var TeknikEtkinLayer = L.geoJson(false, {
    style: etkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='green' >(ETKİN) &#x2714;</font></b><br></center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/teknik1.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		TeknikEtkinLayer.addData(response);
    }
});

// Teknik Etkin Olmayan Yollar //

var NotTeknikEtkinLayer = L.geoJson(false, {
    style: notetkinstyle,
    onEachFeature: function (feature, layer) {
        var popupText = "<br><center><b>"+ feature.properties.Name +" <font color='red'>(ETKİN DEĞİL) &#33; &#33; &#33;	</font><br><br>Referans Aldığı Yollar<br> </b>"+ feature.properties.referans +"</center><br>" + feature.properties.description + "";
   
               layer.bindPopup($('<a href="#" class="prfgor"><b>'+ feature.properties.Name +'<br \><center><small>Etkinlik Değerlerine Bak!</small></center><b></a>').click(function() {
                   $(document).ready(function() {
                       $('.msg').html('' + popupText + '');
                   });
                   sidebar.open('profile');
               })[0]);
			   layer.bindTooltip(feature.properties.Name.toString(), { permanent: true });
    }
});



		var cluster = L.markerClusterGroup();  
$.ajax({
    type: "POST",
    url: './data/teknik0.geojson',
    dataType: 'json',
	beforeSend : function() { map.spin(true)},
    success: function (response) {
		map.spin(false);
		NotTeknikEtkinLayer.addData(response);
    }
});

// layer control 

  var baseLayers = {
    "Open Street Map" : map,
	"Bing Aeriel Map" : bingLayer
  };
  
  var overlays = {
    "Maçka OİŞ Sınırı" : SınırLayer,
	"Ekolojik Etkin Orman Yolları" : EkoloEtkinLayer,
	"Ekolojik Etkin Olmayan Yolları" : NotEkoloEtkinLayer,
    "Ekonomik Etkin Orman Yolları" : EkonoEtkinLayer,
    "Ekonomik Etkin Olmayan Orman Yolları" : NotEkonoEtkinLayer,
    "Sosyal Etkin Orman Yolları" : SosyoEtkinLayer,
    "Sosyal Etkin Olmayan Orman Yolları" : NotSosyoEtkinLayer,
    "Teknik Etkin Orman Yolları" : TeknikEtkinLayer,
    "Teknik Etkin Olmayan Orman Yolları" : NotTeknikEtkinLayer
  };

  L.control.layers(baseLayers, overlays, {collapsed:true}).addTo(map);
  
/*Legend specific*/
var legend = L.control({ position: "bottomright" });

legend.onAdd = function(map) {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML += "<h4>Lejant</h4>";
  div.innerHTML += '<i style="background: #B0E0E6"></i><span>Etkin Orman Yolları</span><br>';
  div.innerHTML += '<i style="background: #FF0000"></i><span>Etkin Olmayan Orman Yolları</span><br>';
  div.innerHTML += '<i style="background: #FFC0CB"></i><span>Maçka OİŞ Sınırı</span><br>';
  //div.innerHTML += '<i class="icon" style="background-image: url(https://d30y9cdsu7xlg0.cloudfront.net/png/194515-200.png);background-repeat: no-repeat;"></i><span>Grænse</span><br>';
  
  

  return div;
};

legend.addTo(map);


// measure

            L.control.scale ({maxWidth:240, metric:true, imperial:false, position: 'bottomleft'}).addTo (map);
            let polylineMeasure = L.control.polylineMeasure ({position:'topleft', unit:'kilometres', showBearings:true, clearMeasurementsOnStop: false, showClearControl: true, showUnitControl: true})
            polylineMeasure.addTo (map);

            function debugevent(e) { console.debug(e.type, e, polylineMeasure._currentLine) }

            map.on('polylinemeasure:toggle', debugevent);
            map.on('polylinemeasure:start', debugevent);
            map.on('polylinemeasure:resume', debugevent);
            map.on('polylinemeasure:finish', debugevent);
            map.on('polylinemeasure:change', debugevent);
            map.on('polylinemeasure:clear', debugevent);
            map.on('polylinemeasure:add', debugevent);
            map.on('polylinemeasure:insert', debugevent);
            map.on('polylinemeasure:move', debugevent);
            map.on('polylinemeasure:remove', debugevent);