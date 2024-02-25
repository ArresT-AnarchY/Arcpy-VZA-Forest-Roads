# -*- coding: utf-8 -*-
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorlarının Belirlenmesi (Tübitak 1002 - Proje No. 122O785)
#  @author: Arş. Gör. Taha Yasin HATAY (ArresT)
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Import arcpy module
import arcpy

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

# Script arguments
Ekonomik_Etkinlik_Klasor = arcpy.GetParameterAsText(0)

Orman_Yolu_Verileri = arcpy.GetParameterAsText(1)

Field = arcpy.GetParameterAsText(2)

# Process: Create File GDB
arcpy.CreateFileGDB_management(Ekonomik_Etkinlik_Klasor, "Ekonomik_Etkinlik", "CURRENT")

# Process: Feature Class to Feature Class
arcpy.AddField_management(Orman_Yolu_Verileri, "VZA_uzunluk", "Float")
arcpy.CalculateField_management(Orman_Yolu_Verileri, "VZA_uzunluk", "!shape.length@meters!", "PYTHON")
arcpy.conversion.FeatureClassToFeatureClass(Orman_Yolu_Verileri, Ekonomik_Etkinlik_Klasor + "\\Ekonomik_Etkinlik.gdb", "Ekonomik_Etkinlik_Tablosu")

Ekonomik_Etkinlik_Tablo = Ekonomik_Etkinlik_Klasor + "\\Ekonomik_Etkinlik.gdb\\Ekonomik_Etkinlik_Tablosu"

fields = [f.name for f in arcpy.ListFields(str(Ekonomik_Etkinlik_Tablo))]
fields.remove('Shape')
fields.remove('OBJECTID')
fields.remove(Field)
fields.remove('VZA_uzunluk')
fields.remove('Shape_Length')
arcpy.DeleteField_management(str(Ekonomik_Etkinlik_Tablo), fields)

#Çıkışları tanımla
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

Ekonomik_Etkinlik_Layer = arcpy.mapping.Layer(Ekonomik_Etkinlik_Tablo)
arcpy.mapping.AddLayer(df, Ekonomik_Etkinlik_Layer)

