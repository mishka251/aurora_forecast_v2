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

import urllib
from urllib import request
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

def getauroradata(request):
    data_url = 'http://gimslaw8.bget.ru/static/files/aurora_ext.csv'
    result = finders.find('files/aurora_ext.csv')
    searched_locations = finders.searched_locations
    url = str(searched_locations[0])+'/files/aurora_ext.csv'
  #  with open(str(searched_locations[0])+'/files/aurora_ext.csv') as f:
   #     return HttpResponse(f.read())
    #return HttpResponse(str(searched_locations[0]))
    contour_data = pd.read_csv(url)
    contour_data.head()

    Z = contour_data.pivot_table(index='longitude', columns='latitude', values='category').T.values
    X_unique = np.sort(contour_data['longitude'].unique())
    Y_unique = np.sort(contour_data['latitude'].unique())
    X, Y = np.meshgrid(X_unique, Y_unique)
    n_contours = 50#contour_data['category'].nunique()#40
    levels = np.linspace(start=0, stop=100, num=n_contours)

    contour = plt.contour(X, Y, Z,levels=levels, cmap=plt.cm.jet)

    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        min_angle_deg=3.0,
        ndigits=1,
        stroke_width=2,
     #   fill_opacity=0.5
    )

    return HttpResponse(geojson)

def test(request):
    longi = [i*0.3515625-180 for i in range(1025)]
    lati = [j*0.3515625-90 for j in range(513)]
    ctr = 0
    ct = 0
    url = "https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt"
    logo = urllib.request.urlopen(url).read();
    fff = logo;
    ff = open("/home/g/gimslaw8/geotest/public_html/aurora_ext.txt", "w");
    ff.write("category,latitude,longitude" + '\n')
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
            ff.write(s[k-1]+ ',' + str(lati[ct]) + ',' + str(longi[k-1]) + '\n')
            arr.append(arr_)

        ct +=1        

    ff.close()
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
