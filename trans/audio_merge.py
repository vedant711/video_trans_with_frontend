import os
from threading import Thread

def merge_audio(lang):
    cmd = f'ffmpeg -loglevel panic -f concat -i {lang}_files/audio_chunks.txt -c copy {lang}_files/{lang}_audio.wav'
    os.system(cmd)
    dont_del = [f'{lang}_audio.wav',f'{lang}.txt']
    for ele in os.listdir(f'{lang}_files'):
        if ele not in dont_del:
            os.remove(f'{lang}_files/{ele}')

def merge_audio_threads(langs,silence_index):
    for sil in silence_index:
        try:
            os.remove(f'chunk{sil}.wav')
        except: pass
    
    thread =[]
    # print('HI')
    for lang in langs:
        thread.append(Thread(target=merge_audio, args=(lang,)))
        thread[-1].start()
    for t in thread:
        t.join()