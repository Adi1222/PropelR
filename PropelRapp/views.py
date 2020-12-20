import simplejson
from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404, _get_queryset
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, HttpResponseServerError, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, time, timedelta
from django.views.decorators import gzip
from calendar import *
import urllib.request
import requests
import cv2
import numpy as np
from .camera import VideoCamera


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                messages.success(request, f"You are now logged in as {request.user.username}")
                return redirect('/PropelR/Dashboard')
            else:
                pass

        else:
            pass
    form = AuthenticationForm()
    return render(request, "PropelRapp/b1.html", context={"form": form})


def register(request):
    if request.method == 'POST':
        return redirect('/PropelR/Dashboard')
    else:
        return render(request, 'PropelRapp/register.html')


@csrf_exempt
def get_cameras(request):
    cameras = Camera.objects.filter(cluster_id=request.POST.get('cluster_id', ''))
    camera_obj = serializers.serialize('python', cameras)
    return JsonResponse(camera_obj, safe=False)


@csrf_exempt
def get_clusters(request):
    clusters = Cluster.objects.filter(customer_id=request.POST.get('customer_id', ''))
    cluster_obj = serializers.serialize('python', clusters)
    return JsonResponse(cluster_obj, safe=False)


# ********************        DASHBOARD         **************#


def dashboard(request):
    chartType = ['Vehicle', 'People', 'Age', 'Gender', 'Emotion']
    (total_visitors_today, total_vehicles_today, age_today, gender_male_today, gender_female_today) = (0, 0, 0, 0, 0)
    (total_visitors, total_vehicles, age, gender_male, gender_female) = (0, 0, 0, 0, 0)

    for x in chartType:
        today = date.today()
        url = "http://3.93.246.89:8000/GetData?chartType={}&cameraName=&startDate={}&endDate={}".format(str(x), str(today), str(today))
        response_today = requests.get(url)
        data = response_today.json()
        print(data)
        if x == 'Vehicle':
            total_vehicles_today = data[0][str(today)]['B3-Parking']
            print(total_vehicles_today)
        elif x == 'People':
            total_visitors_today = data[0][str(today)]['B3-Lobby'] + data[0][str(today)]['Main-Entrance']
            print(total_visitors_today)
        elif x == 'Gender':
            gender_male_today = data[0]['B3-Lobby']['Male'] + data[1]['Main-Entrance']['Male']
            gender_female_today = data[0]['B3-Lobby']['Female'] + data[1]['Main-Entrance']['Female']
            print(gender_male_today)
            print(gender_female_today)

    print()
    start_date = date(2020, 3, 27)
    end_date = date.today()
    for x in chartType:
        today = date.today()
        url = "http://3.93.246.89:8000/GetData?chartType={}&cameraName=&startDate=2020-03-27&endDate={}".format(str(x), str(today))
        response_today = requests.get(url)
        data = response_today.json()
        print(data)
        print()

        i = 0
        l = len(data)
        start = start_date
        end = end_date
        delta = timedelta(days=1)

        if x == 'Vehicle':
            while start <= end and i < l:
                total_vehicles += data[i][str(start)]['B3-Parking']
                start += delta
                i += 1
            print(total_vehicles)
        elif x == 'People':
            while start <= end and i < l:
                total_visitors += (data[i][str(start)]['B3-Lobby'] + data[i][str(start)]['Main-Entrance'])
                start += delta
                i += 1
            print(total_visitors)
        elif x == 'Gender':
            gender_male = data[0]['B3-Lobby']['Male'] + data[1]['Main-Entrance']['Male']
            gender_female = data[0]['B3-Lobby']['Female'] + data[1]['Main-Entrance']['Female']
            print(gender_male)
            print(gender_female)

    context = {
        'total_visitors': total_visitors,
        'total_vehicles': total_vehicles,
        'age': age,
        'gender_male': gender_male,
        'gender_female': gender_female,
        'total_visitors_today': total_visitors_today,
        'total_vehicles_today': total_vehicles_today,
        'age_today': age_today,
        'gender_male_today': gender_male_today,
        'gender_female_today': gender_female_today
    }

    return render(request, 'PropelRapp/main dashboard.html', context=context)


def visitor_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/visitors-count.html', {'clusters': clusters, 'cameras': cameras, 'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        # cluster_ids = set(map(lambda x: x.pk, clusters))
        # cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
        return render(request, 'PropelRapp/visitors-count.html', {'clusters': clusters})


def vehicle_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/vehicle-count.html', {'clusters': clusters, 'cameras': cameras, 'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/vehicle-count.html', {'clusters': clusters})


def age_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/age_detail.html', {'clusters': clusters, 'cameras': cameras,  'customers':customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        # cluster_ids = set(map(lambda x: x.pk, clusters))
        # cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
        return render(request, 'PropelRapp/age_detail.html', {'clusters': clusters})


def gender_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/gender_detail.html', {'clusters': clusters, 'cameras': cameras, 'customers':customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        # cluster_ids = set(map(lambda x: x.pk, clusters))
        # cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
        return render(request, 'PropelRapp/gender_detail.html', {'clusters': clusters})


def repeat_vehicle_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/repeat-vehicle.html', {'clusters': clusters,'customers':customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
    return render(request, 'PropelRapp/repeat-vehicle.html', {'clusters': clusters})


def repeat_visitor_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/repeat-visitors.html', {'clusters': clusters, 'cameras': cameras, 'customers':customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
    return render(request, 'PropelRapp/repeat-visitors.html', {'clusters': clusters})


def camera_tampering_details_dashboard(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        cameras = Camera.objects.filter(is_deleted='N')
        return render(request, 'PropelRapp/cameratampering_details.html', {'clusters': clusters, 'cameras': cameras, 'customers':customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
    return render(request, 'PropelRapp/cameratampering_details.html', {'clusters': clusters})


def profile(request):
    if request.method == 'POST':
        activeuser = Appuser.objects.get(user=request.user)
        form1 = ProfileForm(request.POST, instance=request.user)
        form2 = ProfileForm1(request.POST, request.FILES, instance=request.user)
        if form1.is_valid() and form2.is_valid():
            userform = form1.save()
            # customeform = form2.save()
            # customeform.user = userform
            # customeform.save()
            print(request.FILES)
            data = form2.cleaned_data

            print(data)
            mobile = data["mobile"]

            image = data["profile_pic"]
            # profile_pic = 'profile_image/' + str(image)
            # print(profile_pic)

            if image != None:
                Appuser.objects.filter(user=request.user).update(mobile=mobile, profile_pic=image)
                print(image)
                print(image.name)
                fs = FileSystemStorage()
                filename = fs.save(image.name, image)

                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)
            else:
                Appuser.objects.filter(user=request.user).update(mobile=mobile)

            messages.success(request, f"Profile Updated Successfully")
            return redirect('/PropelR/Profile')
        else:
            messages.error(request, form2.errors)
            return redirect('/PropelR/Profile')

    else:
        form1 = ProfileForm(instance=request.user)
        form2 = ProfileForm1(instance=request.user)
        app_user = Appuser.objects.get(user=request.user)
        return render(request, 'PropelRapp/main-Profile.html', {'form1': form1, 'form2': form2, 'app_user': app_user})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/PropelR/Profile')


    else:
        form = PasswordChangeCustomForm(request.user)
        app_user = Appuser.objects.get(user=request.user)
    return render(request, 'PropelRapp/change password.html', {'form': form, 'app_user': app_user})








# *********************  REPORT  ******************************




def count_visitors(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report visitors.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report visitors.html', {'clusters': clusters})


def age_gender(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report age-gender count.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report age-gender count.html', {'clusters': clusters})


def count_vehicles(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report vehicle.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report vehicle.html', {'clusters': clusters})


def repeat_vehicles_count(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report rvehicle.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report rvehicle.html', {'clusters': clusters})


def repeat_visitors_count(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report rvisitors.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report rvisitors.html', {'clusters': clusters})


def camera_tampering(request):
    if request.user.is_superuser:
        customers = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report camera tempering.html', {'customers': customers})
    else:
        activeuser = Appuser.objects.get(user=request.user)
        cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)
        clusters = Cluster.objects.filter(is_deleted='N', customer=cust_inst).order_by("-created_on", "-modified_on")
        return render(request, 'PropelRapp/report camera tempering.html', {'clusters': clusters})





# *********************  REPORT - DETAILS ******************************


@csrf_exempt
def visitor_details(request):
    visitors = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        url = "http://3.93.246.89:8000/GetData?chartType=People&cameraName={}&startDate={}&endDate={}".format(str(camera), str(startdate), str(enddate))
        response = requests.get(url)
        data1 = response.json()
        l = len(data1)
        i = 0
        people = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            people = data1[i][str(start)][str(camera)]
            dates.append(start)
            visitors.append(people)
            # visitors.append({"date" : start,"people": people})
            start += delta
            i += 1

    print(visitors)
    print()

    data = {
        'dates': dates,
        'visitors': visitors
    }

    return JsonResponse(data)


@csrf_exempt
def age_details(request):
    dates = []
    data_male = []
    data_female = []

    if request.is_ajax():
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
            data1 = response.json()

            data_male.append(data1[0][str(camera)]['Male'])
            data_female.append(data1[0][str(camera)]['Female'])


            dates.append(start)
            start += delta

    data = {'dates': dates, 'data_male': data_male, 'data_female': data_female}
    print(data_female)
    print(data_male)

    return JsonResponse(data)




















@csrf_exempt
def vehicle_details(request):
    vehicles = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
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
        vehicle = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            vehicle = data1[i][str(start)]['B3-Parking']
            dates.append(start)
            vehicles.append(vehicle)
            start += delta
            i += 1

    print(vehicles)
    print()

    data = {
        'dates': dates,
        'vehicles': vehicles
    }

    return JsonResponse(data)


@csrf_exempt
def repeat_vehicle_details(request):
    repeatvehicles = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
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
        vehicle = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            vehicle = data1[i][str(start)]['B3-Parking']
            dates.append(start)
            repeatvehicles.append(vehicle)
            start += delta
            i += 1

    print(repeatvehicles)
    print()

    data = {
        'dates': dates,
        'repeatvehicles': repeatvehicles
    }

    return JsonResponse(data)



@csrf_exempt
def repeat_visitor_details(request):
    repeatvisitors = []
    dates = []

    if request.is_ajax():
        x = request.POST.get('startdate', '')
        y = request.POST.get('enddate', '')
        camera = request.POST.get('camera', '')
        print(x)
        print(camera)



        (month_start, date_start, month_end, date_end) = (0, 0, 0, 0)

        temp_month_start = str(x.split("-")[1])
        temp_date_start = str(x.split("-")[2])

        if (len(temp_month_start) > 1):
            month_start = int(temp_month_start)
        else:
            month_start = int(temp_month_start[1])

        date_start = int(temp_date_start)

        temp_month_end = str(y.split("-")[1])
        temp_date_end = str(y.split("-")[2])

        if (len(temp_month_end) > 1):
            month_end = int(temp_month_end)
        else:
            month_end = int(temp_month_end[1])

        date_end = int(temp_date_end)

        startdate = date(2020, month_start, date_start)
        enddate = date(2020, month_end, date_end)

        start = startdate
        end = enddate

        url = "http://3.93.246.89:8000/GetData?chartType=People&cameraName={}&startDate={}&endDate={}".format(str(camera), str(startdate), str(enddate))
        response = requests.get(url)
        data1 = response.json()
        l = len(data1)
        i = 0
        people = 0
        delta = timedelta(days=1)

        while start <= end and i < l:
            people = data1[i][str(start)][str(camera)]
            dates.append(start)
            repeatvisitors.append(people)
            # visitors.append({"date" : start,"people": people})
            start += delta
            i += 1

    print(repeatvisitors)
    print()

    data = {
        'dates': dates,
        'repeatvisitors': repeatvisitors
    }

    return JsonResponse(data)



@csrf_exempt
def camera_tampering_details(request):
    pass






def user_list(request):
    if request.user.is_superuser:  # for super admin we want to show all the customers list
        user_list = Appuser.objects.filter(is_deleted='N', is_superuser='N').order_by("-created_on", "-modified_on")
    else:
        activeuser = Appuser.objects.get(
            user=request.user)  # for a particular customer we will show only the customer that belong to same customer organization
        cust_inst = Cust_org.objects.filter(cust_org=activeuser.customer)[0]
        user_list = Appuser.objects.filter(is_deleted='N', is_superuser='N', customer=cust_inst).order_by("-created_on", "-modified_on")

    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/userlist.html', {'users': users})


def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if request.user.is_superuser:
            super_admin_user_form = SuperAdminUserForm(request.POST)
            if user_form.is_valid() and super_admin_user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                app_user = super_admin_user_form.save(commit=False)
                app_user.user = user
                app_user.created_by = 'Shyena Tech'
                app_user.modified_by = 'Shyena Tech'
                app_user.save()
                messages.success(request, 'User saved successfully.')
                return redirect('/PropelR/Admin/User')
            else:
                print(user_form.errors)
                print(super_admin_user_form.errors)
                messages.error(request, user_form.errors)
                messages.error(request, super_admin_user_form.errors)
                return redirect('/PropelR/Admin/User/Add_User')


        else:  # ther user is not a superuser
            other_user_form = OtherUserForm(request.POST)
            if user_form.is_valid() and other_user_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                activeuser = Appuser.objects.get(user=request.user)
                cust_inst = Cust_org.objects.get(cust_org=activeuser.customer)

                app_user = other_user_form.save(commit=False)
                app_user.customer = cust_inst
                app_user.user = user
                app_user.created_by = request.user.username
                app_user.modified_by = request.user.username
                app_user.save()
                messages.success(request, 'User saved successfully.')
                return redirect('/PropelR/Admin/User')
            else:
                print(user_form.errors)
                print(other_user_form.errors)
                messages.error(request, user_form.errors)
                messages.error(request, other_user_form.errors)
                return redirect('/PropelR/Admin/User/Add_User')

    else:
        roles = Role.objects.filter(is_deleted='N')
        customers = Cust_org.objects.filter(is_deleted='N')
        user_form = UserForm()
        super_admin_user_form = SuperAdminUserForm()
        other_user_form = OtherUserForm()
        return render(request, 'PropelRapp/add user.html',
                      {'roles': roles, 'customers': customers, 'user_form': user_form, 'super_admin_user_form': super_admin_user_form,
                       'other_user_form': other_user_form})


def edit_user(request, user_id):
    # user = Appuser.objects.get(pk=user_id)
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Admin/User')
    else:
        form = UserForm(instance=user)
        return render(request, 'PropelRapp/user_edit.html', {'form': form})


def delete_user(request, user_id):
    user = get_object_or_404(Appuser, pk=user_id)
    user.is_deleted = 'Y'
    user.save()
    return redirect('/PropelR/Admin/User')


def authorization(request):
    return render(request, 'PropelRapp/roles.html')


'''
def stream_response(request):
    resp = HttpResponse(stream_response_generator(), content_type='text/html')
    return resp


def stream_response_generator():
    yield "<html><body>\n"
    for x in range(1, 11):
        yield "<div>%s</div>\n" % x
        yield " " * 1024  # Encourage browser to render incrementally
        time.sleep(1)
    yield "</body></html>\n"
'''


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def view_feed(request):
    if request.method == 'POST':

        camera = request.POST.get('camera')
        cluster = request.POST.get('clust')

        print(cluster)

        try:
            camera_inst = Camera.objects.get(camname=camera)
        except Camera.DoesNotExist:
            messages.error(request, 'Select a Camera')
            clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
            return render(request, 'PropelRapp/view_feed.html', {'clusters': clusters})

        id = camera_inst.pk

        ip = camera_inst.camip
        ip = str(ip)

        print(ip)
        print(camera)
        print(cluster)

        # cap = cv2.VideoCapture('rtsp://Aditya:1234@192.168.1.101:7777')
        # cap = cv2.VideoCapture(ip)

        opt = request.POST.get('submit')
        if opt == 'view':

            try:
                return StreamingHttpResponse(gen(VideoCamera(ip)), content_type="multipart/x-mixed-replace;boundary=frame")
            except HttpResponseServerError as e:
                print("aborted")

            '''while (True):

                ret, frame = cap.read()
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()'''

        elif opt == 'stop':
            pass
    else:

        if request.user.is_superuser:
            clusters = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
            cameras = Camera.objects.filter(is_deleted='N')
            return render(request, 'PropelRapp/view_feed.html', {'clusters': clusters, 'cameras': cameras})
        else:
            clusters = Cluster.objects.filter(is_deleted='N', created_by=request.user.username).order_by("-created_on", "-modified_on")
            cluster_ids = set(map(lambda x: x.pk, clusters))
            cameras = list(Camera.objects.filter(cluster_id__in=cluster_ids))
            return render(request, 'PropelRapp/view_feed.html', {'clusters': clusters, 'cameras': cameras})


def subscription(request):
    return render(request, 'PropelRapp/subscription.html')


def subscription_plan(request):
    return render(request, 'PropelRapp/subscription plan.html')


def summary(request):
    return render(request, 'PropelRapp/summary.html')


# ****************************       Super-Admin   *************************


def algo_list(request):
    algo_list = Algo_master.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(algo_list, 5)

    try:
        algorithms = paginator.page(page)
    except PageNotAnInteger:
        algorithms = paginator.page(1)
    except EmptyPage:
        algorithms = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/algorithm table.html', {'algorithms': algorithms})


def add_algo(request):
    if request.method == 'POST':
        algo = request.POST['algo_name']
        algo_desc = request.POST['descr']
        # created_by = request.user.username
        # modified_by = request.user.username
        new_algo = Algo_master(algo=algo, algo_desc=algo_desc)
        new_algo.save()
        return redirect('/PropelR/Super-Admin/algorithms')
    else:
        return render(request, 'PropelRapp/algorithm.html')


def edit_algo(request, algo_id):
    algo = Algo_master.objects.get(pk=algo_id)
    if request.method == 'POST':
        form = AlgoithmForm(request.POST, instance=algo)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Super-Admin/algorithms')
    else:
        form = AlgoithmForm(instance=algo)
        return render(request, 'PropelRapp/algo_edit.html', {'form': form})


def delete_algo(request, algo_id):
    algo = get_object_or_404(Algo_master, pk=algo_id)
    algo.is_deleted = 'Y'
    algo.save()
    return redirect('/PropelR/Super-Admin/algorithms')


def customer_list(request):
    pass
    customer_list = Cust_org.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(customer_list, 5)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/customer table.html', {'customers': customers})


def add_customer(request):
    if request.method == 'POST':
        cust_org = request.POST['cust_org']
        cust_org_acro = request.POST['cust_acro']
        created_by = request.user.username
        modified_by = request.user.username
        bill_plan = request.POST['bill']
        status = request.POST['status']
        date_str = request.POST['onboard']

        bill_plan_inst = Bill_plan.objects.get(billplan=bill_plan)
        temp_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_customer = Cust_org(cust_org=cust_org, cust_org_acro=cust_org_acro, status=status, bill_plan=bill_plan_inst, onboard_date=temp_date)
        new_customer.save()
        return redirect('/PropelR/Super-Admin/Customers')
    else:
        bills = Bill_plan.objects.filter(is_deleted='N')
        '''
        try:
            last_inserted = Cust_org.objects.order_by('-id')[0]
            customerid = last_inserted.id
        except IndexError:
            customerid = 1
        except Cust_org.DoesNotExist:
            customerid = 1'''

        return render(request, 'PropelRapp/customer.html', {'bills': bills})


def edit_customer(request, customer_id):
    customer = Cust_org.objects.get(pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Super-Admin/Customers')
    else:
        form = CustomerForm(instance=customer)
        return render(request, 'PropelRapp/customer_edit.html', {'form': form})


def delete_customer(request, customer_id):
    customer = get_object_or_404(Cust_org, pk=customer_id)
    customer.is_deleted = 'Y'
    customer.save()
    return redirect('/PropelR/Super-Admin/Customers')


def bill_list(request):
    bill_list = Bill_plan.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(bill_list, 5)

    try:
        bills = paginator.page(page)
    except PageNotAnInteger:
        bills = paginator.page(1)
    except EmptyPage:
        bills = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/Bill Plan Table.html', {'bills': bills})


def add_bill(request):
    if request.method == 'POST':
        billplan = request.POST['billplan']
        billplan_cd = request.POST['billplan_cd']
        created_by = request.user.username
        modified_by = request.user.username
        new_bill = Bill_plan(billplan=billplan, billplan_cd=billplan_cd)
        new_bill.save()
        return redirect('/PropelR/Super-Admin/Bill-Plan')
    else:
        return render(request, 'PropelRapp/BillPlan.html')


def edit_bill(request, bill_id):
    bill = Bill_plan.objects.get(pk=bill_id)
    if request.method == 'POST':
        form = BillPlanForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Super-Admin/Bill-Plan')
    else:
        form = BillPlanForm(instance=bill)
        return render(request, 'PropelRapp/bill_edit.html', {'form': form})


def delete_bill(request, bill_id):
    bill = get_object_or_404(Bill_plan, pk=bill_id)
    bill.is_deleted = 'Y'
    bill.save()
    return redirect('/PropelR/Super-Admin/Bill-Plan')


def menu_list(request):
    menu_list = Menu.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(menu_list, 5)

    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/Menu List.html', {'menus': menus})


def add_menu(request):
    if request.method == 'POST':
        menu = request.POST['menu']
        created_by = request.user.username
        modified_by = request.user.username
        new_menu = Menu(menu=menu)
        new_menu.save()
        return redirect('/PropelR/Super-Admin/Menu')
    else:
        return render(request, 'PropelRapp/Menu.html')


def edit_menu(request, menu_id):
    menu = Menu.objects.get(pk=menu_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Super-Admin/Menu')
    else:
        form = MenuForm(instance=menu)
        return render(request, 'PropelRapp/menu_edit.html', {'form': form})


def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    menu.is_deleted = 'Y'
    menu.save()
    return redirect('/PropelR/Super-Admin/Menu')


def submenu_list(request):
    submenu_list = Submenu.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(submenu_list, 5)

    try:
        submenus = paginator.page(page)
    except PageNotAnInteger:
        submenus = paginator.page(1)
    except EmptyPage:
        submenus = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/Sub Menu List.html', {'submenus': submenus})


def add_submenu(request):
    if request.method == 'POST':
        submenu = request.POST['submenu']
        menu = request.POST['menu']
        created_by = request.user.username
        modified_by = request.user.username
        menu_inst = Menu.objects.get(menu=menu)
        new_submenu = Submenu(submenu=submenu, menu=menu_inst)
        new_submenu.save()
        return redirect('/PropelR/Super-Admin/SubMenu')
    else:
        menus = Menu.objects.all()
        return render(request, 'PropelRapp/SubMenu.html', {'menus': menus})


def edit_submenu(request, submenu_id):
    submenu = Submenu.objects.get(pk=submenu_id)
    if request.method == 'POST':
        form = SubMenuForm(request.POST, instance=submenu)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Super-Admin/SubMenu')
    else:
        form = SubMenuForm(instance=submenu)
        return render(request, 'PropelRapp/submenu_edit.html', {'form': form})


def delete_submenu(request, submenu_id):
    submenu = Submenu(Bill_plan, pk=submenu_id)
    submenu.is_deleted = 'Y'
    submenu.save()
    return redirect('/PropelR/Super-Admin/SubMenu')


# ************************  Admin  *******************************


def role_list(request):
    role_list = Role.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(role_list, 5)

    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/Role List.html', {'roles': roles})


def add_role(request):
    if request.method == 'POST':
        role = request.POST['role']
        role_desc = request.POST['role_desc']
        created_by = request.user.username
        modified_by = request.user.username

        new_role = Role(role=role, role_desc=role_desc)
        new_role.save()

        List = []

        for menu in Menu.objects.all():  # Fetching the selected checkboxes' values
            if menu.is_deleted == 'N':
                x = str(menu) + '[]'
                r = request.POST.getlist(x)
                # print(r)
                if (len(r) != 0):
                    List.append(r)

        print(List)

        for i in List:
            menu_name = i.pop(0)
            print(menu_name)
            for j in i:
                submenu_name = j
                print(submenu_name)
                menu_inst = Menu.objects.get(menu=menu_name)
                for x in Submenu.objects.all():
                    if x.menu == menu_inst and x.submenu == submenu_name:
                        print(x)
                        new_role_detail = Roledetail(menu=menu_inst, submenu=x, role=new_role)
                        new_role_detail.save()

        return redirect('/PropelR/Admin/Roles')
    else:
        menus = Menu.objects.all()
        submenus = Submenu.objects.all()

        menus = Menu.objects.all()
        submenus = Submenu.objects.all()

        return render(request, 'PropelRapp/Role.html', {'menus': menus, 'submenus': submenus})


def edit_role(request, role_id):
    role = Role.objects.get(pk=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Admin/Roles')
    else:
        form = RoleForm(instance=role)
        return render(request, 'PropelRapp/role_edit.html', {'form': form})


def role_details(request, role_id):
    role = Role.objects.get(pk=role_id)
    if request.method == 'POST':
        form = RoleDetailForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Admin/Roles')
    else:
        form = RoleDetailForm(instance=role)
        return render(request, 'PropelRapp/role_detail.html', {'form': form})


def delete_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    role.is_deleted = 'Y'
    role.save()
    return redirect('/PropelR/Admin/Roles')


def cluster_list(request):
    cluster_list = Cluster.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(cluster_list, 5)

    try:
        clusters = paginator.page(page)
    except PageNotAnInteger:
        clusters = paginator.page(1)
    except EmptyPage:
        clusters = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/cluster table.html', {'clusters': clusters})


def add_cluster(request):
    if request.method == 'POST':
        cluster_name = request.POST['cluster_name']
        description = request.POST['descr']
        created_by = request.user.username
        new_cluster = Cluster(cluster_name=cluster_name, description=description)
        new_cluster.save()
        return redirect('/PropelR/Admin/Configuration/Cluster')
    else:
        return render(request, 'PropelRapp/cluster.html')


def edit_cluster(request, cluster_id):
    cluster = Cluster.objects.get(pk=cluster_id)
    if request.method == 'POST':
        form = ClusterForm(request.POST, instance=cluster)
        if form.is_valid():
            form.save()
            cluster.modified_by = request.user.username
            cluster.save()
            return redirect('/PropelR/Admin/Configuration/Cluster')
    else:
        form = ClusterForm(instance=cluster)
        return render(request, 'PropelRapp/cluster_edit.html', {'form': form})


def delete_cluster(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)
    cluster.is_deleted = 'Y'
    cluster.save()
    return redirect('/PropelR/Admin/Configuration/Cluster')


def camera_table(request):
    camera_list = Camera.objects.filter(is_deleted='N').order_by("-created_on", "-modified_on")
    page = request.GET.get('page', 1)
    paginator = Paginator(camera_list, 5)

    try:
        cameras = paginator.page(page)
    except PageNotAnInteger:
        cameras = paginator.page(1)
    except EmptyPage:
        cameras = paginator.page(paginator.num_pages)

    return render(request, 'PropelRapp/camera table.html', {'cameras': cameras})


def add_camera(request):
    if request.method == 'POST':
        camname = request.POST['camname']
        camip = request.POST['camip']
        x1_cord = request.POST['x1']
        y1_cord = request.POST['y1']
        x2_cord = request.POST['x2']
        y2_cord = request.POST['y2']
        cluster = request.POST['clust']
        algo_type = request.POST['algo']

        clusterinst = Cluster.objects.get(cluster_name=cluster)

        new_camera = Camera(camname=camname, camip=camip, x1_cord=x1_cord, y1_cord=y1_cord, x2_cord=x2_cord, y2_cord=y2_cord, cluster=clusterinst,
                            algo_type=algo_type)
        new_camera.save()

        return redirect('/PropelR/Admin/Configuration/Camera')
    else:
        clusters = Cluster.objects.filter(is_deleted='N')

        '''
       try:
            last_inserted = Camera.objects.order_by('-id')[0]
            cameraid = last_inserted.id
        except IndexError:
            cameraid = 1
        except Camera.DoesNotExist:
            cameraid = 1'''

        return render(request, 'PropelRapp/Camera.html', {'clusters': clusters})


def edit_camera(request, camera_id):
    camera = Camera.objects.get(pk=camera_id)
    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            form.save()
            return redirect('/PropelR/Admin/Configuration/Camera')
    else:
        form = CameraForm(instance=camera)
        return render(request, 'PropelRapp/camera_edit.html', {'form': form})


def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, pk=camera_id)
    camera.is_deleted = 'Y'
    camera.save()
    return redirect('/PropelR/Admin/Configuration/Camera')


def other_config(request):
    return render(request, 'PropelRapp/other-config.html')  # REMAINING


def logout_request(request):
    logout(request)
    return redirect('/PropelR/')
