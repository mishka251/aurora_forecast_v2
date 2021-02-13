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

# Create your views here.
def index(request):
    return render(request, 'index.html')

def test(request):
    data_url = 'http://gimslaw8.bget.ru/static/files/aurora_ext.csv'
    contour_data = pd.read_csv(data_url)
    contour_data.head()
    Z = contour_data.pivot_table(index='longitude', columns='latitude', values='category').T.values
    X_unique = np.sort(contour_data['longitude'].unique())
    Y_unique = np.sort(contour_data['latitude'].unique())
    X, Y = np.meshgrid(X_unique, Y_unique)
    n_contours = 40#contour_data['category'].nunique()#40
    levels = np.linspace(start=0, stop=100, num=n_contours)
    #levels = np.linspace(start=contour_data['category'].min(), stop=contour_data['category'].max(), num=n_contours)
    contour = plt.contour(X, Y, Z,levels=levels, cmap=plt.cm.jet)
 
   # contour = plt.contour(X, Y, Z,levels=[4,15,27,40,70,100], colors#=['#e6f1f6','#feffef','#fff4d5','#fcddc9','#f8c6bf','#ff9999'])
    # Convert matplotlib contourf to geojson
    
           #{ value: 4, color: [0, 116, 165,0.1] }, 
        #{ value: 15, color: [246, 255, 146,0.15] },
       #{ value: 27, color: 	[255, 200, 47,0.2] },
       #{ value: 40, color: [241, 106, 22,0.23] },
    #    { value: 70, color: [231, 51, 26,0.28] },
     #63   { value: 100, color: [255, 0, 0,0.4] }
    
    
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        min_angle_deg=3.0,
        ndigits=1,
        stroke_width=2,
     #   fill_opacity=0.5
    )
    #geojson = geojsoncontour.contour_to_geojson(
    #    contour=contour,
    #    min_angle_deg=3.0,
    #    ndigits=3,
    #    stroke_width=2,
    #    fill_opacity=0.5
    #)
    
    return HttpResponse(geojson)
 

