   // konumu bul
   lc = L.control.locate({
       strings: {
           title: "Yerimi Bul!"
       }
   }).addTo(map);
   
   // yer arama
   const search = new GeoSearch.GeoSearchControl({
       provider: new GeoSearch.OpenStreetMapProvider(),
       style: 'bar',
       showMarker: true, // optional: true|false  - default true
       showPopup: true, // optional: true|false  - default false
       marker: {
           // optional: L.Marker    - default L.Icon.Default
           icon: new L.Icon.Default(),
           draggable: false,
       },
       popupFormat: ({
           query,
           result
       }) => result.label, // optional: function    - default returns result label,
       resultFormat: ({
           result
       }) => result.label, // optional: function    - default returns result label
       maxMarkers: 1, // optional: number      - default 1
       retainZoomLevel: false, // optional: true|false  - default false
       animateZoom: true, // optional: true|false  - default true
       autoClose: false, // optional: true|false  - default false
       searchLabel: 'Aradığınız yeri yazabilirsiniz!', // optional: string      - default 'Enter address'
       keepResult: false, // optional: true|false  - default false
       updateMap: true, // optional: true|false  - default true
   });
   map.addControl(search);
   
   //mouse yeri
   L.control.mousePosition().addTo(map);