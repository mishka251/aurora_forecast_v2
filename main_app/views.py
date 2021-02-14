from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
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

import requests

import urllib
from urllib import request
import os
import yadisk
import time

from datetime import datetime, timezone, timedelta
from django.conf import settings

def tester(request):
    return render(request, 'tester.html')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def getauroradata(request):
    tmstpd = request.GET.get('tmstp')
    url = "http://gimslaw8.bget.ru/getdata.php?type=aurora&dt=2021-01-02-11:50"
    hemip = 'http://gimslaw8.bget.ru/getdata.php?type=power&dt=2021-01-02-11:50'
    url1 = "https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json"
    url2 = "https://services.swpc.noaa.gov/products/solar-wind/plasma-6-hour.json"
    aurora = urllib.request.urlopen(url).read()
    full_date = tmstpd
    date_aurora = full_date[0:10] + ' ' + full_date[11:16]
    date_hemi = full_date[0:10] + '_' + full_date[11:16]

    NorthHPI = ''
    SouthHPI = ''
    hemi = urllib.request.urlopen(hemip).read()
    hemi_arr = json.loads(hemi)
    str_ = ''

    for index in range(len(hemi_arr)):
        if date_hemi in hemi_arr[index]:
            str_ = hemi_arr[index]

    if (str_ == ''):
        str_ = hemi_arr[len(hemi_arr) - 1]

    str_ = ' '.join(str_.split())
    str_ = str_[17:]
    str_ = str_[17:]
    str_ = str_.split()
    NorthHPI = str_[0]
    SouthHPI = str_[1]

    mag = urllib.request.urlopen(url1).read()
    mag_ = json.loads(mag.decode())
    m = len(mag_) - 1
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
    p = len(proton_) - 1
    speed = ''
    density = ''
    for i in range(len(proton_)):
        if date_hemi in proton_[i][0]:
            p = i
            break
    density = proton_[int(p)][1]
    speed = proton_[int(p)][2]

    result = [NorthHPI, SouthHPI, bx_gsm, by_gsm, bz_gsm, lon_gsm, lat_gsm, speed, density]
    return HttpResponse(json.dumps(result))


def test(request):
    tmstpd = request.GET.get('tmstp')
    mod = request.GET.get('mod')
    data_to_query = tmstpd
    just_date = tmstpd[0:10]
    date1 = time.strptime(just_date, "%Y-%m-%d")
    date2 = time.strptime('2020-10-30', "%Y-%m-%d")
    if (mod == 'w'):
        #
        # url = 'https://geomagnet.ru/weimer_api/?type=epot&tmstp='+data_to_query
        url = 'https://geomagnet.ru/weimer_api/?type=epot&tmstp=2021-01-24-20:02'
        logo = urllib.request.urlopen(url).read();
        fff = logo;
        arr = [];
        for line in fff.decode().splitlines():
            s = line.strip()
            arr.append(s)
        j = json.loads(''.join(arr));
        arr1 = []
        data = j['coordinates']
        for k in range(1, len(data)):
            arr_ = []
            arr_.append(int(data[k][2]))
            arr_.append(float(data[k][1]))
            arr_.append(float(data[k][0]))
            arr1.append(arr_)
        arr1 = np.array(arr1)
        d = arr1
        import matplotlib.tri as tri
        z = d[:, 0]
        x = d[:, 2]
        y = d[:, 1]
        xi = np.sort(np.unique(x))
        yi = np.sort(np.unique(y))
        from scipy.ndimage.filters import gaussian_filter
        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        Xi, Yi = np.meshgrid(xi, yi)
        zi = interpolator(Xi, Yi)
        zi = gaussian_filter(zi, sigma=.7)
        levels = len(np.unique(z))
        contour = plt.contour(xi, yi, zi, levels=levels, cmap=plt.cm.jet, extend='both')  #
        geojson = geojsoncontour.contour_to_geojson(
            contour=contour,
            stroke_width=10
        )
        return HttpResponse(geojson)
        ###
    #
    else:
        longi = [i * 0.3515625 - 180 for i in range(1025)]
        lati = [j * 0.3515625 - 90 for j in range(513)]
        ctr = 0
        ct = 0
        #    data_to_query = tmstpd
        #    just_date = tmstpd[0:10]
        #    date1 = time.strptime(just_date, "%Y-%m-%d")
        #    date2 = time.strptime('2020-10-30', "%Y-%m-%d")
        typ = 'new'
        if (date1 >= date2):
            typ = 'new'
        else:
            typ = 'old'

        if typ == 'new':
            # return redirect('/getdata?type=aurora&dt='+data_to_query)
            # url = '/getdata?type=aurora&dt='+data_to_query
            # logo = urllib.request.urlopen(url).read();
            # fff = logo;
            # arr = [];
            # for line in fff.decode().splitlines():
            #     s=line.strip()
            #     arr.append(s)
            # j = json.loads(''.join(arr));
            j = getdata('aurora', data_to_query)
            if j is None:
                return JsonResponse(None, safe=False)
            arr1 = []
            data = j['coordinates']
            for k in range(1, len(data)):
                arr_ = []
                if (str(data[k][2]) != '0' and str(data[k][2]) != '1' and str(data[k][2]) != '2'):
                    arr_.append(int(data[k][2]))
                    arr_.append(float(data[k][1]))
                    arr_.append(float(data[k][0]))
                    arr1.append(arr_)
            arr1 = np.array(arr1)
            d = arr1
            import matplotlib.tri as tri
            z = d[:, 0]
            x = d[:, 2]
            y = d[:, 1]
            xi = np.sort(np.unique(x))
            yi = np.sort(np.unique(y))
            from scipy.ndimage.filters import gaussian_filter
            triang = tri.Triangulation(x, y)
            interpolator = tri.LinearTriInterpolator(triang, z)
            Xi, Yi = np.meshgrid(xi, yi)
            zi = interpolator(Xi, Yi)
            zi = gaussian_filter(zi, sigma=.7)
            levels = len(np.unique(z))
            contour = plt.contour(xi, yi, zi, levels=levels, cmap=plt.cm.jet, extend='both')  #
            geojson = geojsoncontour.contour_to_geojson(
                contour=contour,
                stroke_width=10
            )
            return HttpResponse(geojson)

        if typ == 'old':
            logo = getdata('aurora', data_to_query)
            # url = '/getdata?type=aurora&dt='+data_to_query
            # logo = urllib.request.urlopen(url).read();
            fff = logo;
            arr = [];
            for line in fff.splitlines():
                if (ctr == 1025):
                    ctr = 0
                    ct += 1
                if '#' in line.decode():
                    continue
                s = line.split()
                for k in range(1, len(s), 3):
                    ciqw = 0
                    if ((s[k - 1]) == '0' or (s[k - 1]) == '1' or (s[k - 1]) == '2'):
                        continue
                    arr_ = []
                    arr_.append(float(s[k - 1]))
                    arr_.append((lati[ct]))
                    arr_.append((longi[k - 1]))
                    arr.append(arr_)
                ct += 1
            arr = np.array(arr)
            contour_data = pd.DataFrame({'category': arr[..., 0], 'latitude': arr[..., 1], 'longitude': arr[..., 2]})
            Z = contour_data.pivot_table(index='longitude', columns='latitude', values='category').T.values
            X_unique = np.sort(contour_data['longitude'].unique())
            Y_unique = np.sort(contour_data['latitude'].unique())
            X, Y = np.meshgrid(X_unique, Y_unique)
            n_contours = 50  # contour_data['category'].nunique()#40
            levels = np.linspace(start=0, stop=100, num=n_contours)
            contour = plt.contour(X, Y, Z, levels=levels, cmap=plt.cm.jet)
            geojson = geojsoncontour.contour_to_geojson(
                contour=contour,
                min_angle_deg=1.0,
                ndigits=1,
                stroke_width=2,
            )
            return HttpResponse(geojson)


def sand(request):
    tkn = settings.YA_DISK_TOKEN
    y = yadisk.YaDisk(token=tkn)
    start_year = 2020
    today = datetime.today()
    years = [start_year]
    start_year = start_year + 1
    while (start_year <= today.year):
        years.append(start_year)
        start_year = start_year + 1
    dates = []
    for year in years:
        files = list(y.listdir("/Aurora-forecast/Power/" + str(year)))
        for file in files:
            name = file['path']  # a_pow_2020-08-15
            pos = int(name.find('a_pow_'))
            date = name[pos + 6:pos + 16]
            dates.append(date)
    for year in years:
        files = list(y.listdir("/Aurora-forecast/Map/" + str(year)))
        for file in files:
            name = file['path']
            dates.append(name[31:41])
    return HttpResponse(json.dumps(dates))


def weimer(request):
    tmstpd = request.GET.get('tmstp')
    mod = request.GET.get('mod')
    data_to_query = tmstpd
    # url = 'https://geomagnet.ru/weimer_api/?type=epot&tmstp=2015-03-17-23:15'
    url = 'https://geomagnet.ru/weimer_api/?type=epot&tmstp=' + data_to_query
    logo = urllib.request.urlopen(url).read();
    fff = logo;
    if (str(json.loads(fff))[2] == 'e'):
        url = 'https://geomagnet.ru/weimer_api/?type=epot&tmstp=2021-02-01-05:21'
        logo = urllib.request.urlopen(url).read();
        fff = logo;
    arr = [];
    for line in fff.decode().splitlines():
        s = line.strip()
        arr.append(s)
    j = json.loads(''.join(arr));
    arr1 = []
    data = j['coordinates']
    for k in range(1, len(data)):
        arr_ = []
        if (str(data[k][2]) != '0' and str(data[k][2]) != '1' and str(data[k][2]) != '2'):
            arr_.append(int(data[k][2]))
            arr_.append(float(data[k][1]))
            arr_.append(float(data[k][0]))
            arr1.append(arr_)
    arr1 = np.array(arr1)
    d = arr1
    import matplotlib.tri as tri
    z = d[:, 0]
    x = d[:, 2]
    y = d[:, 1]
    xi = np.sort(np.unique(x))
    yi = np.sort(np.unique(y))
    from scipy.ndimage.filters import gaussian_filter
    triang = tri.Triangulation(x, y)
    interpolator = tri.LinearTriInterpolator(triang, z)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)
    zi = gaussian_filter(zi, sigma=.7)
    levels = 20  # len(np.unique(z))
    contour = plt.contour(xi, yi, zi, levels=levels, cmap=plt.cm.jet, extend='both')  #
    geojson = geojsoncontour.contour_to_geojson(
        contour=contour,
        stroke_width=10
    )
    return HttpResponse(geojson)


def get_yadisk_power(file_path):
    tkn = settings.YA_DISK_TOKEN
    ya_disk = yadisk.YaDisk(token=tkn)
    ya_disk.download(file_path, 'tmp.txt')
    lines = []
    with open('tmp.txt', 'r') as f:
        line = f.readline().strip()
        while line:
            if '#' not in line:
                lines.append(line)
            line = f.readline().strip()

    return lines


def get_another_from_yadisk(file_path):
    tkn = settings.YA_DISK_TOKEN
    ya_disk = yadisk.YaDisk(token=tkn)
    ya_disk.download(file_path, 'tmp.txt')
    lines = []
    with open('tmp.txt', 'r') as f:
        line = f.readline().strip()
        while line:
            if '#' not in line:
                lines.append(line)
            line = f.readline().strip()

    return json.loads('/n'.join(lines))


def get_data_from_noaa(url):
    r = requests.get(url)
    return r.text


def getdata(type, dt):
    tkn = settings.YA_DISK_TOKEN
    date = dt[0:10]
    year = dt[0:4]
    ya_disk = yadisk.YaDisk(token=tkn)
    data = None
    if type == 'power':

        name_power = 'a_pow_' + date
        file = 'disk:/Aurora-forecast/Power/' + year + '/' + name_power + '\n.txt'
        if ya_disk.exists(file):
            data = get_yadisk_power(file)
        else:
            data = 'none'
        # resource = ya_disk.
    else:  # TODO elif, else - raise 400
        path = 'disk:/Aurora-forecast/Map/' + year + '/' + date + '/' + 'a_map_'
        if date < '2020-10-29':
            test_path = '/Aurora-forecast/Map/' + year + '/' + date + '/'
            if ya_disk.exists(test_path):
                hour = date[11:13]
                min = date[14:16]

                if (min < '5'):  # TODO нормальное округление времени
                    min = min[0] + '0'
                else:
                    min = min[0] + '5'

                time = hour + ':' + min

                wholedate = date + '-' + time

                path_corr = path + wholedate + '.txt'

                if not ya_disk.exists(path_corr):  # 1 попытка сделать коррекцию
                    date = datetime.strptime(wholedate, '%Y-%m-%d-%H:%M')
                    date -= timedelta(minutes=5)
                    wholedate = date.strftime('%Y-%m-%d-%H:%M')
                    path_corr = path + wholedate + '.txt'

                if ya_disk.exists(path_corr):
                    path = path_corr
                    data = get_another_from_yadisk(path)
                else:
                    path = 'https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt'
                    data = get_data_from_noaa(path)
            else:
                path = 'https://services.swpc.noaa.gov/text/aurora-nowcast-map.txt'
                data = get_data_from_noaa(path)
        else:
            hour = dt[11:13]
            min = dt[14:16]

            iters = 0

            wholedate = date + '-' + hour + ':' + min
            path_corr = path + wholedate + '.txt'
            if not ya_disk.exists(path_corr):
                now = datetime.strptime(wholedate, '%Y-%m-%d-%H:%M')
                midnight_prev = datetime.strptime(date + ' 00:00', '%Y-%m-%d %H:%M')
                midnight_next = datetime.strptime(date + ' 23:59', '%Y-%m-%d %H:%M')
                path_found = False
                while now > midnight_prev:
                    iters +=1
                    now -= timedelta(minutes=1)
                    path_corr = path + now.strftime('%Y-%m-%d-%H:%M') + '.txt'
                    if ya_disk.exists(path_corr):
                        path_found = True
                        data = get_another_from_yadisk(path_corr)
                        break
                    if iters > 2*60:
                        break
                if not path_found:
                    iters = 0
                    now = datetime.strptime(wholedate, '%Y-%m-%d-%H:%M')
                    while now < midnight_next:
                        now += timedelta(minutes=1)
                        iters += 1
                        path_corr = path + now.strftime('%Y-%m-%d-%H:%M') + '.txt'
                        if ya_disk.exists(path_corr):
                            path_found = True
                            data = get_another_from_yadisk(path_corr)
                            break
                        if iters > 2 * 60:
                            break
                    if not path_found:
                        data = None  # not found
            else:
                data = get_another_from_yadisk(path_corr)
    return data


def getdata_view(request):
    type = request.GET['type']
    dt: str = request.GET['dt']

    data = getdata(type, dt)
    return JsonResponse(data, safe=False)
