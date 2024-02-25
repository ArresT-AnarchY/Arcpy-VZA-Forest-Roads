#-*coding:mbcs*-#
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorlarının Belirlenmesi (Tübitak 1002 - Proje No. 122O785)
#  @author: Arş. Gör. Taha Yasin HATAY (ArresT)
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import arcpy
import os
import sys
import numpy as np
from scipy.optimize import fmin_slsqp
import pandas as pd

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

##########################################################################################################
#Girişler
##########################################################################################################
Workspace = arcpy.GetParameterAsText(0)
Sosyal_Etkinlik_Tablosu = arcpy.GetParameterAsText(1)
yol_name = arcpy.GetParameterAsText(2)
input_name = arcpy.GetParameterAsText(3)
if input_name == '#' or not input_name:
    input_name = "Yol_Egimi, Yol_Uzunluk, Dolambac_Faktor, Kayip_Orman, Kazi_Yesil"
output_name = arcpy.GetParameterAsText(4)
if output_name == '#' or not output_name:
    output_name = "Hizmet_Suresi, MAHALLE_NUFUS, Ziraat_Mera_iskan"

##########################################################################################################
#Çıkışlar
##########################################################################################################
ALL_Layer = arcpy.GetParameterAsText(5)
etkinlik_matrisi_Layer = arcpy.GetParameterAsText(6)
normalize_tablo_Layer = arcpy.GetParameterAsText(7)
korelasyon_table_Layer = arcpy.GetParameterAsText(8)
Sosyal_Etkinlik_Analiz_Layer = arcpy.GetParameterAsText(9)
Sosyal_Etkinlik_Target_Etkin_Layer = arcpy.GetParameterAsText(10)
Sosyal_Etkinlik_Target_Etkin_Olmayan_Layer = arcpy.GetParameterAsText(11)

##########################################################################################################
# Analize girecek veriler için normalize veri tablosunun açılması
##########################################################################################################
arcpy.TableToTable_conversion(Sosyal_Etkinlik_Tablosu, Workspace, "Normalize_Veri_Tablosu", "", "", "")
normalize_tablo = Workspace + r"\\Normalize_Veri_Tablosu"
arcpy.TableToTable_conversion(Sosyal_Etkinlik_Tablosu, Workspace, "girdi_cikti_verileri", "", "", "")
girdi_cikti_verileri = Workspace + r"\\girdi_cikti_verileri"

##########################################################################################################
# 1 km orman yollarına göre ayarlanacak verilerin yol uzunluğuna bölünerek, 1 km (1000 m) ile çarpılması
##########################################################################################################
# carpim_listesi = ["MAHALLE_NUFUS", "Estetik_Orman", "Ziraat_Mera_iskan"]
# existing_fields = [field.name for field in arcpy.ListFields(normalize_tablo)]
# fields_to_process = [field for field in carpim_listesi if field in existing_fields]
# if not fields_to_process:
    # arcpy.AddError("Belirtilen sütunlar tabloda bulunamadı.")
    # sys.exit(1)
    
# with arcpy.da.UpdateCursor(normalize_tablo, fields_to_process + ["VZA_uzunluk"]) as cursor:
    # for row in cursor:
        # for i in range(len(fields_to_process)):
            # row[i] = row[i] * 1000 / row[-1] if row[-1] != 0 else 0
        # cursor.updateRow(row)
        
##########################################################################################################
#normalize min max değerleri
##########################################################################################################
alanlar_min_max = {
    "Yol_Egimi": {"min": 0, "max": 15},
    "Yol_Uzunluk": {"min": 0, "max": 20000},
    "Dolambac_Faktor": {"min": 1, "max": 5},
    "Kayip_Orman": {"min": 0, "max": 100},
    "Hizmet_Suresi": {"min": 0, "max": 365},
    "Kazi_Yesil": {"min": 0, "max": 100},
    "MAHALLE_NUFUS": {"min": 0, "max": 5000},
    "Estetik_Orman": {"min": 0, "max": 100},
    "Ziraat_Mera_iskan": {"min": 0, "max": 100},
}

##########################################################################################################
# Normalizasyon yapmak için belirtilen min-max değerlerini kullanarak normalize etme
##########################################################################################################
with arcpy.da.UpdateCursor(normalize_tablo, list(alanlar_min_max.keys())) as cursor:
    for row in cursor:
        for i, alan in enumerate(list(alanlar_min_max.keys())):
            min_value = alanlar_min_max[alan]["min"]
            max_value = alanlar_min_max[alan]["max"]
            normalized_value = 0.00001+(row[i] - min_value) / (max_value - min_value)
            row[i] = normalized_value
        cursor.updateRow(list(row))


##########################################################################################################
# Bir korelasyon yapalım ve bakalım değerlerimizin arasında nasıl bir bağlantı var?
##########################################################################################################
alan_isimleri = [field.name for field in arcpy.ListFields(normalize_tablo)]
korelasyondata = [row for row in arcpy.da.SearchCursor(normalize_tablo, alan_isimleri)]
korelasyon_verileri = pd.DataFrame(korelasyondata, columns=alan_isimleri)
del korelasyon_verileri['OBJECTID']
del korelasyon_verileri['Shape_Length']
del korelasyon_verileri['VZA_uzunluk']
korelasyon_matrisi = korelasyon_verileri.corr()

csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
korelasyon_matrisi.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "Korelasyon_Matrisi")
arcpy.Delete_management(csv_path1)
korelasyon_table_path = Workspace + r"\\Korelasyon_Matrisi"
arcpy.management.AlterField(korelasyon_table_path, "Field1", "Degiskenler", "Degiskenler")

##########################################################################################################
# Girdi ve çıktı sütunlarının input ve output olarak ayarlanması
########################################################################################################## 
input_fields = input_name.split(', ')
output_fields = output_name.split(', ')
names_field = yol_name

#sayı olarak kontrol
input_count = len(input_fields)
output_count = len(output_fields)

fields = arcpy.ListFields(normalize_tablo)
field_names = [field.name for field in fields]

for field in input_fields + output_fields:
    if field not in field_names:
        arcpy.AddError("Minimize Target Field ve Maximize Target Field ile Feature Tablosu uyum saglamiyor")
        sys.exit()

# Girdi ve çıktı verileri için numpy tanımlanması
X = np.empty((0, len(input_fields)), float)
y = np.empty((0, len(output_fields)), float)
names = []

# Tablodan girdi ve çıktı değerleri numpy verisi
with arcpy.da.SearchCursor(normalize_tablo, input_fields + output_fields + [names_field]) as cursor:
    for row in cursor:
        X = np.append(X, [np.array([row[i] for i in range(len(input_fields))])], axis=0)
        y = np.append(y, [np.array([row[i] for i in range(len(input_fields), len(input_fields) + len(output_fields))])], axis=0)
        names.append(row[-1])

#Dataframe
xy = np.hstack((X, y))
data = pd.DataFrame(xy, index=names, columns=input_fields+output_fields)

#Dataframe içerisinde 0 değer olamaz. Bunlar 0.1 olmalı.
if (data == 0).any().any() or data.isnull().any().any():
    arcpy.AddError("Hata: Verilerinizde 0 degeri bulunmaktadir. Lutfen Arazide toplanan verileri ve hesaplanan verileri kontrol ediniz!")
    sys.exit(1) 

##########################################################################################################
# Veri zarflama analizi (VZA) (DEA) yapılması için class ın oluşturulması
##########################################################################################################
class DEA(object):
    def __init__(self, inputs, outputs):
    # DEA classı için hazırlık yapalım. giriş ve çıkışlar ile başlatacağız.
        self.inputs = inputs
        self.outputs = outputs
        self.n = inputs.shape[0]
        self.m = inputs.shape[1]
        self.r = outputs.shape[1]
        self.unit_ = range(self.n)
        self.input_ = range(self.m)
        self.output_ = range(self.r)
        self.output_w = np.zeros((self.r, 1), dtype=np.float)
        self.input_w = np.zeros((self.m, 1), dtype=np.float)
        self.lambdas = np.zeros((self.n, 1), dtype=np.float)
        self.efficiency = np.zeros_like(self.lambdas)
        self.names = []
    
    def __efficiency(self, unit):
    # gelen her veri için etkinlik hesabı yapılmalı.
        denominator = np.dot(self.inputs, self.input_w)
        numerator = np.dot(self.outputs, self.output_w)
        return (numerator/denominator)[unit]
    
    def __target(self, x, unit):
    # Bu bir optimizasyon problemi olduğu için hedefimizi bilmeliyiz.
        in_w, out_w, lambdas = x[:self.m], x[self.m:(self.m+self.r)], x[(self.m+self.r):]
        denominator = np.dot(self.inputs[unit], in_w)
        numerator = np.dot(self.outputs[unit], out_w)
        return numerator/denominator
    
    def __constraints(self, x, unit):
    # kısıtlamalar...
        in_w, out_w, lambdas = x[:self.m], x[self.m:(self.m+self.r)], x[(self.m+self.r):]
        constr = []
        for input in self.input_:
            t = self.__target(x, unit)
            lhs = np.dot(self.inputs[:, input], lambdas)
            cons = t*self.inputs[unit, input] - lhs
            constr.append(cons)
        for output in self.output_:
            lhs = np.dot(self.outputs[:, output], lambdas)
            cons = lhs - self.outputs[unit, output]
            constr.append(cons)
        for u in self.unit_:
            constr.append(lambdas[u])
        return np.array(constr)
    
    def __optimize(self):
    # her birim için ayrıca optimizasyon
        d0 = self.m + self.r + self.n
        self.caniniyedigim=[]
        for unit in self.unit_:
            x0 = np.random.rand(d0) - 0.5
            x0 = fmin_slsqp(self.__target, x0, f_ieqcons=self.__constraints, args=(unit,))
            self.input_w, self.output_w, self.lambdas = x0[:self.m], x0[self.m:(self.m+self.r)], x0[(self.m+self.r):]
            self.efficiency[unit] = self.__efficiency(unit)
            self.lambdas[np.where(self.lambdas <= 0.001)[0]] = 0            
            self.caniniyedigim.append(self.lambdas)
        self.caniniyedigim = np.array(self.caniniyedigim)

        self.caniniyedigim = pd.DataFrame(self.caniniyedigim,columns=names,index=names)
    
    def name_units(self, names):
    # birimlerin isimleri
        assert(self.n == len(names))
        self.names = names
    
    def fit(self):
    # DEA sonuçlanması..
        self.__optimize()
        arcpy.AddWarning("Her Yol Biriminde Sosyal Etkinlik Skorlari:\n")
        arcpy.AddWarning("------------------------------------------------------------------------")
        for n, eff in enumerate(self.efficiency):
            if len(self.names) > 0:
                name = "Birim kod: %s" % self.names[n]
            else:
                name = "Birim kod: %d" % (n+1)
            arcpy.AddMessage("%s Sosyal Etkinlik Skoru: %.4f" % (name, eff))
        arcpy.AddWarning("------------------------------------------------------------------------")
if __name__ == "__main__":
    # İstenen eff sınırı
    hedef_eff_siniri = 1.2

    while True:
        dea = DEA(X,y)
        dea.name_units(names)
        dea.fit()
        
        # Ne olmadı mı??? Yeniden dene.. (Eğer eff değeri hedef_eff_siniri'nden küçükse veya sıfırdan büyükse döngüyü sonlandır)
        if all((dea.efficiency >= 0) & (dea.efficiency <= hedef_eff_siniri)):
            break
            
    # senin ben canını yerim ;) 
    caniniyedigim = dea.caniniyedigim
    etkinlik_matrisi = caniniyedigim.copy()
    etkinlik_matrisi['Score'] = dea.efficiency

##########################################################################################################
# Etkinlik matrisi oluşturma
##########################################################################################################
csv_path = arcpy.env.scratchGDB + "\\buff.csv"
etkinlik_matrisi.to_csv(csv_path, index=True)
arcpy.TableToTable_conversion(csv_path, Workspace, "Etkinlik_Matrisi")
arcpy.Delete_management(csv_path)
old_field = "Field1"
etkinlik_table_path = Workspace + r"\\Etkinlik_Matrisi"
arcpy.AlterField_management(etkinlik_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Etkinlik matrisinin girdi verileri ile çarpılması işlemi
##########################################################################################################
birlestirme_df = pd.DataFrame()
for i in range(len(caniniyedigim)):
    mask = (caniniyedigim.iloc[[i]] > 0) & (caniniyedigim.iloc[[i]] < 5)
    col_indices = caniniyedigim.columns[mask.iloc[0]]
    result_df = data.loc[col_indices, :]
    mask_df = caniniyedigim.iloc[[i], :].loc[:, mask.iloc[0]]
    mask_df = mask_df.T
    maskindex = mask_df.columns[0]
    result_df.index = result_df.index.astype(str)
    mask_df.index = mask_df.index.astype(str)
    merged_df = pd.concat([result_df, mask_df], axis=1)
    merged_df.iloc[:, :-1] = merged_df.iloc[:, :-1].multiply(merged_df.iloc[:, -1], axis=0)
    merged_df_sum = pd.DataFrame(merged_df.iloc[:, :-1].sum(axis=0)).T
    merged_df_sum.index = [maskindex]
    birlestirme_df = pd.concat([birlestirme_df, merged_df_sum], axis=0)

##########################################################################################################
# Data Denormalize, bu kısım VZA'ya giren verilerin yeniden denormalizasyonu ile ilgilidir.
##########################################################################################################
data_denormalize = data.copy()
for col in data.columns:
    original_col = col
    if original_col in alanlar_min_max:
        min_value = alanlar_min_max[original_col]['min']
        max_value = alanlar_min_max[original_col]['max']
        data_denormalize[col] = data[col] * (max_value - min_value) + min_value - 0.00001

field = ['VZA_uzunluk']
uzunluk = [row[0] for row in arcpy.da.SearchCursor(Sosyal_Etkinlik_Tablosu, field)]

uzunluk_frame = pd.DataFrame(uzunluk, columns=field)
data_denormalize['VZA_uzunluk'] = uzunluk_frame['VZA_uzunluk'].values

# for col in carpim_listesi:
    # data_denormalize[col] = data_denormalize[col] * data_denormalize["VZA_uzunluk"] / 1000

##########################################################################################################
# Hedef verilerinin oluşturulması, Bu aşamada hedef verilerin denormalizasyonu ve 1 km'lik değerler yerine,
# gerçek değerlere dönüştürülmesi işlemi yapılmaktadır.
##########################################################################################################
hedef_denormalize = birlestirme_df.copy()
for col in birlestirme_df.columns:
    original_col = col
    if original_col in alanlar_min_max:
        min_value = alanlar_min_max[original_col]['min']
        max_value = alanlar_min_max[original_col]['max']
        hedef_denormalize[col] = birlestirme_df[col] * (max_value - min_value) + min_value - 0.00001

#Denormalizasyon değerlerinin kullanıcıya gösterimi
arcpy.AddWarning("Yol_Egimi normalizasyon degeri            - Min= 0 - Max= 15      - (%)")
arcpy.AddWarning("Yol_Uzunluk normalizasyon degeri          - Min= 0 - Max= 20000   - birim= (m)")
arcpy.AddWarning("Dolambac_Faktor normalizasyon degeri      - Min= 1 - Max= 5       - birim= birimsiz ")
arcpy.AddWarning("Kayip_Orman normalizasyon degeri          - Min= 0 - Max= 100     - birim= (ha) ")
arcpy.AddWarning("Hizmet_Suresi normalizasyon degeri        - Min= 0 - Max= 365     - birim= (gün)")
arcpy.AddWarning("MAHALLE_NUFUS normalizasyon degeri        - Min= 0 - Max= 5000    - birim= (kişi)")
arcpy.AddWarning("Estetik_Orman normalizasyon degeri        - Min= 0 - Max= 100     - birim= (ha)")
arcpy.AddWarning("Ziraat_Mera_iskan normalizasyon degeri    - Min= 0 - Max= 100     - birim= (ha)")
arcpy.AddWarning("------------------------------------------------------------------------")

# 1 km'lik yoldan gerçek değerlere dönüşüm..
field = ['VZA_uzunluk']
uzunluk = [row[0] for row in arcpy.da.SearchCursor(Sosyal_Etkinlik_Tablosu, field)]

uzunluk_frame = pd.DataFrame(uzunluk, columns=field)
hedef_denormalize['VZA_uzunluk'] = uzunluk_frame['VZA_uzunluk'].values

# for col in carpim_listesi:
     # hedef_denormalize[col] = hedef_denormalize[col] * hedef_denormalize["VZA_uzunluk"] / 1000

#skor hedef değerlere eklenmeli
hedef_denormalize['Score'] = etkinlik_matrisi['Score'].values
hedef_denormalize['Score'] = hedef_denormalize['Score'].round(3)
    
degisim = hedef_denormalize.copy()
col1 = degisim.columns.copy()
degisim.columns = ['HEDEF_' + str(col) for col in degisim.columns]
degisim.rename(columns={'HEDEF_Score': 'Score'}, inplace=True)

if "VZA_uzunluk" in hedef_denormalize.columns:
    del hedef_denormalize["VZA_uzunluk"]
if "VZA_uzunluk" in data_denormalize.columns:
    del data_denormalize["VZA_uzunluk"]

csv_path2 = arcpy.env.scratchGDB + "\\buff2.csv"
degisim.to_csv(csv_path2, index=True)
arcpy.TableToTable_conversion(csv_path2, Workspace, "hedefler")
arcpy.Delete_management(csv_path2)
old_field = "Field1"
target_table_path = Workspace + r"\\hedefler"
arcpy.AlterField_management(target_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Değişim oranlarının hesaplanması.. gerçek değerler ile hedef değerler arasındaki oransal değişim göz önüne
# alınır. böylece değişim oranları ortaya konar.
##########################################################################################################
degisim_oranlari = pd.DataFrame()
for col in data_denormalize.columns:
    for row in data_denormalize.index:
        oran = round((((hedef_denormalize.loc[row, col] - data_denormalize.loc[row, col]) / data_denormalize.loc[row, col]) * 100),2)
        degisim_oranlari.loc[row, col] = oran     

degisim_oranlari.columns = ['PROJEKSIYON_' + str(col1[i]) for i in range(degisim_oranlari.shape[1])]
degisim_oranlari[degisim_oranlari.abs() < 0.001] = 0

csv_path3 = arcpy.env.scratchGDB + "\\buff3.csv"
degisim_oranlari.to_csv(csv_path3, index=True)
arcpy.TableToTable_conversion(csv_path3, Workspace, "projection")
arcpy.Delete_management(csv_path2)
old_field = "Field1"
projection_table_path = Workspace + r"\\projection"
arcpy.AlterField_management(projection_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Etkinlik Analizi tablosu (ALL) tablosunun oluşturulması.. Bu kısımda artık gerçek değerler, hedef değerler
#ve projeksiyon oranları ortaya konmalıdır. Ayrıca sütun sıralaması da önemlidir.
##########################################################################################################
ALL = pd.concat([data_denormalize, degisim, degisim_oranlari], axis=1)
new_order = []

for i in range(len(data_denormalize.columns)):
    new_order.append(data_denormalize.columns[i])
    new_order.append(degisim.columns[i])
    new_order.append(degisim_oranlari.columns[i])

ALL = ALL.reindex(columns=new_order)

ALL['Score'] = etkinlik_matrisi['Score'].values
ALL['Score'] = ALL['Score'].round(3)


csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
ALL.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "ALL")
arcpy.Delete_management(csv_path1)
old_field = "Field1"
ALL_table_path = Workspace + r"\\ALL"
arcpy.AlterField_management(ALL_table_path, old_field, yol_name, yol_name)

##########################################################################################################
# Referans kümelerini oluşturmak için, caniniyedigim isimli değişkene geri dönmeliyiz. orada hazırlanan
# matris üzerinden etkinlik değerleri ve referans kümelerini alıp, bunu ALL tablosuna ve etkin olmayan yollar
# tablosuna yazdırmalıyız
##########################################################################################################
matris_coz = pd.DataFrame(np.copy(caniniyedigim))
matris_coz.columns = caniniyedigim.columns
matris_coz.index = caniniyedigim.index

# Sonuçları tutacak df
referans_df = pd.DataFrame(columns=[yol_name, 'Referanslar'])

# caniniyedigim üzerinde dönelim
for index, row in matris_coz.iterrows():
    yol_kodu = index
    satir_sonuclar = []
    # Satırdaki sütunlar üzerinde dönelim
    for sutun_adi, deger in row.iteritems():
        # kendisi eğer 1 ise kendisini vermesin.
        if sutun_adi != index and 0 < deger < 1:
            satir_sonuclar.append("{0} ({1:.5f})".format(sutun_adi, deger))

    if satir_sonuclar:
        referans_df = pd.concat([referans_df, pd.DataFrame({yol_name: [yol_kodu], 'Referanslar': [", ".join(satir_sonuclar)]})], ignore_index=True)

csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
referans_df.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "Referans")
arcpy.Delete_management(csv_path1)
Referans_table_path = Workspace + r"\\Referans"

arcpy.JoinField_management(ALL_table_path, yol_name, Referans_table_path, yol_name)
arcpy.DeleteField_management(ALL_table_path, [yol_name + "_1"])
arcpy.management.DeleteField(ALL_table_path, "Field1")
with arcpy.da.UpdateCursor(ALL_table_path, "Referanslar") as cursor:
    for row in cursor:
        if row[0] is None:
            row[0] = 'Etkin'
            cursor.updateRow(row)

##########################################################################################################
# ArGIS layerları için artık elimizdeki tabloları görselleştirme zamanı.. Bu görselleştirme sayesinde,
# arcgis üzerinde çıkışlarımızı direkt ekrana yansıtabileceğiz.
##########################################################################################################
if "\\" in Sosyal_Etkinlik_Tablosu:
    arcpy.management.Copy(str(Sosyal_Etkinlik_Tablosu), str(Workspace) + r"\\Sosyal_Etkinlik_Analizi")

else:
    arcpy.management.Copy(str(Workspace) + "\\" + str(Sosyal_Etkinlik_Tablosu), str(Workspace) + r"\\Sosyal_Etkinlik_Analizi")

Sosyal_Etkinlik_Analiz = str(Workspace) + r"\\Sosyal_Etkinlik_Analizi"
fields = [f.name for f in arcpy.ListFields(str(Sosyal_Etkinlik_Analiz))]
fields.remove('Shape')
fields.remove('OBJECTID')
fields.remove(yol_name)
fields.remove('Shape_Length')
arcpy.DeleteField_management(str(Sosyal_Etkinlik_Analiz), fields)

arcpy.JoinField_management(Sosyal_Etkinlik_Analiz, yol_name, ALL_table_path, yol_name)
arcpy.DeleteField_management(Sosyal_Etkinlik_Analiz, [yol_name + "_1"])

# Etkin olanlar, ALL tablosundan oluşan, Sosyal Etkinlik Analizi içinde "Score" sütunu 1'e eşit olanları filtrelemeli
query_1 = "Score >= 0.9999"
Sosyal_Etkinlik_Target_Etkin = str(Workspace) + r"\\Sosyal_Etkin_Olan"
arcpy.Select_analysis(Sosyal_Etkinlik_Analiz, Sosyal_Etkinlik_Target_Etkin, query_1)

# Etkin olanlar, ALL tablosundan oluşan, Sosyal Etkinlik Analizi içinde "Score" sütunu 1'den küçük olanları filtrelemeli
query_2 = "Score < 1"
Sosyal_Etkinlik_Target_Etkin_Olmayan = str(Workspace) + r"\\Sosyal_Etkin_Olmayan"
arcpy.Select_analysis(Sosyal_Etkinlik_Analiz, Sosyal_Etkinlik_Target_Etkin_Olmayan, query_2)

# Fazla tablolar varmış. meyveyi yedik. posasını atalım.. ;)
arcpy.Delete_management(projection_table_path)
arcpy.Delete_management(target_table_path)
arcpy.Delete_management(Referans_table_path)
arcpy.Delete_management(girdi_cikti_verileri)

# Ekrana yazdıralım.
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

ALL_Layer = arcpy.mapping.TableView(ALL_table_path)
arcpy.mapping.AddTableView(df, ALL_Layer)

etkinlik_matrisi_Layer = arcpy.mapping.TableView(etkinlik_table_path)
arcpy.mapping.AddTableView(df, etkinlik_matrisi_Layer)

normalize_tablo_Layer = arcpy.mapping.TableView(normalize_tablo)
arcpy.mapping.AddTableView(df, normalize_tablo_Layer)

korelasyon_table_Layer = arcpy.mapping.TableView(korelasyon_table_path)
arcpy.mapping.AddTableView(df, korelasyon_table_Layer)

Sosyal_Etkinlik_Target_Etkin_Olmayan_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Target_Etkin_Olmayan)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Target_Etkin_Olmayan_Layer)

Sosyal_Etkinlik_Target_Etkin_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Target_Etkin)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Target_Etkin_Layer)

Sosyal_Etkinlik_Analiz_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Analiz)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Analiz_Layer)

# Ekranı son kez yenilemek gerekli.. tablo, feature class güncellensin.. ;) c ya.
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
    

