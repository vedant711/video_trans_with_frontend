from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import messages
# import urllib.request
from django.views.decorators.csrf import csrf_exempt
# import gdown
from .models import Logs
import os,shutil
# from .forms import UploadFileForm
# from .forms import UploadFileForm
from datetime import datetime
# import re
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.views import APIView
# from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from threading import Thread
import subprocess
import hashlib
import json
# from humanize import naturalsize

# Create your views here.

def handle_uploaded_file(f,id,ext):
    print('Uploading...')
    with open(f'trans/static/uploaded/{id}.{ext}','wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def video_processing(url,id):
    try:
        # log1 = Logs.objects.get(start_datetime = st_dt,source=url)
        # # global id
        # id=log1.id
        # print(id)
        # print(url)
        # os.chdir('/root/video_trans/translation_tool/trans')
        os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans')


        process = f'python3 pivot_control.py {id} &'
        p = subprocess.Popen(process,shell=True)
        return 'success'
    except:
        return 'failed'

    
    



@login_required(login_url='/')
def user_token_view(request):
    try:
        token = Token.objects.create(user=request.user)
        return render(request, 'user_token.html', {'token': token.key})
    except:
        return HttpResponse('Already created the API key')

def signup1(request):
    if request.method=="POST":
        username=request.POST['username']       
        pass1=request.POST['password']
        # pass2=request.POST['password1']
        # if pass1==pass2:
        if User.objects.filter(username=username).exists():
            messages.info(request,'OOPS! Usename already taken')
            return render(request,'create_acc.html')            
        else:
            user=User.objects.create_user(username=username,password=pass1)
            user.save()
            messages.info(request,'Account created successfully!!')
            return render(request,'login.html')
    return render(request,'create_acc.html')

def index(request):
    if request.user.is_authenticated: return redirect(f'/view/{request.user}')
    else:
        if request.method=='POST':
            username=request.POST['username']
            pass1=request.POST['password']
            user=auth.authenticate(username=username,password=pass1)
            if user is not None:
                auth.login(request,user)
                # return render(request,'index.html')
                # print(user)
                # return redirect('/auth_token')
                return redirect(f'/view/{user}')
            else:
                messages.info(request,'Invalid credentials')
                return render(request,'login.html')
        return render(request,'login.html')

@login_required(login_url='/')
def upload(request):
    context = {'user':request.user}
    if request.method=='POST':
        url = request.POST['url']
        callback = request.POST['callback']
        # os.chdir('/root/video_trans/translation_tool')
        os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool')

        log = Logs()
        log.start_datetime= str(datetime.now())
        st_dt = log.start_datetime
        log.status = 'waiting for video'
        log.source = url
        log.callback_url = callback
        log.user = request.user
        log.save()
        log1 = Logs.objects.get(start_datetime = st_dt,source=url,callback_url=callback)
        id = log1.id
        log1.queueId = hashlib.md5(str(id).encode("utf-8")).hexdigest()
        log1.save()

        # form = UploadFileForm(request.POST, request.FILES)
        # path = request.FILES['file']
        # if form.is_valid():
        # print(path)
            # global file
            
        # file = request.FILES['file']
        # print(file.name)
        # st_dt = form['date']
        # log1 = Logs.objects.get(start_datetime = st_dt)
        # global id
        # id=log1.id
        # ext = file.name.split('.')[-1]
        # log1.path = f'../{id}.{ext}'
        # log1.save()
        # handle_uploaded_file(file,id,ext)
        os.chdir('trans')
        # os.system(f'python3 pivot_control.py {log1.path} {id}')
        mess = video_processing(url,id)
        # tracking_url = ''
        if mess == 'success':
            messages.info(request,'Video Translation started successfully')
            tracking_url = f'/track/{log1.queueId}'
        else:
            messages.info(request, 'There was some error processing the video')
            tracking_url =''
            # os.chdir('static/uploaded/')
    # context = {'form' : UploadFileForm()}
        context = {'tracking_url': tracking_url,'queueId':log1.queueId,'user':request.user}
    return render(request,'index.html',context)
    # return render(request,'index.html')
    

@csrf_exempt
def api(request):
    try:
        # url = request.GET.get('url')
        # callback_url = request.GET.get('callback')
        # print(url)
        if request.method=='POST':
            # url = request.POST.get('url')
            # print(url)
            try:
                # username = request.headers['username']
                # password= request.headers['password']

                # user=auth.authenticate(username=username,password=password)
                url = request.POST['url']
                callback_url = request.POST['callback']
                # print(request.headers)
                # print(request.POST)
                # for obj in request:
                #     print(obj)
                    # print(request.obj)
                # print(request.__dict__)
                # print(url,callback_url)

                # if user is not None:
                    
                    # print(request.headers)
                auth_key = request.headers['Authorization']
                # token = Token.objects.get(user_id=user.id)
                # if auth_key == token.key:
                keys = ['60ea74a6edd466cf71852da61e618f470ed35208']
                if auth_key in keys:
                    os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool')
                    log = Logs()
                    log.start_datetime= str(datetime.now())
                    st_dt = log.start_datetime
                    log.status = 'waiting for video'
                    log.source = url
                    log.callback_url = callback_url
                    log.save()
                    log1 = Logs.objects.get(start_datetime = st_dt,source=url,callback_url=callback_url)
                    # print('hi')
                    id = log1.id
                    log1.queueId = hashlib.md5(str(id).encode("utf-8")).hexdigest()
                    # print(log1.queueId)
                    
                    log1.save()
                    # print(log1)
                    #
                    # file = 
                    # log1 = Logs.objects.get(start_datetime = st_dt)
                    #     # global id
                    # id=log1.id
                    # # print(id)
                    # # print(url)
                    # os.chdir('trans/static/uploaded')
                    # # print(os.getcwd())
                    # urllib.request.urlretrieve(url, f'{id}.mp4')
                    # # gdown.download(url,f'{id}.mp4',quiet=True)
                    # ext = 'mp4'
                    # # print(ext)
                    # log1.path = f'../{id}.{ext}'
                    # log1.save()
                    # # handle_uploaded_file(file,id,ext)
                    # os.chdir('/root/video_trans/translation_tool/trans/')
                    # os.system(f'python3 pivot_control.py {log1.path} {id}')
                    # t=Thread(target=video_processing,args=(url,st_dt,))
                    # t.start()
                    mess = video_processing(url,id)
                    # return HttpResponse('Processing the video')
                    if mess == 'success':
                        return JsonResponse({'status':200,'text':'Video Processing','queueid':log1.queueId})
                    else:
                        return JsonResponse({'status':300,'text':'Unexpected Error Occured','queueid':0})
                else:
                    return JsonResponse({'status':305,'text':'Invalid Auth Key','queueid':0})
                # else:
                #     return JsonResponse({'status':305,'text':'Invalid Username or Password','queueid':0})
            except:
                return JsonResponse({'status':300,'text':'Invalid Input','queueid':0})
    except:
        pass

@csrf_exempt
def check(request):
    try:
        if request.method == 'POST':
            # out_url = request.GET.get('url')
            received_data = json.loads(request.body.decode("utf-8"))
            print(received_data)
            return JsonResponse({'status':200,'message':'Received the request','received_data':[received_data['output'],received_data['queue_id']]})
        return HttpResponse('waiting for response')
    except:
        return JsonResponse({'status':500,'message':'Unexpected Error Occured'})

@login_required(login_url='/')    
def track(request,queueId):
    try:
        log = Logs.objects.get(queueId=queueId)
        # print(request.user,log.user)
        # print(type(request.user),type(log.user))
        if log.user == str(request.user):
            id = log.id
            file = open(f'/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded/logs/log{id}.txt','r',encoding='utf-8')
            output = list(file.readlines())
            file.close()
            context = {'output':output,'queueId':queueId}
        else:
            messages.info(request,"Bad Request!\nYou cannot access other user's request.")
            return redirect(f'/view/{request.user}')
    except:
        context = {'output':'','queueId':queueId}
    return render(request,'track.html',context)

@login_required(login_url='/')
def indi_page(request,user):
    logs = Logs.objects.filter(user=request.user).all()
    context={'logs':logs}
    # print(logs)
    return render(request,'indi_page.html',context)

def logout_view(request):
    try:
        logout(request)
        return redirect('/')
    except:
        messages.info(request,'Unable to logout')
