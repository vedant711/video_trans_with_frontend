import os

def vid_to_wav(id,path):
    command2mp3 = f"ffmpeg -loglevel panic -i {path} vid.mp3 -c:v copy"
    command2wav = f"ffmpeg -loglevel panic -i vid.mp3 vid.wav -c:v copy"
    try:os.system(command2mp3)
    except: return
    try:os.system(command2wav)
    except:return