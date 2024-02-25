# -*- coding: utf-8 -*-
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#  Orman Yollarının Fonksiyonel Duruma Bağlı Etkinlik Skorlarının Belirlenmesi (Tübitak 1002 - Proje No. 122O785)
#  @author: Arş. Gör. Taha Yasin HATAY (ArresT)
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Import arcpy module
import arcpy
import sys
import os
import json


# Set environment settings
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False


# Get script parameters
Ekonomik_Etkinlik_Klasor = arcpy.GetParameterAsText(0)
Workspace = arcpy.GetParameterAsText(1)
Etkin_Orman_Yollari = arcpy.GetParameterAsText(2)
Etkin_Olmayan_Orman_Yollari = arcpy.GetParameterAsText(3)
GeoJSON_Cikti_Klasor = arcpy.GetParameterAsText(4)

# Define output paths
etkin_olan = Workspace + "\\Ekonomik_Etkin_Olan_WGS84"
etkin_olmayan = Workspace + "\\Ekonomik_Etkin_Olmayan_WGS84"
etkinlayer = Workspace + "\\etkinlyr"
etkinolmayanlayer = Workspace + "\\etkinolmayanlyr"
etkin_kmz = Ekonomik_Etkinlik_Klasor + "\\etkin_olan.kmz"
etkin_olmayan_kmz = Ekonomik_Etkinlik_Klasor + "\\etkin_olmayan.kmz"
etkinlayer1 = Ekonomik_Etkinlik_Klasor + "\\etkin_olan.lyr"
etkinolmayanlayer2 = Ekonomik_Etkinlik_Klasor + "\\etkin_olmayan.lyr"
buff1 = Workspace + "\\etkin_olan"
buff2 = Workspace + "\\etkin_olmayan"
etkinlayergdb = Workspace + "\\etkinlyr.gdb"
etkinolmayanlayergdb = Workspace + "\\etkinolmayanlyr.gdb"

# Define coordinate system
wgs84_gcs = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

# Project feature classes
arcpy.Project_management(Etkin_Orman_Yollari, etkin_olan, wgs84_gcs, "", "", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")
arcpy.Project_management(Etkin_Olmayan_Orman_Yollari, etkin_olmayan, wgs84_gcs, "", "", "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

arcpy.MakeFeatureLayer_management(etkin_olan, etkinlayer)
arcpy.MakeFeatureLayer_management(etkin_olmayan, etkinolmayanlayer)

# Convert to KML
arcpy.LayerToKML_conversion(etkinlayer, etkin_kmz, "0", "NO_COMPOSITE", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")
arcpy.LayerToKML_conversion(etkinolmayanlayer, etkin_olmayan_kmz, "0", "NO_COMPOSITE", "DEFAULT", "1024", "96", "CLAMPED_TO_GROUND")

arcpy.KMLToLayer_conversion(etkin_kmz, etkinlayer1,'etkin_olan.lyr')
arcpy.KMLToLayer_conversion(etkin_olmayan_kmz, etkinolmayanlayer2,'etkin_olmayan.lyr')

arcpy.FeatureClassToFeatureClass_conversion(Ekonomik_Etkinlik_Klasor + "\\etkin_olan.lyr\\etkin_olan.lyr.gdb\\Polylines" , Workspace, "etkin_olan")
arcpy.FeatureClassToFeatureClass_conversion(Ekonomik_Etkinlik_Klasor + "\\etkin_olmayan.lyr\\etkin_olmayan.lyr.gdb\\Polylines" , Workspace, "etkin_olmayan")

arcpy.JoinField_management(etkin_olan, "YOL_KODU", buff1, "NAME")
arcpy.JoinField_management(etkin_olmayan, "YOL_KODU", buff2, "NAME")

# Feature Class'ten veriyi çekme
features = []
fields = ['SHAPE@JSON', 'Referanslar', 'Score', 'PopupInfo', 'YOL_KODU']  # Koordinatları ve özellik alanları belirtin


with arcpy.da.SearchCursor(etkin_olan, fields) as cursor:
    for row in cursor:
        geometry_json = json.loads(row[0])
        properties = {'referans': row[1], 'Score': row[2], 'description': row[3], 'Name': row[4]}  # İhtiyaca göre özellikleri ekleyin
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",  # Veri tipine göre "Point", "LineString", "Polygon" vb. ekleyin
                "coordinates": [geometry_json['paths'][0]],  # "coordinates" direkt olarak "paths" içeriğine eşitlenir,
            },
            "properties": properties
        }
        features.append(feature)

# FeatureCollection oluşturma
feature_collection = {
    "type": "FeatureCollection",
    "name": "EtkinOlan",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": features
}

# GeoJSON dosyasına yazma
with open(GeoJSON_Cikti_Klasor + "\\etkin_olan.geojson", 'w') as f:
    json.dump(feature_collection, f, indent=2)
    
    
# Feature Class'ten veriyi çekme
features2 = []
fields = ['SHAPE@JSON', 'Referanslar', 'Score', 'PopupInfo', 'YOL_KODU']  # Koordinatları ve özellik alanları belirtin

with arcpy.da.SearchCursor(etkin_olmayan, fields) as cursor:
    for row in cursor:
        geometry_json = json.loads(row[0])
        properties = {'referans': row[1], 'Score': row[2], 'description': row[3], 'Name': row[4]}  # İhtiyaca göre özellikleri ekleyin
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",  # Veri tipine göre "Point", "LineString", "Polygon" vb. ekleyin
                "coordinates": [geometry_json['paths'][0]],  # "coordinates" direkt olarak "paths" içeriğine eşitlenir,
            },
            "properties": properties
        }
        features2.append(feature)

# FeatureCollection oluşturma
feature_collection = {
    "type": "FeatureCollection",
    "name": "EtkinOlmayan",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": features2
}

# GeoJSON dosyasına yazma
with open(GeoJSON_Cikti_Klasor + "\\etkin_olmayan.geojson", 'w') as f:
    json.dump(feature_collection, f, indent=2)


arcpy.management.Delete(etkinlayer)
arcpy.management.Delete(etkinolmayanlayer)
arcpy.management.Delete(buff1)
arcpy.management.Delete(buff2)
arcpy.management.Delete(etkin_kmz)
arcpy.management.Delete(etkin_olmayan_kmz)
arcpy.management.Delete(etkinlayer1)
arcpy.management.Delete(etkinolmayanlayer2)
arcpy.management.Delete(etkinlayergdb)
arcpy.management.Delete(etkinolmayanlayergdb)