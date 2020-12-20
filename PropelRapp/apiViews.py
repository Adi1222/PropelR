import simplejson
from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404, _get_queryset
from .forms import *
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, time, timedelta
import urllib.request
import requests

@csrf_exempt
def get_visitors_data(request, *args, **kwargs):
    labels = []
    data = []

    x = request.POST.get('startdate','')
    y = request.POST.get('enddate','')
    camera = request.POST.get('camera','')

    print(x)
    print(camera)

    (month_start, date_start, month_end, date_end) = (0,0,0,0)

    temp_month_start = str(x.split("-")[1])
    temp_date_start = str(x.split("-")[2])

    if(len(temp_month_start) > 1):
        month_start = int(temp_month_start)
    else:
        month_start = int(temp_month_start[1])

    date_start = int(temp_date_start)


    temp_month_end = str(y.split("-")[1])
    temp_date_end = str(y.split("-")[2])

    if(len(temp_month_end) > 1):
        month_end = int(temp_month_end)
    else:
        month_end = int(temp_month_end[1])

    date_end = int(temp_date_end)


    startdate = date(2020, month_start, date_start)
    enddate = date(2020, month_end, date_end)

    start = startdate
    end = enddate

    url = "http://3.93.246.89:8000/GetData?chartType=People&cameraName={}&startDate={}&endDate={}".format(str(camera),str(startdate), str(enddate))
    response = requests.get(url)
    data1 = response.json()
    l = len(data1)
    i = 0
    visitors = 0
    delta = timedelta(days=1)

    while start<=end and i<l:
        visitors = data1[i][str(start)][str(camera)]
        labels.append(start)
        data.append(visitors)
        start += delta
        i += 1

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@csrf_exempt
def get_vehicles_data(request,  *args, **kwargs):
    labels = []
    data = []

    x = request.POST.get('startdate','')
    y = request.POST.get('enddate','')
    camera = request.POST.get('camera','')

    print(camera)

    (month_start, date_start, month_end, date_end) = (0,0,0,0)

    temp_month_start = str(x.split("-")[1])
    temp_date_start = str(x.split("-")[2])

    if(len(temp_month_start) > 1):
        month_start = int(temp_month_start)
    else:
        month_start = int(temp_month_start[1])

    date_start = int(temp_date_start)


    temp_month_end = str(y.split("-")[1])
    temp_date_end = str(y.split("-")[2])

    if(len(temp_month_end) > 1):
        month_end = int(temp_month_end)
    else:
        month_end = int(temp_month_end[1])

    date_end = int(temp_date_end)


    startdate = date(2020, month_start, date_start)
    enddate = date(2020, month_end, date_end)

    start = startdate
    end = enddate

    url = "http://3.93.246.89:8000/GetData?chartType=Vehicle&cameraName=&startDate={}&endDate={}".format(str(startdate), str(enddate))
    response = requests.get(url)
    data1 = response.json()
    l = len(data1)
    i = 0
    vehicles = 0
    delta = timedelta(days=1)

    while start<=end and i<l:
        vehicles = data1[i][str(start)]['B3-Parking']
        labels.append(start)
        data.append(vehicles)
        start += delta
        i += 1

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })






@csrf_exempt
def get_age_data(request, *args, **kwargs):
    labels = []
    data = []

    x = request.POST.get('startdate','')
    y = request.POST.get('enddate','')
    camera = request.POST.get('camera','')

    print(x)
    print(camera)

    (month_start, date_start, month_end, date_end) = (0,0,0,0)

    temp_month_start = str(x.split("-")[1])
    temp_date_start = str(x.split("-")[2])

    if(len(temp_month_start) > 1):
        month_start = int(temp_month_start)
    else:
        month_start = int(temp_month_start[1])

    date_start = int(temp_date_start)


    temp_month_end = str(y.split("-")[1])
    temp_date_end = str(y.split("-")[2])

    if(len(temp_month_end) > 1):
        month_end = int(temp_month_end)
    else:
        month_end = int(temp_month_end[1])

    date_end = int(temp_date_end)


    startdate = date(2020, month_start, date_start)
    enddate = date(2020, month_end, date_end)

    start = startdate
    end = enddate

    url = "http://3.93.246.89:8000/GetData?chartType=Age&cameraName={}&startDate={}&endDate={}".format(str(camera),str(startdate), str(enddate))
    response = requests.get(url)
    data1 = response.json()

    keys = ["(0, 2)", "(15, 20)", "(25, 32)", "(38, 43)", "(4, 6)", "(48, 53)", "(60, 100)", "(8, 12)"]

    for k in keys:
        data.append(data1[0][str(camera)][k])
        labels.append(k)


    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })









@csrf_exempt
def get_gender_data(request, *args, **kwargs):
    labels = []
    data_male = []
    data_female = []

    x = request.POST.get('startdate','')
    y = request.POST.get('enddate','')
    camera = request.POST.get('camera','')

    print(x)
    print(camera)

    (month_start, date_start, month_end, date_end) = (0,0,0,0)

    temp_month_start = str(x.split("-")[1])
    temp_date_start = str(x.split("-")[2])

    if(len(temp_month_start) > 1):
        month_start = int(temp_month_start)
    else:
        month_start = int(temp_month_start[1])

    date_start = int(temp_date_start)


    temp_month_end = str(y.split("-")[1])
    temp_date_end = str(y.split("-")[2])

    if(len(temp_month_end) > 1):
        month_end = int(temp_month_end)
    else:
        month_end = int(temp_month_end[1])

    date_end = int(temp_date_end)


    startdate = date(2020, month_start, date_start)
    enddate = date(2020, month_end, date_end)

    start = startdate
    end = enddate
    delta = timedelta(days=1)

    while start<=end:
        url = "http://3.93.246.89:8000/GetData?chartType=Gender&cameraName={}&startDate={}&endDate={}".format(str(camera), str(start), str(start))
        response = requests.get(url)
        data = response.json()

        data_male.append(data[0][str(camera)]['Male'])
        data_female.append(data[0][str(camera)]['Female'])


        labels.append(start)
        start += delta


    return JsonResponse(data={
        'labels': labels,
        'data_male': data_male,
        'data_female':data_female
    })







@csrf_exempt
def get_repeat_visitors_data(request, *args, **kwargs):
    labels = []
    data = []

    x = request.POST.get('startdate','')
    y = request.POST.get('enddate','')
    camera = request.POST.get('camera','')

    print(x)
    print(camera)

    (month_start, date_start, month_end, date_end) = (0,0,0,0)

    temp_month_start = str(x.split("-")[1])
    temp_date_start = str(x.split("-")[2])

    if(len(temp_month_start) > 1):
        month_start = int(temp_month_start)
    else:
        month_start = int(temp_month_start[1])

    date_start = int(temp_date_start)


    temp_month_end = str(y.split("-")[1])
    temp_date_end = str(y.split("-")[2])

    if(len(temp_month_end) > 1):
        month_end = int(temp_month_end)
    else:
        month_end = int(temp_month_end[1])

    date_end = int(temp_date_end)


    startdate = date(2020, month_start, date_start)
    enddate = date(2020, month_end, date_end)

    start = startdate
    end = enddate

    url = "http://3.93.246.89:8000/GetData?chartType=People&cameraName={}&startDate={}&endDate={}".format(str(camera),str(startdate), str(enddate))
    response = requests.get(url)
    data1 = response.json()
    l = len(data1)
    i = 0
    visitors = 0
    delta = timedelta(days=1)

    while start<=end and i<l:
        visitors = data1[i][str(start)][str(camera)]
        labels.append(start)
        data.append(visitors)
        start += delta
        i += 1

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })




@csrf_exempt
def get_repeat_vehicles_data(request, *args, **kwargs):
    labels = []
    data = []

    x = request.POST.get('startdate','')
    y = request.POST.get('enddate','')
    camera = request.POST.get('camera','')

    print(camera)

    (month_start, date_start, month_end, date_end) = (0,0,0,0)

    temp_month_start = str(x.split("-")[1])
    temp_date_start = str(x.split("-")[2])

    if(len(temp_month_start) > 1):
        month_start = int(temp_month_start)
    else:
        month_start = int(temp_month_start[1])

    date_start = int(temp_date_start)


    temp_month_end = str(y.split("-")[1])
    temp_date_end = str(y.split("-")[2])

    if(len(temp_month_end) > 1):
        month_end = int(temp_month_end)
    else:
        month_end = int(temp_month_end[1])

    date_end = int(temp_date_end)


    startdate = date(2020, month_start, date_start)
    enddate = date(2020, month_end, date_end)

    start = startdate
    end = enddate

    url = "http://3.93.246.89:8000/GetData?chartType=Vehicle&cameraName=&startDate={}&endDate={}".format(str(startdate), str(enddate))
    response = requests.get(url)
    data1 = response.json()
    l = len(data1)
    i = 0
    vehicles = 0
    delta = timedelta(days=1)

    while start<=end and i<l:
        vehicles = data1[i][str(start)]['B3-Parking']
        labels.append(start)
        data.append(vehicles)
        start += delta
        i += 1

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


@csrf_exempt
def get_camera_tampering_data(request, *args, **kwargs):
    pass

