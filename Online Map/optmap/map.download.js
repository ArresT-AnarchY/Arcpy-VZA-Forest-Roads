    function saveToFile(content, filename) {
      var file = filename + '.geojson';
      saveAs(new File([JSON.stringify(content)], file, {
        type: "text/plain;charset=utf-8"
      }), file);
    }

L.easyButton( '<i class="fa fa-download" title="Katmanları indirin" aria-hidden="true"></i>', function(){
  var fg = map.pm.getGeomanLayers(true); // or getGeomanLayers()
  saveToFile(fg.toGeoJSON(), 'Webmap_CbsDestek_Com');
  alert('GEOJSON dosyası az sonra bilgisayarınıza indirilecektir.');
}).addTo(map);