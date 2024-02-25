# -*- coding: utf-8 -*-
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorlarının Belirlenmesi (Tübitak 1002 - Proje No. 122O785)
#  @author: Arş. Gör. Taha Yasin HATAY (ArresT)
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Import module
import arcpy

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

# Script arguments
Ekolojik_Etkinlik_Klasor = arcpy.GetParameterAsText(0)

Orman_Yolu_Verileri = arcpy.GetParameterAsText(1)

Field = arcpy.GetParameterAsText(2)

# Process: Create File GDB
arcpy.CreateFileGDB_management(Ekolojik_Etkinlik_Klasor, "Ekolojik_Etkinlik", "CURRENT")

# Process: Feature Class to Feature Class
arcpy.AddField_management(Orman_Yolu_Verileri, "VZA_uzunluk", "Float")
arcpy.CalculateField_management(Orman_Yolu_Verileri, "VZA_uzunluk", "!shape.length@meters!", "PYTHON")
arcpy.conversion.FeatureClassToFeatureClass(Orman_Yolu_Verileri, Ekolojik_Etkinlik_Klasor + "\\Ekolojik_Etkinlik.gdb", "Ekolojik_Etkinlik_Tablosu")

Ekolojik_Etkinlik_Tablo = Ekolojik_Etkinlik_Klasor + "\\Ekolojik_Etkinlik.gdb\\Ekolojik_Etkinlik_Tablosu"

fields = [f.name for f in arcpy.ListFields(str(Ekolojik_Etkinlik_Tablo))]
fields.remove('Shape')
fields.remove('OBJECTID')
fields.remove(Field)
fields.remove('VZA_uzunluk')
fields.remove('Shape_Length')
arcpy.DeleteField_management(str(Ekolojik_Etkinlik_Tablo), fields)

#Çıkışları tanımla
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

Ekolojik_Etkinlik_Layer = arcpy.mapping.Layer(Ekolojik_Etkinlik_Tablo)
arcpy.mapping.AddLayer(df, Ekolojik_Etkinlik_Layer)

