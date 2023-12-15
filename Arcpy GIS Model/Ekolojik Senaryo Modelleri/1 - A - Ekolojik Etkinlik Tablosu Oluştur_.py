# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# AAAAA.py
# Created on: 2023-04-04 06:12:09.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: AAAAA <Sosyal_Etkinlik_Tablosu_Klasörü_Belirleyin> <Sosyal_Bellek_Klasörü_Belirleyin> <Orman_Yolu_Verilerini_Seçin> <Output_File_GDB__2_> <Field> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False

# Script arguments
Sosyal_Etkinlik_Klasor = arcpy.GetParameterAsText(0)

Orman_Yolu_Verileri = arcpy.GetParameterAsText(1)

Field = arcpy.GetParameterAsText(2)

# Process: Create File GDB
arcpy.CreateFileGDB_management(Sosyal_Etkinlik_Klasor, "Sosyal_Etkinlik", "CURRENT")

# Process: Feature Class to Feature Class
arcpy.conversion.FeatureClassToFeatureClass(Orman_Yolu_Verileri, Sosyal_Etkinlik_Klasor + "\\Sosyal_Etkinlik.gdb", "Sosyal_Etkinlik_Tablosu")

Sosyal_Etkinlik_Tablo = Sosyal_Etkinlik_Klasor + "\\Sosyal_Etkinlik.gdb\\Sosyal_Etkinlik_Tablosu"

fields = [f.name for f in arcpy.ListFields(str(Sosyal_Etkinlik_Tablo))]
fields.remove('Shape')
fields.remove('OBJECTID')
fields.remove(Field)
fields.remove('Shape_Length')
arcpy.DeleteField_management(str(Sosyal_Etkinlik_Tablo), fields)

#Çıkışları tanımla
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

Sosyal_Etkinlik_Layer = arcpy.mapping.Layer(Sosyal_Etkinlik_Tablo)
arcpy.mapping.AddLayer(df, Sosyal_Etkinlik_Layer)

