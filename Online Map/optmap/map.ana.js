// map kısmı
   var map = L.map('map').setView([39.26625, 34.87061], 6);
   mapLink =
       '<a href="https://openstreetmap.org">OpenStreetMap</a>';
   L.tileLayer(
       'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                           attribution:
                    'CBSDestek.Com',
				minZoom: 1,
				maxZoom: 18,
				noWrap: true
       }).addTo(map);
  
	
    var BING_KEY = 'Anyhm1rOlnyjJRAqCE0wCuJjHgBy96dprOuS5hZyI7Zgv_K60K1_YylvCbVPs09f'
    var bingLayer = L.tileLayer.bing(BING_KEY).addTo(map)

        var center = [40, 0];

        // Define some base layers
        var osm = L.tileLayer(
            '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            {attribution: '© OpenStreetMap contributors'}
        );

        var otopomap = L.tileLayer(
            '//{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
            {attribution: '© OpenStreetMap contributors. OpenTopoMap.org'}
        );

        // The tree containing the layers
        var baseTree = [
            {
                label: 'OpenStreeMap',
                children: [
                    {label: 'OSM', layer: osm, name: 'OpenStreeMap'},
                    {label: 'OpenTopoMap', layer: otopomap, name: 'Topographic - OSM'},
                ]
            },
            {
                label: 'BingMap',
                children: [
                    {label: 'Bingmap', layer: bingLayer, name: 'Bingmap'},
                ]
            }
        ];

        L.control.layers.tree(baseTree).addTo(map);