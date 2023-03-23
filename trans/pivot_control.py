import mysql.connector
import subprocess
import sys
# from datetime import datetime
# from threading import Thread
import os
import urllib.request


def running_requests(cursor):
    cursor.execute("SELECT * FROM logs WHERE status='running'")
    return cursor.fetchall()

# def proc(path):
#     p = subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # stdout, stderr = p.communicate()
    
    # p=subprocess.Popen(process,shell=True)

limit = 5
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="translator1"
)
cursor = mydb.cursor()
cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

running = running_requests(cursor)
# path = input('Enter the path for the video: ')
# print(sys.argv)
# path = sys.argv[1]
id = sys.argv[1]
# url = sys.argv[3]

cursor.execute(f'SELECT * FROM logs WHERE id={id}')
url = cursor.fetchone()[4]


os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/static/uploaded')
# print(os.getcwd())
# urllib.request.urlretrieve(url, f'{id}.mp4')
# gdown.download(url,f'{id}.mp4',quiet=True)
ext = 'mp4'
# print(ext)
# log1.path = f'../{id}.{ext}'
# log1.save()
try:
    urllib.request.urlretrieve(url, f'{id}.mp4')
    path = f'../{id}.mp4'
    cursor.execute(f'UPDATE logs SET path="{path}" WHERE id = {id}')
    mydb.commit()
    # os.chdir('/root/video_trans/translation_tool/trans/')
    os.chdir('/Volumes/My Passport/Webmyne Internship/video_trans_tool/trans/')

    if len(running) < 5:
        if path != '':
            # sql = "INSERT INTO logs (status,start_datetime,path) VALUES (%s, %s, %s)"
            # d= str(datetime.now())
            # val = ("running", d, path)
            # cursor.execute(sql, val)
            # mydb.commit()

            # cursor.execute(f"SELECT id FROM logs WHERE start_datetime='{d}'")
            # id = cursor.fetchone()[0]

            cursor.execute(f'UPDATE logs SET status="running" WHERE id = {id}')
            mydb.commit()

            process = f"python3 main.py {path} {id} &"

            # subprocess.call(['gnome-terminal', '-x', process])
            # process1 = process.split()
            # subprocess.PIPE()
            # p = subprocess.Popen(process,shell=True, stdin=subprocess.PIPE,
            #                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # t = Thread(target=proc, args=(path,))
            # t.start()
            # print(process)
            p=subprocess.Popen(process,shell=True)
            # stdout, stderr = p.communicate()
            # We have started the program, and can suspend this interpreter
            quit(0)
        # print('Hi')
    else:
        if path!='':
            # sql = "INSERT INTO logs (status,start_datetime,path) VALUES (%s, %s, %s)"
            # d= str(datetime.now())
            # val = ("waiting", d, path)
            # cursor.execute(sql, val)
            # mydb.commit()
            cursor.execute(f'UPDATE logs SET status="waiting" WHERE id = {id}')
            mydb.commit()
except:
    cursor.execute(f'UPDATE logs SET status="unsuccessful" WHERE id = {id}')
    mydb.commit()


