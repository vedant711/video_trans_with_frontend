import os
from pydub.utils import make_chunks
from pydub import AudioSegment
from vid_wav import vid_to_wav
from translate import threads
from audio import threads_audio
from merge import merge
from datetime import datetime
# import threading
import sys
import mysql.connector
# import time
import shutil
import subprocess
from threading import Thread
from audio_merge import merge_audio_threads
import requests
import json
from dotenv.main import load_dotenv
# import os


def waiting_requests(cursor):
    cursor.execute("SELECT * FROM logs WHERE status='waiting' ORDER BY id")
    return cursor.fetchall()

def running_requests(cursor):
    cursor.execute("SELECT * FROM logs WHERE status='running'")
    return cursor.fetchall()

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def getToken():
    load_dotenv()

    refresh_token = os.environ['REFRESH_TOKEN']
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    oauth = 'https://www.googleapis.com/oauth2/v4/token' # Google API oauth url
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret, 
        'refresh_token': refresh_token,
    }

    token = requests.post(oauth, headers=headers, data=data)
    _key = json.loads(token.text)
    return _key['access_token']


if __name__ == '__main__':
    blockPrint()
    os.chdir('static/uploaded')

    mydb = mysql.connector.connect(
        host="localhost",
        auth_plugin='mysql_native_password',
        user="root",
        password="12345678",
        database="translator1",
    )

    mycursor = mydb.cursor()

    mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    orig_path = sys.argv[1]
    id = sys.argv[2]

    # print(orig_path,id)

    mycursor.execute(f"SELECT * FROM logs WHERE id={id}")
    # return cursor.fetchall()
    curr_status = mycursor.fetchone()[1]
    # print(curr_status)

    # if curr_status=='waiting':
    mycursor.execute(f'UPDATE logs SET status="running" WHERE id = {id}')
    mydb.commit()


    # sql = "INSERT INTO logs (status,start_datetime,path) VALUES (%s, %s, %s)"
    # d= str(datetime.now())
    # val = ("running", d, orig_path)
    # mycursor.execute(sql, val)
    # mydb.commit()

    # mycursor.execute(f"SELECT id FROM logs WHERE start_datetime='{d}'")
    # id = mycursor.fetchone()[0]
    try: os.mkdir('logs')
    except(FileExistsError): pass
    txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
    txt.write('Process Begins\n')
    txt.close()

    try: os.mkdir(f'audio_analyze{id}')
    except(FileExistsError): pass

    os.chdir(f'audio_analyze{id}')
    # orig_path = '../java.mp4'
    try: vid_to_wav(id,orig_path)
    except PermissionError: sys.exit()
    except FileNotFoundError: sys.exit()

    iter_factor = 0
    path=f'vid.wav'
    try:
        aud = AudioSegment.from_file(path,'wav')
        chunk_length_ms = 5000
        chunks = make_chunks(aud, chunk_length_ms)
        os.remove('vid.mp3')
        os.remove('vid.wav')
    except PermissionError:
        # print('Thank You for Using Our Service')
        sys.exit()
    except FileNotFoundError:
        # print('Thank You for Using Our Service')
        sys.exit()

    # langs = ['hi','gu','fr','ko','bn','zh-CN','pt','de','pl','ar','ru','es','sv','la','el']
    langs = ['hi','fr','zh-CN','pt','de','pl','ru','es','sv','el']
    # langs = ['hi']
    translated_files = {}

    exit_flag=0
    csv_file = open('op.csv','a+', encoding='utf-16')
    csv_file.close()
    # check_list = [[0 for i in range(len(langs))] for j in range(len(chunks))]
    silence_index=[]
    try:
        # txt = open(f'../logs/log{id}.txt','a+',encoding='utf-8')
        # txt.write('Process Starts\n')
        # txt.close()
        threads(id,chunks,langs,silence_index,exit_flag)
        threads_audio(id,langs,silence_index,exit_flag)
        merge_audio_threads(langs,silence_index)
        # print(exit_flag)
        merge(id,langs,orig_path)
        # print(id)
        # print(os.path.exists(f'/root/video_trans/translation_tool/trans/static/uploaded/output{id}/final_trans.mkv'))
        # if os.path.exists(f'/root/video_trans/translation_tool/trans/static/uploaded/output{id}/final_trans.mkv'):
        if os.path.exists(f'/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded/output{id}/final_trans.mkv'):
            # print('HI')
            mycursor.execute(f'UPDATE logs SET status="uploading video" WHERE id={int(id)}')
            mydb.commit()
            mycursor.execute(f"SELECT * FROM logs WHERE id={id}")
            mycursor_obj_output = mycursor.fetchone()
            callback_url,queue_id = mycursor_obj_output[5],mycursor_obj_output[6]
            print(callback_url,queue_id)
            try:
                # load_dotenv()

                # api_key = os.environ['API_KEY']
                api_key=getToken()
                # print(api_key)
                headers = {
                    "Authorization":f"Bearer {api_key}"
                }
                para={
                    'name': f'final_trans{id}.mkv'
                }
                files = {
                    'data':('metadata',json.dumps(para),'application/json;charset=UTF-8'),
                    'file':open(f'output{id}/final_trans.mkv','rb')
                }
                r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                    headers=headers,
                    files=files
                )
                # print(r.json())
                url_id = r.json()['id']
                output_url = f'https://drive.google.com/uc?id={url_id}'
                r1=requests.post(callback_url,data=json.dumps({
                    'status':200,
                    'output':output_url,
                    'queue_id':queue_id
                }))
                txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
                txt.write(f'Response for callback\n')
                txt.write(f'{r1.json()}')
                txt.close()
                mycursor.execute(f'UPDATE logs SET status="successful" WHERE id={int(id)}')
                mydb.commit()
            except:
                mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
                mydb.commit()
        else:
            mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
            mycursor.execute(f"SELECT * FROM logs WHERE id={id}")
            # callback_url = mycursor.fetchone()[5]
            # r1 = requests.post(callback_url,data=json.dumps({
            #     'status':400,
            #     'output':'Unable to generate your output video'
            # }))
            # txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
            # txt.write(f'Response for callback\n')
            # txt.write(f'{r1.json()}')
            # txt.close()
            try:
                shutil.rmtree(f'output{id}')
            except:
                pass
            mydb.commit()
        # if os.getcwd() == '/root/video_trans/translation_tool/trans/static/uploaded':
        if os.getcwd() == '/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded':
            txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
            txt.write('Process Ends\n')
            txt.close()
        # elif os.getcwd() == f'/root/video_trans/translation_tool/trans/static/uploaded/audio_analyze{id}':
        elif os.getcwd() == f'/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded/audio_analyze{id}':
            txt = open(f'../logs/log{id}.txt','a+',encoding='utf-8')
            txt.write('Process Ends\n')
            txt.close()

        waiting = waiting_requests(mycursor)
        running = running_requests(mycursor)
        running_num = len(running)
        # print('starting another process')
        # if os.getcwd() != '/root/video_trans/translation_tool/trans':
        if os.getcwd() != '/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans':
            # os.chdir('/root/video_trans/translation_tool/trans')
            os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans')
        if waiting != [] and running_num < 5:
            limit_available = 5-running_num
            # print(waiting[])
            if len(waiting) > limit_available:
                thread = []
                for i in range(limit_available):
                    # print(waiting[i])

                    process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                    # p=subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
                    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # t=Thread
                    p=subprocess.Popen(process,shell=True)

                    # print(process,p)
            else:
                for i in range(len(waiting)):
                    # print(waiting[i])

                    process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                    # p=subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
                    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    p=subprocess.Popen(process,shell=True)
                    # print(process,p)
                    
        sys.exit(0)
        # os.chdir('..')
        # shutil.move(f'logs/log{id}.txt',f'logs/log{id}.txt')
    # except SystemExit:
    #     # pass
    #     print('Something')
    #     exit_flag=1
    except PermissionError:
        # print('Thank you for using our Service bye for now!')
        mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
        mydb.commit()
        exit_flag =1
        try:shutil.rmtree(f'../output{id}')
        except:pass
        if waiting != [] and running_num < 5:
            limit_available = 5-running_num
            # print(waiting[])
            if len(waiting) > limit_available:
                for i in range(limit_available):
                    # print(waiting[i])

                    process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                    # p=subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
                    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    p=subprocess.Popen(process,shell=True)

                    # print(process,p)
            else:
                for i in range(len(waiting)):
                    # print(waiting[i])

                    process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                    # p=subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
                    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    p=subprocess.Popen(process,shell=True)
                    # print(process,p)
        sys.exit(0)
    except FileNotFoundError:
        # print('Sorry for Inconvenience')
        mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
        mydb.commit()
        try:shutil.rmtree(f'../output{id}')
        except:pass
        if waiting != [] and running_num < 5:
            limit_available = 5-running_num
            # print(waiting[])
            if len(waiting) > limit_available:
                for i in range(limit_available):
                    # print(waiting[i])

                    process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                    # p=subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
                    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    p=subprocess.Popen(process,shell=True)
                    # print(process,p)
            else:
                for i in range(len(waiting)):
                    # print(waiting[i])

                    process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                    # p=subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
                    #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    p=subprocess.Popen(process,shell=True)
                    # print(process,p)
        quit(0)
