   // konumu bul
   lc = L.control.locate({
       strings: {
           title: "Yerimi Bul!"
       }
   }).addTo(map);
   
   //mouse yeri
   L.control.mousePosition().addTo(map);