# Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorunun Belirlenmesi
Bu çalışma, 122O785 kodlu TÜBİTAK projesinin katkılarıyla hazırlanmıştır.

Bu çalışmada, orman yolları ile orman varlığı arasındaki ilişki ve sistematik bir ağ olan orman yollarının birbirleri ile olan ilişkileri incelenmiştir. Kamu kaynakları kullanılarak planlanan ve inşa edilen orman yollarının farklı girdi ve farklı çıktılar kullanılarak Veri Zarflama Analizi ile etkinliklerinin ölçülmesi amaçlanmıştır. Bu planlama ve yapım sürecinin etkin ve verimli olarak kullanımı hedeflenmektedir. Bu etkinlik skorlarının değerlendirilmesi ile mevcut orman yollarının daha sağlıklı hale getirilmesi konusunda çalışmalar güncel tutulacaktır. Ayrıca, plancılar için kılavuz niteliğinde bir paket program ortaya konarak, programlama tabanlı olarak GIS aplikasyonları için Python programlama ile program modülü oluşturulmuştur.

Orman yolları, 292 sayılı Orman Yolları Planlaması, Yapımı ve Bakımı tebliğinde yer alan teknik ve geometrik standartlara göre planlanmakta ve yapılmaktadır. Odun üretimi fonksiyonuna bağlı olarak planlanan ve inşa edilen orman yolları, bu çalışma sonucunda farklı orman fonksiyonlarına göre değerlendirilebilecektir. Kamu kaynaklarının daha tutarlı kullanımının önünü açabilecek öncü bir model olacaktır.

# Dosyaların tasarımı
İçerikte bulunan dosyaların tanıtımı:

**Arcpy GIS model:** Bu dosya içerisinde ArcMap için kullanılabilecek dosyalar bulunmaktadır.

**Online Map:** Bu dosya içerisinde çalışma kapsamında Online harita dosyaları bulunmaktadır.

**Sample data:** Bu dosya içerisinde örnek veriler bulunmaktadır.  


# Kurulum nasıl yapılmalıdır?
Bu sistem Arcmap10.8 ile test edilmiştir.

1. Arcpy GIS model dosyası içerisinde herhangi bir senaryo verilerine giriş yapılır.
2. Arcmap açılır.
3. ArcCatalog içerisinden .tbx uzantılı dosya açılır. 
4. Kurulum gerektiren modüller ilk ve son modüllerdir. Bu nedenle, İlk veya son modüle sağ tıklanır ve properties seçilir. Çıkan ekranda "script file" kısmında dosyalarda bulunan .py uzantılı kod betiği seçilir. "Arcpy GIS model" klasöründe uygun senaryonun içerisinde bulunan aynı isimli ".py uzantılı kod betiği" seçilir.

Örnek:
![Screenshot of Module](https://tahayasin.com/VZA_DEA/kurulum.jpg)

5. Ardından B sekmesinden başlamak üzere, tüm girdi ve çıktı değişkenlerinin hesaplama kısmı için modüller çalıştırılır.
6. En son aşamada yeniden script file tanımlaması yapılır ve direkt veri zarflama analizine geçilir.

# Ekolojik senaryo değişkenler

| **DEĞİŞKEN**                                            | **GİRDİ/ÇIKTI** |
| ------------------------------------------------------- | --------------- |
|Yol uzunluğu|Girdi|
|Yolun akarsu yataklarını kesme sıklığı/sayısı-oranı|Girdi|
|Sanat yapısı sayısı ve uygunluğu|Girdi|
|Bakı|Girdi|
|Yolun geçtiği yamaç eğimi|Girdi|
|Yolun eğimi|Girdi|
|Yol genişliği|Girdi|
|Kazı şevi yüksekliği|Girdi|
|İşletmeye açılan alan|Girdi|
|Yol boyunca gözlenen şev akıntı ve heyelanlı alan sayısı|Girdi|
|Doğa Koruma|Çıktı|
|Yolun bağlantı sağladığı alanlar|Çıktı|     

# Ekonomik senaryo değişkenler

| **DEĞİŞKEN**                                            | **GİRDİ/ÇIKTI** |
| ------------------------------------------------------- | --------------- |
| Yolun Bakısı                                            | Girdi           |
| Yamaç eğimi                                             | Girdi           |
| Yol sanat yapılarının yapılmış olması                   | Girdi           |
| İnşaat alanı genişliği                                  | Girdi           |
| Kıvrımlılık faktörü                                     | Girdi           |
| Dolambaçlılık faktörü                                   | Girdi           |
| Yatay kurpların yoğunluğu                               | Girdi           |
| Yol yüzeyindeki deformasyonlar                          | Girdi           |
| Yol uzunluğu ve işletmeye açılan alan ((İAA/YU\*500 m)) | Çıktı           |
| Ekonomik fonksiyonlu ormandan geçen orman yolları       | Çıktı           |

# Sosyal senaryo değişkenler

| **DEĞİŞKEN**                                            | **Girdi/Çıktı** |
| ------------------------------------------------------- | --------------- |
| Yol uzunluğu                                            | Girdi           |
| Yolun düz ve kurplu yapı kompozisyonu (dolambaçlılık)   | Girdi           |
| İnşaat alanı genişliği ve kayıp orman alanı             | Girdi           |
| Yol Eğimi                                               | Girdi           |
| Estetik amaçlı yol koruma ormanına geçme                | Çıktı           |
| Ziraat ve mera alanlarına ulaşım                        | Çıktı           |
| Kazı şevlerinin yeşillenmiş (vejetasyonla kaplı) olması | Çıktı           |
| Çevresindeki köylerin nüfus miktarı                     | Çıktı           |


# Teknik senaryo değişkenler

| **DEĞİŞKEN**                                | **Girdi/Çıktı** |
| ------------------------------------------- | --------------- |
| Yol Eğimi                                   | Girdi           |
| Heyelan ve göçükler                         | Girdi           |
| Yolun Bakısı                                | Girdi           |
| Platform genişliği                          | Girdi           |
| Banket genişliği                            | Girdi           |
| Hendek genişliği                            | Girdi           |
| Ağaçların yol platformuna (yatay) yakınlığı | Girdi           |
| Karşılaşma ve Duraklama yeri                | Çıktı           |
| Sanat yapıları                              | Çıktı           |
| Yolun bağlantı sağladığı bölmeler           | Çıktı           |
| İşletmeye açtığı meşcere alanı              | Çıktı           |
| Taşınacak emval miktarı (292 sayılı tebliğ) | Çıktı           |


## Lisans

122O785 kodlu TÜBİTAK projesiyle desteklenmiştir. Tüm yazılım, girdiler ve çıktılar lisanslıdır.

  
## Kullanılan Teknolojiler

**Program:** ArcGIS, ArcMap, ArcCatalog, Spyder

**Language:** Python, ArcPy

  
## Kullananlar

Bu proje ile aşağıdaki grupların kullanması hedeflenmiştir

- Orman Mühendisleri
- Harita Mühendisleri
- Çevre Mühendisleri
- Şehir Bölge Planlama
- Maden Mühendisleri

.. profesyonel olarak arazi planlaması ve analizleri yapan tüm gruplar

  ## Destek

Konu hakkında bilgi almak için tyhatay@ktu.edu.tr adresine eposta atabilirsiniz.



