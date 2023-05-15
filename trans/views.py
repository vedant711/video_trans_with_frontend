from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import re
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
from django.contrib.admin.views.decorators import staff_member_required
import subprocess
import hashlib
import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def handle_uploaded_file(f,id,ext):
    print('Uploading...')
    with open(f'trans/static/uploaded/{id}.{ext}','wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


import logging

def foo(request):
    # logging.basicConfig(level=logging.INFO)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    some_logger = logging.getLogger(__name__)
    some_logger.info('Your log message... IP:' + ip)
    # print(some_logger)

def video_processing(url,id):
    try:
        # log1 = Logs.objects.get(start_datetime = st_dt,source=url)
        # # global id
        # id=log1.id
        # print(id)
        # print(url)
        # os.chdir('/root/video_trans/translation_tool/trans')
        os.chdir(os.path.join(BASE_DIR,'trans'))
        # os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans')


        process = f'python3 pivot_control.py {id} &'
        p = subprocess.Popen(process,shell=True)
        return 'success'
    except:
        return 'failed'

    
    



@login_required(login_url='/')
def user_token_view(request):
    foo(request)
    try:
        token = Token.objects.create(user=request.user)
        return render(request, 'user_token.html', {'token': token.key})
    except:
        return HttpResponse('Already created the API key')

@csrf_exempt
@staff_member_required(login_url='/')
def signup1(request):
    foo(request)
    if request.method=="POST":
        username=request.POST['username']       
        pass1=request.POST['password']
        # pass2=request.POST['password1']
        # if pass1==pass2:
        if User.objects.filter(username=username).exists():
            messages.info(request,'OOPS! Usename already taken')
            # return render(request,'create_acc.html')            
        else:
            user=User.objects.create_user(username=username,password=pass1)
            user.save()
            messages.info(request,'Account created successfully!!')
            # return render(request,'login.html')
        return redirect('/adminportal')

@csrf_exempt
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
                if request.user.is_staff:
                    return redirect(f'/adminportal')
                else:
                    return redirect(f'/view/{user}')
            else:
                messages.info(request,'Invalid credentials')
                return render(request,'login.html')
        return render(request,'login.html')

@login_required(login_url='/')
def upload(request):
    foo(request)
    context = {'user':request.user}
    if request.method=='POST':
        url = request.POST['url']
        email = request.POST['email']
        # os.chdir('/root/video_trans/translation_tool')
        # os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool')
        os.chdir(BASE_DIR)

        log = Logs()
        log.start_datetime= str(datetime.now())
        st_dt = log.start_datetime
        log.status = 'waiting for video'
        log.source = url
        log.email = email
        log.user = request.user
        log.save()
        log1 = Logs.objects.get(start_datetime = st_dt,source=url,email=email)
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
            return redirect(f'/view/{request.user}')
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
    foo(request)
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
                    # os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool')
                    os.chdir(BASE_DIR)
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
    foo(request)
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
    foo(request)
    try:
        log = Logs.objects.get(queueId=queueId)
        # print(request.user,log.user)
        # print(type(request.user),type(log.user))
        if log.user == str(request.user):
            id = log.id
            # file = open(f'/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded/logs/log{id}.txt','r',encoding='utf-8')
            file = open(os.path.join(BASE_DIR,f'trans/static/uploaded/logs/log{id}.txt'),'r',encoding='utf-8')
            output = file.read()
            file.close()
            begin,end=False,False
            if 'Process Begins' in output:begin = True
            if 'Process Ends' in output:end = True

            # begin=True if 'Process Begins' in output else False
            # else:begin=False
            translation_begin,translation_end,tts_begin,tts_end = False,False,False,False
            langs = ['hi','fr','zh-CN','pt','de','pl','ru','es','sv','el']
            trans_start,trans_end,textts_start,textts_end = {},{},{},{}
            # for line in output:
            for lang in langs:
                if f'{lang} translation start = ' in output:
                    if not translation_begin: translation_begin = True
                    if lang=='zh-CN': trans_start['zh'] =re.findall(f'{lang} translation start = .*',output)[0].replace(f'{lang} translation start = ','')
                    else:trans_start[lang]=re.findall(f'{lang} translation start = .*',output)[0].replace(f'{lang} translation start = ','')
                    # trans_start[lang] = x
                if f'{lang} translation complete = ' in output:
                    if not translation_end: translation_end = True
                    if lang=='zh-CN':trans_end['zh']=re.findall(f'{lang} translation complete = .*',output)[0].replace(f'{lang} translation complete = ','')
                    else:trans_end[lang]=re.findall(f'{lang} translation complete = .*',output)[0].replace(f'{lang} translation complete = ','')
                    # trans_end[lang] = x
                if f'{lang} tts start = ' in output:
                    if not tts_begin: tts_begin=True
                    if lang=='zh-CN':textts_start['zh'] = re.findall(f'{lang} tts start = .*',output)[0].replace(f'{lang} tts start = ','')
                    else:textts_start[lang] = re.findall(f'{lang} tts start = .*',output)[0].replace(f'{lang} tts start = ','')
                if f'{lang} tts complete = ' in output:
                    if not tts_end: tts_end=True
                    if lang=='zh-CN':textts_end['zh'] = re.findall(f'{lang} tts complete = .*',output)[0].replace(f'{lang} tts complete = ','')
                    else:textts_end[lang] = re.findall(f'{lang} tts complete = .*',output)[0].replace(f'{lang} tts complete = ','')
            # context = {'output':output,'queueId':queueId}
            # print(tts_begin)
            output = {'begin':begin,'translation_begin':translation_begin,'translation_end':translation_end,'langs':langs,'tts_begin':tts_begin,'tts_end':tts_end,'end':end}
            context = {'queueId':queueId,'output':output,'trans_start':trans_start,'trans_end':trans_end,'textts_start':textts_start,'textts_end':textts_end,'user':request.user}
        else:
            messages.info(request,"Bad Request!\nYou cannot access other user's request.")
            return redirect(f'/view/{request.user}')
    except:
        context = {'output':'','queueId':queueId}
    return render(request,'track.html',context)

@csrf_exempt
@login_required(login_url='/')
def indi_page(request,user):
    foo(request)
    context = {}
    if request.method == 'POST':
    # logs = Logs.objects.filter(user=request.user).all()
        try:
            dt = request.POST['date']
            status = request.POST['status']
        except:
            # print(request.body)
            # data = request.body.decode()
            from ast import literal_eval
            data = literal_eval(request.body.decode('utf-8'))
            dt = data['date']
            status = data['status']
        # print(dt)
        # print(status)
        if status=='all':
            logs = Logs.objects.filter(user=request.user,start_datetime__icontains=dt).all()
            # print(logs)
        elif status =='running':
            logs = Logs.objects.filter(user=request.user,status__in=['running','waiting for video','uploading video'],start_datetime__icontains=dt).all()
        else:
            logs = Logs.objects.filter(user=request.user,status=status,start_datetime__icontains=dt).all()
        # for log in logs:
        #     print(log.start_datetime)
        # print(logs)
        context={'logs':logs,'dt':dt,'status':status}
    # print(logs)
    # print(logs)
    return render(request,'indi_page.html',context)

def logout_view(request):
    foo(request)
    try:
        logout(request)
        return redirect('/')
    except:
        messages.info(request,'Unable to logout')


def error404(request,exception):
    return render(request,'404.html')

def error500(request):
    return render(request,'500.html')

@staff_member_required(login_url='/')
def admin_portal(request):
    all_users = User.objects.all()
    context={'user':request.user,'all':all_users}
    return render(request,'admin.html',context)

@staff_member_required(login_url='/')
def remove_user(request,user):
    User.objects.get(username=user).delete()
    return redirect('/adminportal')