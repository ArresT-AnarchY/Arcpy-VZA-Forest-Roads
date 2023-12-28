#-*coding:mbcs*-#
import arcpy
import os
import sys
import numpy as np
from scipy.optimize import fmin_slsqp
import pandas as pd

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

#Girişler
Workspace = arcpy.GetParameterAsText(0)
Sosyal_Etkinlik_Tablosu = arcpy.GetParameterAsText(1)
yol_name = arcpy.GetParameterAsText(2)
input_name = arcpy.GetParameterAsText(3)
if input_name == '#' or not input_name:
    input_name = "Yol_Uzunluk, Dolambac_Faktor, Kayip_Orman, Yol_Egimi"
output_name = arcpy.GetParameterAsText(4)
if output_name == '#' or not output_name:
    output_name = "Estetik_Orman, Ziraat_Mera_iskan, Kazi_Yesil, MAHALLE_NUFUS"

#Çıkışlar
ALL_Layer = arcpy.GetParameterAsText(3)
etkinlik_matrisi_Layer = arcpy.GetParameterAsText(4)
girdi_cikti_verileri_Layer = arcpy.GetParameterAsText(5)
projection_Layer = arcpy.GetParameterAsText(6)
target_LAYER = arcpy.GetParameterAsText(7)
Sosyal_Etkinlik_Projection_Layer = arcpy.GetParameterAsText(8)
Sosyal_Etkinlik_Target_Layer = arcpy.GetParameterAsText(9)

# Process: Table to Table
arcpy.TableToTable_conversion(Sosyal_Etkinlik_Tablosu, Workspace, "girdi_cikti_verileri", "", "", "")
table_path = Workspace + r"\\girdi_cikti_verileri"

# Girdi ve çıktı sütunlarını belirledim
input_fields = input_name.split(', ')
output_fields = output_name.split(', ')
names_field = yol_name

#Girdi ve Çıktıların Kontrolü
input_count = len(input_fields)
output_count = len(output_fields)

fields = arcpy.ListFields(Sosyal_Etkinlik_Tablosu)
field_names = [field.name for field in fields]

for field in input_fields + output_fields:
    if field not in field_names:
        arcpy.AddWarning("Minimize Target Field ve Maximize Target Field ile Feature Tablosu uyum saglamiyor")
        sys.exit()

# Girdi ve çıktı verileri için numpy tanımlanması
X = np.empty((0, len(input_fields)), float)
y = np.empty((0, len(output_fields)), float)
names = []

# Tablodan girdi ve çıktı değerleri numpy verisi
with arcpy.da.SearchCursor(table_path, input_fields + output_fields + [names_field]) as cursor:
    for row in cursor:
        X = np.append(X, [np.array([row[i] for i in range(len(input_fields))])], axis=0)
        y = np.append(y, [np.array([row[i] for i in range(len(input_fields), len(input_fields) + len(output_fields))])], axis=0)
        names.append(row[-1])

#Dataframe yaptım
xy = np.hstack((X, y))
data = pd.DataFrame(xy, index=names, columns=input_fields+output_fields)

#Dataframe içerisinde 0 değer olamaz. Bunlar 0.1 olmalı.
if (data == 0).any().any() or data.isnull().any().any():
    arcpy.AddWarning("Hata: Verilerinizde 0 degeri bulunmaktadir. Lutfen Arazide toplanan verileri ve hesaplanan verileri kontrol ediniz!")
    sys.exit(1) 

#DEA ANALİZİ
class DEA(object):
    def __init__(self, inputs, outputs):
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
        denominator = np.dot(self.inputs, self.input_w)
        numerator = np.dot(self.outputs, self.output_w)
        return (numerator/denominator)[unit]
    
    def __target(self, x, unit):
        in_w, out_w, lambdas = x[:self.m], x[self.m:(self.m+self.r)], x[(self.m+self.r):]
        denominator = np.dot(self.inputs[unit], in_w)
        numerator = np.dot(self.outputs[unit], out_w)
        return numerator/denominator
    
    def __constraints(self, x, unit):
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
        assert(self.n == len(names))
        self.names = names
    
    def fit(self):
        self.__optimize()
        arcpy.AddMessage("Her Yol Biriminde Sosyal Etkinlik Skorlari:\n")
        arcpy.AddMessage("---------------------------\n")
        for n, eff in enumerate(self.efficiency):
            if len(self.names) > 0:
                name = "Birim kod: %s" % self.names[n]
            else:
                name = "Birim kod: %d" % (n+1)
            arcpy.AddMessage("%s Sosyal Etkinlik Skoru: %.4f" % (name, eff))
            arcpy.AddMessage("\n")
        arcpy.AddMessage("---------------------------\n")
if __name__ == "__main__":
    # İstenen eff sınırı
    hedef_eff_siniri = 1.99

    while True:
        dea = DEA(X,y)
        dea.name_units(names)
        dea.fit()
        
        # Eğer eff değeri hedef_eff_siniri'nden küçükse döngüyü sonlandır
        if all(dea.efficiency <= hedef_eff_siniri):
            break
    caniniyedigim = dea.caniniyedigim
    etkinlik_matrisi = caniniyedigim.copy()
    etkinlik_matrisi['Score'] = dea.efficiency

#etkinlik matrisi oluşturma
csv_path = arcpy.env.scratchGDB + "\\buff.csv"
etkinlik_matrisi.to_csv(csv_path, index=True)
arcpy.TableToTable_conversion(csv_path, Workspace, "etkinlik_matrisi")
arcpy.Delete_management(csv_path)
old_field = "Field1"
etkinlik_table_path = Workspace + r"\\etkinlik_matrisi"
arcpy.AlterField_management(etkinlik_table_path, old_field, yol_name, yol_name)

#target tablosunun oluşturulması (data ile çarpılma işlemi)
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

# # Kısıtlamaların Eklenmesi
birlestirme_df['Score'] = etkinlik_matrisi['Score'].values
sinir = birlestirme_df['Score'] < 1
birlestirme_df.loc[sinir, 'Yol_Egimi'] = birlestirme_df.loc[sinir, 'Yol_Egimi'].apply(lambda x: max(4, x))
# birlestirme_df.loc[sinir, 'Yol_Genisligi'] = birlestirme_df.loc[sinir, 'Yol_Genisligi'].apply(lambda x: max(4, x))
# birlestirme_df.loc[sinir, 'Kazi_Yukseklik'] = birlestirme_df.loc[sinir, 'Kazi_Yukseklik'].apply(lambda x: max(4, x))
    
degisim = birlestirme_df.copy()
col1 = degisim.columns.copy()
degisim.columns = ['TARGET_' + str(col) for col in degisim.columns]
# assert data.shape == birlestirme_df.shape

csv_path2 = arcpy.env.scratchGDB + "\\buff2.csv"
degisim.to_csv(csv_path2, index=True)
arcpy.TableToTable_conversion(csv_path2, Workspace, "target")
arcpy.Delete_management(csv_path2)
old_field = "Field1"
target_table_path = Workspace + r"\\target"
arcpy.AlterField_management(target_table_path, old_field, yol_name, yol_name)

#projeksiyon oranlarının bulunması
degisim_oranlari = pd.DataFrame()
for col in data.columns:
    for row in data.index:
        oran = round((((birlestirme_df.loc[row, col] - data.loc[row, col]) / data.loc[row, col]) * 100),2)
        degisim_oranlari.loc[row, col] = oran    

degisim_oranlari.columns = ['PROJECTION_' + str(col1[i]) for i in range(degisim_oranlari.shape[1])]
degisim_oranlari[degisim_oranlari.abs() < 0.001] = 0

csv_path3 = arcpy.env.scratchGDB + "\\buff3.csv"
degisim_oranlari.to_csv(csv_path3, index=True)
arcpy.TableToTable_conversion(csv_path3, Workspace, "projection")
arcpy.Delete_management(csv_path2)
old_field = "Field1"
projection_table_path = Workspace + r"\\projection"
arcpy.AlterField_management(projection_table_path, old_field, yol_name, yol_name)

#ALL tablosu oluşturulması ve sıralaması
ALL = pd.concat([data, degisim, degisim_oranlari], axis=1)
new_order = []

for i in range(len(data.columns)):
    new_order.append(data.columns[i])
    new_order.append(degisim.columns[i])
    new_order.append(degisim_oranlari.columns[i])

ALL = ALL.reindex(columns=new_order)

csv_path1 = arcpy.env.scratchGDB + "\\buff1.csv"
ALL.to_csv(csv_path1, index=True)
arcpy.TableToTable_conversion(csv_path1, Workspace, "ALL")
arcpy.Delete_management(csv_path1)
old_field = "Field1"
ALL_table_path = Workspace + r"\\ALL"
arcpy.AlterField_management(ALL_table_path, old_field, yol_name, yol_name)

#Sosyal Etkinlik Şablonları oluştur
if "\\" in Sosyal_Etkinlik_Tablosu:
    arcpy.management.Copy(str(Sosyal_Etkinlik_Tablosu), str(Workspace) + r"\\Sosyal_Etkinlik_Projeksiyon")
    arcpy.management.Copy(str(Sosyal_Etkinlik_Tablosu), str(Workspace) + r"\\Sosyal_Etkinlik_Target")

else:
    arcpy.management.Copy(str(Workspace) + "\\" + str(Sosyal_Etkinlik_Tablosu), str(Workspace) + r"\\Sosyal_Etkinlik_Projeksiyon")
    arcpy.management.Copy(str(Workspace) + "\\" + str(Sosyal_Etkinlik_Tablosu), str(Workspace) + r"\\Sosyal_Etkinlik_Target")

Sosyal_Etkinlik_Projection = str(Workspace) + r"\\Sosyal_Etkinlik_Projeksiyon"
Sosyal_Etkinlik_Target = str(Workspace) + r"\\Sosyal_Etkinlik_Target"
fields = [f.name for f in arcpy.ListFields(str(Sosyal_Etkinlik_Projection))]
fields.remove('Shape')
fields.remove('OBJECTID')
fields.remove(yol_name)
fields.remove('Shape_Length')
arcpy.DeleteField_management(str(Sosyal_Etkinlik_Projection), fields)
arcpy.DeleteField_management(str(Sosyal_Etkinlik_Target), fields)

arcpy.JoinField_management(Sosyal_Etkinlik_Projection, yol_name, projection_table_path, yol_name)
arcpy.DeleteField_management(Sosyal_Etkinlik_Projection, [yol_name + "_1"])
arcpy.JoinField_management(Sosyal_Etkinlik_Target, yol_name, target_table_path, yol_name)
arcpy.DeleteField_management(Sosyal_Etkinlik_Target, [yol_name + "_1"])

# "TARGET_Score" sütunu 1'e eşit olanları filtrele
query_1 = "TARGET_Score >= 1"
Sosyal_Etkinlik_Target_Etkin = str(Workspace) + r"\\Sosyal_Etkin_Olan"
arcpy.Select_analysis(Sosyal_Etkinlik_Target, Sosyal_Etkinlik_Target_Etkin, query_1)

# "TARGET_Score" sütunu 1'den düşük olanları filtrele
query_2 = "TARGET_Score < 1"
Sosyal_Etkinlik_Target_Etkin_Olmayan = str(Workspace) + r"\\Sosyal_Etkin_Olmayan_Hedefler"
arcpy.Select_analysis(Sosyal_Etkinlik_Target, Sosyal_Etkinlik_Target_Etkin_Olmayan, query_2)


arcpy.Delete_management(table_path)
arcpy.Delete_management(projection_table_path)
arcpy.Delete_management(target_table_path)
arcpy.Delete_management(Sosyal_Etkinlik_Target)

#Çıkışları tanımla
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

ALL_Layer = arcpy.mapping.TableView(ALL_table_path)
arcpy.mapping.AddTableView(df, ALL_Layer)

etkinlik_matrisi_Layer = arcpy.mapping.TableView(etkinlik_table_path)
arcpy.mapping.AddTableView(df, etkinlik_matrisi_Layer)

Sosyal_Etkinlik_Projection_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Projection)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Projection_Layer)

Sosyal_Etkinlik_Target_Etkin_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Target_Etkin)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Target_Etkin_Layer)

Sosyal_Etkinlik_Target_Etkin_Olmayan_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Target_Etkin_Olmayan)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Target_Etkin_Olmayan_Layer)

