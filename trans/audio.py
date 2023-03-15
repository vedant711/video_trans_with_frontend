import time
from pydub import AudioSegment
# from gtts import gTTS
from threading import Thread
# from talkey.engines import EspeakTTS
import os
# os.chdir('audio_analyze')
# EspeakTTS.say(phrase=con, )
from datetime import datetime
# from merge import merge
import wave
import re

global iter_factor,log_flag
iter_factor,log_flag = 0,0

def audio(entry_id,lang,silence_index,exit_flag):
    # txt = open(f'log.txt','a+',encoding='utf-16')
    # txt.write(f'{lang} tts start = ')
    # txt.write(str(datetime.now()) + '\n')
    # txt.close()
    global log_flag
    while True:
        try:
            if log_flag ==0:
                log_flag =1
                txt = open(f'../logs/log{entry_id}.txt','a+',encoding='utf-8')
                s= f'{lang} tts start = {str(datetime.now())}\n'
                txt.write(str(s))
                txt.close()
                log_flag = 0
                break
            else:
                time.sleep(1)
        except:
            log_flag = 0
            exit_flag=1
            # print('hello')
            return
    try:
        trans_file = open(f'{lang}_files/{lang}.txt','r', encoding='utf-16')
        read_file = trans_file.readlines()
        trans_file.close()
        cont = '. '.join(read_file).strip()
        # cont1 = ''.join(cont.splitlines())
        splitting_factor = '@#$%^&*()'
        cont_arr2 = cont.split(splitting_factor)
        cont_arr1 = []
        no_of_lines = []
        cont_arr = []
        cont_arr3 = []
        del cont
        del read_file
        del trans_file
        del splitting_factor
        # i=0
        # while True:
        #     no_of_lines = cont_arr2[i].count('\n')
        #     if no_of_lines = 
        # no_line_exit = 1
        # i=0
        # while True:
        #     for ele in cont_arr2:
        #         if ele.count('\n')>20:
        #             no_line_exit = 0
        #     if no_line_exit ==1:
        #         break
        #     if cont_arr2[i].count('\n') > 20:
        #         res = -1
        #         for k in range(20):
        #             res = cont_arr2[i].find('\n', res + 1)
        for ele in cont_arr2:
            sub_arr = re.compile("(?:^.*$\n?){1,20}",re.M).findall(ele)
            for subs in sub_arr:
                cont_arr3.append(subs)

        del cont_arr2     

        for ele in cont_arr3:
            # if '!_+:;<>,./' not in ele:
            if ele != '!_+:;<>,./\n. ' and ele != '!_+:;<>,./':
                # print(ele)
                # print(ele.count('\n'))
                no_of_lines.append(ele.count('\n'))
            temp_ele = ele
            ele = ''.join(temp_ele.splitlines())
            cont_arr.append(ele)
        i=0

        del cont_arr3
        
        # print(cont_arr)
        while i<len(cont_arr):
            con = cont_arr[i]
            if con != '!_+:;<>,./ ' and con!='!_+:;<>,./. ':
                if '!_+:;<>,./' in con:
                    c1 = con.split(' ',maxsplit=1)
                    # print(c1)
                    for ele in c1:
                        cont_arr1.append(ele)   
                else:
                    cont_arr1.append(con)
            else:
                cont_arr1.append(con)
            i+=1
        del cont_arr
        # print(cont_arr1)
        # print(len(no_of_lines),len(cont_arr1))
        lang1 = lang
        if lang == 'zh-CN':
            lang1='zh'
        global iter_factor
        try:
            os.remove(f'{lang}_files/audio_chunks.txt')
        except:
            pass
        while True:
            try:
                combined = AudioSegment.empty()
                # combined=[]
                i=0
                for con in cont_arr1:
                    # con = cont_arr1[i]
                    # print(con)
                    if '!_+:;<>,./' not in con:
                        # print('Text to speech')
                        # if iter_factor >= 3:
                        #     time.sleep(5)
                        #     iter_factor = 0
                        #     print('Iter Factor exceeded')
                        # time.sleep(1)
                        # print(con)
                        cmd = f'espeak -v {lang1} "{con}" -s 150 -w {lang}_files/{lang}_sep{i}.wav'
                        # print(cmd)
                        os.system(cmd)
                        audio_file = AudioSegment.from_wav(f'{lang}_files/{lang}_sep{i}.wav')
                        duration = audio_file.duration_seconds
                        orig_duration = no_of_lines[i] * 5
                        if duration < orig_duration:
                            sub = orig_duration-duration
                            # print(f'Increasing by {sub}')
                            chunk_silent = AudioSegment.silent(duration = sub*1000)
                            final_audio = audio_file + chunk_silent
                            final_audio.export(f'{lang}_files/{lang}_sep{i}.wav',format='wav')
                        # print(i)
                        i+=1
                            # speaker = gTTS(text=con,lang=lang,slow=False)
                            # speaker.save(f'./{lang}_sep{i}.mp3')
            
                k=0
                cont_ind=0
                # print('compiling audio')
                # if silence_index != []:
                iter =0
                count = 0
                for j in range(len(cont_arr1)):
                    if iter == 10:
                        combined.export(f'{lang}_files/{lang}_chunk{count}.wav',format='wav')
                        del combined
                        combined = AudioSegment.empty()
                        # print(f'combining {count} 10 files for {lang}')
                        audio_txt = open(f'{lang}_files/audio_chunks.txt', 'a+')
                        audio_txt.write(f'file {lang}_chunk{count}.wav\n')
                        audio_txt.close()
                        count+=1
                        iter=0

                    if '!_+:;<>,./' in cont_arr1[j]:
                        # global silence_index
                        try:
                            combined+=AudioSegment.from_wav(f'chunk{silence_index[k]}.wav')
                            # combined.append(AudioFileClip(f'chunk{silence_index[k]}.wav'))
                            # w=wave.open(f'chunk{silence_index[k]}.wav','rb')
                            # combined.append([w.getparams(), w.readframes(w.getnframes())])
                            # print(f'merging silence_index[{k}]')
                            # print(k)
                            # os.remove(f'chunk{silence_index[k]}.wav')
                            
                            iter +=1
                            k+=1
                        except:
                            # print(k,lang)
                            # print(len(silence_index))
                            pass
                    else:
                        combined+=AudioSegment.from_wav(f'{lang}_files/{lang}_sep{cont_ind}.wav')
                        # combined.append(AudioFileClip(f'{lang}_files/{lang}_sep{cont_ind}.wav'))
                        # w=wave.open(f'{lang}_files/{lang}_sep{cont_ind}.wav','rb')
                        # combined.append([w.getparams(), w.readframes(w.getnframes())])
                        # print(f'Merging cont_ind[{cont_ind}]')
                        os.remove(f'{lang}_files/{lang}_sep{cont_ind}.wav')
                        iter+=1
                        cont_ind+=1
                        # os.remove(f'{lang}_files/{lang}_sep{cont_ind}.wav')
                    # output = wave.open(f'{lang}_files/{lang}_audio.wav', "wb")
                    # output.setparams(combined[0][0])
                    # for i in range(len(combined)):
                    #     output.writeframes(combined[i][1])
                    # output.close()
                # else:
                #     print('HI')
                #     # print(cont_arr1)
                #     for j in range(len(cont_arr1)):
                #         w=wave.open(f'{lang}_files/{lang}_sep{cont_ind}.wav','rb')
                #         combined.append([w.getparams(), w.readframes(w.getnframes())])
                #         # print(f'Merging cont_ind[{cont_ind}]')
                #         # print(combined)
                #         cont_ind+=1
                # print(combined)
                #     # print('Exporting')
                #     # final_clip = concatenate_audioclips(combined)        
                # combined.export(f'{lang}_files/{lang}_audio.wav',format='wav')
                #     # final_clip.write_audiofile(f'{lang}_files/{lang}_audio.mp3')
                #     print('Merging Audio..')
                #     output = wave.open(f'{lang}_files/{lang}_audio.wav', "wb")
                #     output.setparams(combined[0][0])
                #     for i in range(len(combined)):
                #         output.writeframes(combined[i][1])
                #     output.close()
                # print('Exported')
                # os.system(f'ffmpeg -i {lang}_files/{lang}_audio.wav {lang}_files/{lang}_audio.mp3')
                # os.system(f'ffmpeg -i {lang}_files/{lang}_audio.wav -c:v copy {lang}_files/{lang}_audio.mp3')
                # os.remove(f'{lang}_files/{lang}_audio.wav')
                # for sil in silence_index:
                #     try:
                #         os.remove(f'chunk{sil}.wav')
                #     except: pass
                # print('combining')
                # combined.export(f'{lang}_files/{lang}_chunk{count}.wav',format='wav')
                # # final_comb = AudioSegment.empty()
                # cmd = f'ffmpeg -f concat -i {lang}_files/audio_chunks.txt -c copy {lang}_files/{lang}_audio.wav'
                # os.system(cmd)
                # for cindex in range(count):

                #     final_comb += AudioSegment.from_wav(f'{lang}_files/{lang}_chunk{cindex}.wav')
                #     os.remove(f'{lang}_files/{lang}_chunk{cindex}.wav')
                # final_comb.export(f'{lang}_files/{lang}_audio.wav',format='wav')
                combined.export(f'{lang}_files/{lang}_chunk{count}.wav',format='wav')
                audio_txt = open(f'{lang}_files/audio_chunks.txt', 'a+')
                audio_txt.write(f'file {lang}_chunk{count}.wav\n')
                audio_txt.close()
                break
            except PermissionError:
                # print(f'Hello from audio thread {lang}')
                exit_flag=1
                return 
            except FileNotFoundError:
                return

                # return
            except:
                print('sleeping')
                time.sleep(5)
    except PermissionError:
        return
    except FileNotFoundError:
        return
    while True:
        try:
            if log_flag ==0:
                log_flag =1
                txt = open(f'../logs/log{entry_id}.txt','a+',encoding='utf-8')
                s= f'{lang} tts complete = {str(datetime.now())}\n'
                txt.write(str(s))
                txt.close()
                log_flag = 0
                break
            else:
                time.sleep(1)
        except:
            log_flag = 0
            # print('hello')
            exit_flag=1
            return
    # except:
    #     exit_flag=1
    #     return
        
        # except:
        #     print('sleeping...')
        #     time.sleep(5)

def threads_audio(id,langs,silence_index,exit_flag):
    thread =[]
    # print('HI')
    for lang in langs:
        thread.append(Thread(target=audio, args=(id,lang,silence_index,exit_flag,)))
        thread[-1].start()
    for t in thread:
        t.join()
    # print(thread)
    # print(thread)
    # return exit_flag


# langs = ['hi','fr','zh-CN','pt','de','pl','ru','es','sv','el']


# id = 188
# exit_flag=0
# silence_index=[19,39,86,108,120,132,140,141,181,200,233,237,248,264,292,302,345,353,361,366,373,375,381,421,458,459,462,468,473,487,491,519,525,527,548]
# # silence_index=[]
# # orig_path = '../java.mp4'
# os.chdir('static/uploaded/audio_analyze188')
# print(os.getcwd())
# threads_audio(id,langs,silence_index,exit_flag)
# # merge(id,langs,orig_path)
# print('Hello')