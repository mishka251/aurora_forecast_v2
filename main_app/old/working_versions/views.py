#https://services.swpc.noaa.gov/json/ovation_aurora_latest.json



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
import verde as vd
from numpy import linspace

import urllib
from urllib import request
import os
import yadisk
import time

from datetime import datetime

def collec_to_gdf(collec_poly):
    """Transform a `matplotlib.contour.QuadContourSet` to a GeoDataFrame"""
    polygons, colors = [], []
    for i, polygon in enumerate(collec_poly.collections):
        mpoly = []
        for path in polygon.get_paths():
            try:
                path.should_simplify = False
                poly = path.to_polygons()
                # Each polygon should contain an exterior ring + maybe hole(s):
                exterior, holes = [], []
                if len(poly) > 0 and len(poly[0]) > 3:
                    # The first of the list is the exterior ring :
                    exterior = poly[0]
                    # Other(s) are hole(s):
                    if len(poly) > 1:
                        holes = [h for h in poly[1:] if len(h) > 3]
                mpoly.append(Polygon(exterior, holes))
            except:
                print('Warning: Geometry error when making polygon #{}'
                      .format(i))
        if len(mpoly) > 1:
            mpoly = MultiPolygon(mpoly)
            polygons.append(mpoly)
            colors.append(polygon.get_facecolor().tolist()[0])
        elif len(mpoly) == 1:
            polygons.append(mpoly[0])
            colors.append(polygon.get_facecolor().tolist()[0])
    return GeoDataFrame(
        geometry=polygons,
        data={'RGBA': colors},
        crs={'init': 'epsg:4326'})

# Create your views here.
def index(request):
    return render(request, 'index.html')

def getauroradata(request):
    tmstpd = request.GET.get('tmstp')
    #url = "https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt" # Product Generated At: 2020-08-04 03:55
    url = "http://gimslaw8.bget.ru/getdata.php?type=aurora&dt=2021-01-02-11:50"
    hemip = 'http://gimslaw8.bget.ru/getdata.php?type=power&dt=2021-01-02-11:50'
    #hemip = "https://services.swpc.noaa.gov/text/aurora-nowcast-hemi-power.txt"
    url1 = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    url2 = "https://services.swpc.noaa.gov/products/solar-wind/plasma-6-hour.json"
    aurora = urllib.request.urlopen(url).read()
    full_date = tmstpd
    date_aurora = full_date[0:10]+' '+full_date[11:16]
    date_hemi = full_date[0:10]+'_'+full_date[11:16]
    #return HttpResponse(date)
  #  for line in aurora.splitlines():
   #     if 'Product Generated At' in line.decode():
    #        s=line#.decode().split()
     #       date = (s[23:]).decode("utf-8") 
   
    NorthHPI = ''
    SouthHPI= ''
    hemi = urllib.request.urlopen(hemip).read()
    hemi_arr = json.loads(hemi)
    str_=''
    
    for index in range(len(hemi_arr)):
        if date_hemi in hemi_arr[index]:
            str_ = hemi_arr[index]
        
   # for line in hemi.splitlines():
#        if '#' in line.decode():
 #           continue
  #      if date_hemi in line.decode():
   #        NorthHPI = line.decode("utf-8") 
    if(str_==''):
        str_ = hemi_arr[len(hemi_arr)-1]

    str_ = ' '.join(str_.split())
    str_ = str_[17:]
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
        if date_hemi in mag_[i][0]:
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
        if date_hemi in proton_[i][0]:
            p = i
            break    
    density = proton_[int(p)][1]
    speed = proton_[int(p)][2]
    
    result = [NorthHPI,SouthHPI,bx_gsm,by_gsm,bz_gsm,lon_gsm,lat_gsm,speed,density]
    return HttpResponse(json.dumps(result))
    

def test(request):
    tmstpd = request.GET.get('tmstp')
   # return HttpResponse(tmstpd)
    longi = [i*0.3515625-180 for i in range(1025)]
    lati = [j*0.3515625-90 for j in range(513)]
    ctr = 0
    ct = 0
    data_to_query = tmstpd#'2020-08-05-00:50' 
    
    just_date = tmstpd[0:10]
    #return HttpResponse(just_date)2021-01-08
    date1 = time.strptime(just_date, "%Y-%m-%d") 
    date2 = time.strptime('2020-10-30', "%Y-%m-%d") 
    typ = 'new'
    if(date1>=date2):
        typ = 'new'
    else:
        typ = 'old'
  #  return HttpResponse(typ)
    #url = 'http://gimslaw8.bget.ru/getdata.php?type=aurora'
    
    if typ == 'new':
        url = 'http://gimslaw8.bget.ru/getdata.php?type=aurora&dt='+data_to_query
        logo = urllib.request.urlopen(url).read();
        fff = logo;
        arr = [];
        
        for line in fff.decode().splitlines():
            s=line.strip()
            arr.append(s)
        
        j = json.loads(''.join(arr));
        arr1 = []
        data = j['coordinates']
    
    
        for k in range(1,len(data)):
            arr_ = []
            if (str(data[k][2]) != '0' and str(data[k][2]) != '1' and str(data[k][2]) != '2'):
                arr_.append(int(data[k][2]))
                arr_.append(float(data[k][1]))
                arr_.append(float(data[k][0]))
                arr1.append(arr_)
    
    
        arr1 = np.array(arr1)
        d = arr1
        '''
        contour_data = pd.DataFrame({'category': arr1[..., 0], 'latitude': arr1[..., 1],'longitude': arr1[..., 2]})
        
        Z = contour_data.pivot_table(index='longitude', columns='latitude', values='category').T.values
        X_unique = np.sort(contour_data['longitude'].unique())
        Y_unique = np.sort(contour_data['latitude'].unique())
        X, Y = np.meshgrid(X_unique, Y_unique)
        '''
        import matplotlib.tri as tri
        z=d[:,0]
        x=d[:,2]
        y=d[:,1]
        
        xi = np.sort(np.unique(x))
        yi = np.sort(np.unique(y))
        #X, Y = np.meshgrid(X_unique, Y_unique)
        
        #xi = linspace(x.min(),x.max(),50);
        #yi = linspace(y.min(),y.max(),50);
        
        from scipy.ndimage.filters import gaussian_filter
    
    
        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = interpolator(Xi, Yi)
        zi = gaussian_filter(zi, sigma=.7)
        #zi[Xi <= z.min()] = None
        #zi[Xi > z.max()] = None
       # zi[Xi > 100] = None
        levels = len(np.unique(z))
        contour = plt.contour(xi, yi, zi,levels=levels, cmap=plt.cm.jet,extend='both')#
        
        geojson = geojsoncontour.contour_to_geojson(
            contour=contour,
           # min_angle_deg=20.0,
            #ndigits=10,
            stroke_width=10,
    
        )
        #return HttpResponse('1')  
        #return HttpResponse(levels)   
        return HttpResponse(geojson)   
    
    if typ=='old':
        url = 'http://gimslaw8.bget.ru/getdata.php?type=aurora&dt=2020-08-05-11:50'
        logo = urllib.request.urlopen(url).read();
        fff = logo;  
        arr = [];
        for line in fff.splitlines():
            if (ctr == 1025):
                ctr = 0
                ct += 1
            if '#' in line.decode():
                continue
            s=line.split()
            for k in range(1,len(s),3):
                ciqw=0
                if ((s[k-1]) == '0' or (s[k-1]) == '1'  or (s[k-1]) == '2'):
                    continue
                arr_ = []
                arr_.append(float(s[k-1]))
                arr_.append((lati[ct]))
                arr_.append((longi[k-1]))
                arr.append(arr_)
            ct +=1  
    
        arr = np.array(arr)

        
        contour_data = pd.DataFrame({'category': arr[..., 0], 'latitude': arr[..., 1],'longitude': arr[..., 2]})
        
        Z = contour_data.pivot_table(index='longitude', columns='latitude', values='category').T.values
        X_unique = np.sort(contour_data['longitude'].unique())
        Y_unique = np.sort(contour_data['latitude'].unique())
        X, Y = np.meshgrid(X_unique, Y_unique)
        n_contours = 50#contour_data['category'].nunique()#40
        levels = np.linspace(start=0, stop=100, num=n_contours)
    
        contour = plt.contour(X, Y, Z,levels=levels, cmap=plt.cm.jet)
    
        geojson = geojsoncontour.contour_to_geojson(
            contour=contour,
            min_angle_deg=1.0,
            ndigits=1,
            stroke_width=2,
    
        )
        return HttpResponse(geojson)     

           
        
   

def yadisk2(request):
    #API_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'

    return render(request, 'index.html')
    
    
def sand(request):
#    data = vd.datasets.CheckerBoard().scatter(size=500, random_state=0)
    tkn = 'AgAAAAAmPFRWAADLW8HrD162JU_KmQ71dAnQ6fA'
    y = yadisk.YaDisk(token=tkn)
    start_year = 2020
    today = datetime.today()
    years = [start_year]
    start_year = start_year+1
    while(start_year <= today.year):
        years.append(start_year)
        start_year = start_year+1
    #files = list(y.listdir("/Aurora-forecast/Power/2020"))
    dates = []
    for year in years:
        files = list(y.listdir("/Aurora-forecast/Power/"+str(year)))
        for file in files:
            name = file['path'] #a_pow_2020-08-15
            pos = int(name.find('a_pow_'))
            date = name[pos+6:pos+16]
            dates.append(date)
   # ndates = []
    for year in years:
        files = list(y.listdir("/Aurora-forecast/Map/"+str(year)))
        for file in files:
            name = file['path']
            dates.append(name[31:41])
    return HttpResponse(json.dumps(dates))
    
    