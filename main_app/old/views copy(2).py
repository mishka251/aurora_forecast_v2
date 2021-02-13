



from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import scipy
from scipy.interpolate import griddata
from geopandas import GeoDataFrame
from shapely.geometry import Polygon, MultiPolygon
import geojsoncontour
from matplotlib.ticker import MaxNLocator
import csv
from django.contrib.staticfiles import finders
import json 

import urllib
from urllib import request
import os


# Create your views here.
def index(request):
    return render(request, 'index.html')

def getauroradata(request):
    url = "https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt"
    hemip = "https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt"
    url1 = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    url2 = "https://services.swpc.noaa.gov/products/solar-wind/plasma-6-hour.json"
    aurora = urllib.request.urlopen(url).read()
    date = ''
    for line in aurora.splitlines():
        if 'Product Generated At' in line.decode():
            s=line#.decode().split()
            date = (s[23:]).decode("utf-8") 
   
    NorthHPI = ''
    SouthHPI= ''
    hemi = urllib.request.urlopen(hemip).read()
    for line in hemi.splitlines():
        if '#' in line.decode():
            continue
        if date[1:17] in line.decode():
           NorthHPI = line.decode("utf-8") 
    str_ = ' '.join(NorthHPI.split())
    str_ = str_[17:]
    str_  =str_.split()
    NorthHPI = str_[0]
    SouthHPI=str_[1]
    
    
    mag = urllib.request.urlopen(url1).read()
    mag_ = json.loads(mag.decode())
    m = len(mag_)-1
    bx_gsm = ''
    by_gsm = ''
    bz_gsm = ''
    lon_gsm = ''
    lat_gsm = ''
    bt = ''
    for i in range(len(mag_)):
        if date[1:17] in mag_[i][0]:
            m = i
            break
    bx_gsm = mag_[int(m)][1]
    by_gsm = mag_[int(m)][2]
    bz_gsm = mag_[int(m)][3]
    lon_gsm = mag_[int(m)][4]
    lat_gsm = mag_[int(m)][5]
    bt = mag_[int(m)][6]

    proton = urllib.request.urlopen(url2).read()
    proton_ = json.loads(proton.decode())
    p = len(proton_)-1
    speed = ''
    density = ''
    for i in range(len(proton_)):
        if date[1:17] in proton_[i][0]:
            p = i
            break    
    density = proton_[int(p)][1]
    speed = proton_[int(p)][2]
    result = [NorthHPI,SouthHPI,bx_gsm,by_gsm,bz_gsm,lon_gsm,lat_gsm,speed,density]
    return HttpResponse(json.dumps(result))

def test(request):
    longi = [i*0.3515625-180 for i in range(1025)]
    lati = [j*0.3515625-90 for j in range(513)]
    ctr = 0
    ct = 0
    url = "https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt"
    logo = urllib.request.urlopen(url).read();
    fff = logo;
   # ff = open("/home/g/gimslaw8/geotest/public_html/aurora_ext.txt", "w");
#    ff.write("category,latitude,longitude" + '\n')
    arr = []
    #arr.append(['category','latitude','longitude'])
    for line in fff.splitlines():
        if (ctr == 1025):
            ctr = 0
            ct += 1
        if '#' in line.decode():
            continue
        s=line.decode().split()
        for k in range(1,len(s),3):
            ciqw=0
            if ((s[k-1]) == '0' or (s[k-1]) == '1'  or (s[k-1]) == '2'):
                continue
            arr_ = []
            arr_.append(float(s[k-1]))
            arr_.append((lati[ct]))
            arr_.append((longi[k-1]))
         #   ff.write(s[k-1]+ ',' + str(lati[ct]) + ',' + str(longi[k-1]) + '\n')
            arr.append(arr_)

        ct +=1        

    #ff.close()
    arr = np.array(arr)
    contour_data = pd.DataFrame({'category': arr[:, 0], 'latitude': arr[:, 1],'longitude': arr[:, 2]})
    
    Z = contour_data.pivot_table(index='longitude', columns='latitude', values='category').T.values
    X_unique = np.sort(contour_data['longitude'].unique())
    Y_unique = np.sort(contour_data['latitude'].unique())
    X, Y = np.meshgrid(X_unique, Y_unique)
    n_contours = 100#contour_data['category'].nunique()#40
    levels = np.linspace(start=0, stop=100, num=n_contours)

    contour = plt.contour(X, Y, Z,levels=levels, cmap=plt.cm.jet)

    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        min_angle_deg=1.0,
        ndigits=1,
        stroke_width=2,
     #   fill_opacity=0.5
    )

    return HttpResponse(geojson)
    #pd.DataFrame(arr)
    #return HttpResponse(contour_data.iloc[1])

def yadisk(request):
    API_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'

    return render(request, 'index.html')
