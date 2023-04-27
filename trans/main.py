import os
from pydub.utils import make_chunks
from pydub import AudioSegment
from vid_wav import vid_to_wav
from translate import threads
from audio import threads_audio
from merge import merge
import sys
import mysql.connector
import time
import shutil
import subprocess
from audio_merge import merge_audio_threads
import requests
import json
from dotenv.main import load_dotenv
import random


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

def new_process(mycursor):
    sleep_time = random.randrange(1000,5000)
    final_sleep = round(sleep_time/1000,2)
    time.sleep(final_sleep)
    waiting = waiting_requests(mycursor)
    running = running_requests(mycursor)
    running_num = len(running)
    if os.getcwd() != '/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans':
        os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans')
    if waiting != [] and running_num < 5:
        limit_available = 5-running_num
        if len(waiting) > limit_available:
            thread = []
            for i in range(limit_available):
                process = f"python3 main.py {waiting[i][3]} {waiting[i][0]} &"
                p=subprocess.Popen(process,shell=True)

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

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    orig_path = sys.argv[1]
    id = sys.argv[2]


    mycursor.execute(f"SELECT * FROM logs WHERE id={id}")

    curr_status = mycursor.fetchone()[1]

    mycursor.execute(f'UPDATE logs SET status="running" WHERE id = {id}')
    mydb.commit()
    try: os.mkdir('logs')
    except(FileExistsError): pass
    txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
    txt.write('Process Begins\n')
    txt.close()

    try: os.mkdir(f'audio_analyze{id}')
    except(FileExistsError): pass

    os.chdir(f'audio_analyze{id}')
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
    except PermissionError:sys.exit()
    except FileNotFoundError:sys.exit()

    # langs = ['hi','gu','fr','ko','bn','zh-CN','pt','de','pl','ar','ru','es','sv','la','el']
    langs = ['hi','fr','zh-CN','pt','de','pl','ru','es','sv','el']
    translated_files = {}

    exit_flag=0
    csv_file = open('op.csv','a+', encoding='utf-16')
    csv_file.close()
    silence_index=[]
    try:
        threads(id,chunks,langs,silence_index,exit_flag)
        threads_audio(id,langs,silence_index,exit_flag)
        merge_audio_threads(langs,silence_index)
        merge(id,langs,orig_path)
        if os.path.exists(f'/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded/output{id}/final_trans.mkv'):
            mycursor.execute(f'UPDATE logs SET status="uploading video" WHERE id={int(id)}')
            mydb.commit()
            mycursor.execute(f"SELECT * FROM logs WHERE id={id}")
            mycursor_obj_output = mycursor.fetchone()
            callback_url,queue_id,email = mycursor_obj_output[5],mycursor_obj_output[6],mycursor_obj_output[8]
            try:
                api_key=getToken()
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
                url_id = r.json()['id']
                output_url = f'https://drive.google.com/uc?id={url_id}'
                print(callback_url,email)
                if callback_url != '' and callback_url!=None:
                    r1=requests.post(callback_url,data=json.dumps({
                        'status':200,
                        'output':output_url,
                        'queue_id':queue_id
                    }))
                    txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
                    txt.write(f'Response for callback\n')
                    txt.write(f'{r1.json()}')
                    txt.close()
                else:
                    print(f'sending email to {email}')
                    password = os.environ['EMAIL_PASSWORD']
                    import smtplib, ssl

                    port = 587  # For starttls
                    smtp_server = "smtp.gmail.com"
                    sender_email = "vedant.dict19@sot.pdpu.ac.in"

                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.starttls(context=context)
                        message = f"\nYou can find your output at {output_url} for the queue ID : {queue_id}"

                        server.login(sender_email, password)
                        server.sendmail(sender_email, email,message)
                    txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
                    txt.write(f'Response for callback\n')
                    txt.write(f'Queue ID: {queue_id}\nOutput URL: {output_url}')
                    txt.close()
                
                mycursor.execute(f'UPDATE logs SET status="successful" WHERE id={int(id)}')
                mydb.commit()
            except:
                mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
                mydb.commit()
        else:
            mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
            mycursor.execute(f"SELECT * FROM logs WHERE id={id}")
            try:shutil.rmtree(f'output{id}')
            except:pass
            mydb.commit()
        if os.getcwd() == '/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded':
            txt = open(f'logs/log{id}.txt','a+',encoding='utf-8')
            txt.write('Process Ends\n')
            txt.close()
        elif os.getcwd() == f'/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded/audio_analyze{id}':
            txt = open(f'../logs/log{id}.txt','a+',encoding='utf-8')
            txt.write('Process Ends\n')
            txt.close()
        new_process(mycursor) 
        sys.exit(0)
    except PermissionError:
        mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
        mydb.commit()
        exit_flag =1
        try:shutil.rmtree(f'../output{id}')
        except:pass
        new_process(mycursor)
        sys.exit(0)
    except FileNotFoundError:
        mycursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id={int(id)}')
        mydb.commit()
        try:shutil.rmtree(f'../output{id}')
        except:pass
        new_process(mycursor)
        quit(0)
