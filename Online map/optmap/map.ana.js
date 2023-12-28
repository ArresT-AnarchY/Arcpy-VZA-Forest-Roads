// map kısmı
   var map = L.map('map').setView([40.75764, 39.60709], 11);
   mapLink =
       '<a href="https://openstreetmap.org">OpenStreetMap</a>';
   L.tileLayer(
       'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                           attribution:
                    'Karadeniz Teknik Üniversitesi- Arş. Gör. Taha Yasin HATAY - <font color="red">Bu Harita 122O785 Nolu TÜBİTAK Projesi kapsamında hazırlanmıştır.</font>',
				minZoom: 1,
				maxZoom: 18,
				noWrap: true
       }).addTo(map);
	   
	
    var BING_KEY = 'Anyhm1rOlnyjJRAqCE0wCuJjHgBy96dprOuS5hZyI7Zgv_K60K1_YylvCbVPs09f'
    var bingLayer = L.tileLayer.bing(BING_KEY).addTo(map)