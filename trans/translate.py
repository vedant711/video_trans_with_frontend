from deep_translator import GoogleTranslator
from datetime import datetime
import csv
import time
import os
from threading import Thread
import random

from recog import recog_chunk


global iter_factor,log_flag, check_list
iter_factor = 0
log_flag = 0
check_list = []

def isfloat(s):
    try: 
        float(s)
        return True
    except:
        return False
    
def translate(id,langs,lang,chunks):
    global log_flag
    while True:
        try:
            if log_flag ==0:
                log_flag =1
                txt = open(f'../logs/log{id}.txt','a+',encoding='utf-8')
                s= f'{lang} translation start = {str(datetime.now())}\n'
                txt.write(str(s))
                # print(s)
                txt.close()
                log_flag = 0
                break
            else:
                time.sleep(1)
        except:
            log_flag = 0
            # print('hello')
            return
    
    translator = GoogleTranslator(source='auto',target=lang)
    
    global iter_factor
    # global chunks
    try:
        flag=0
        while True:
            try:
                os.mkdir(f'{lang}_files')
                flag += 1
            except(FileExistsError):
                pass
            # except:
            #     return
            try:
                csv_file = open('op.csv','r',encoding='utf-16')
            except FileNotFoundError:
                return
            except PermissionError:
                return
            reader = list(csv.reader(csv_file))
            # if len(reader) <=100 and len(chunks)>=100:
            #     continue
            csv_file.close()
            splitting_factor = '@#$%^&*()'
            ind_lang = langs.index(lang)
            # iter_factor = 0
            if flag != 1:
                for lines in check_list: lines[ind_lang] = 0
                flag = 1
            for row in reader:
                # rep_flag = 0
                if row != []:
                    count_row = reader.count(row)
                    try:
                        if count_row > 1:
                            ind_arr = [i for i, n in enumerate(reader) if n == row]
                            # ind = ind_arr[count_row-1]
                            for ind in ind_arr:
                                if check_list[ind][ind_lang] ==0:
                                    break
                            if check_list[ind][ind_lang] == 0:
                                if row[0] != '' and '@#$%^&*()' not in row[0]:
                                    trans_file = open(f'{lang}_files/{lang}.txt','r', encoding='utf-16')
                                    read_file = list(trans_file.readlines())
                                    trans_file.close()
                                    trans_file = open(f'{lang}_files/{lang}.txt','a+', encoding='utf-16')
                                    # print(len(read_file))
                                    if len(read_file) == ind:
                                    # print(f'The curr len is {len(read_file)}')
                                        if row[0].isnumeric() or isfloat(row[0]):
                                            trans_file.write(row[0]+'\n')
                                            check_list[ind][ind_lang] = 1
                                            continue
                                        else:
                                            trans = translator.translate(row[0])
                                            trans_file.write(trans+'\n')
                                            check_list[ind][ind_lang] = 1
                                            iter_factor +=1
                                            continue
                                    else:
                                        pass
                            # rep_flag+=1
                    except FileNotFoundError:
                        return
                    except PermissionError:
                        return
                    else:
                        ind = reader.index(row)
                    if check_list[ind][ind_lang] == 0:
                        try:
                            trans_file = open(f'{lang}_files/{lang}.txt','a+', encoding='utf-16')
                            if row[0] != '' and '@#$%^&*()' not in row[0]:
                                if iter_factor >= 50:
                                    sleep_time = random.randrange(1000,5000)
                                    final_sleep = round(sleep_time/1000,2)
                                    time.sleep(final_sleep)
                                    iter_factor =0
                                    # print('Iter Factor exceeded')
                                    # break
                                if row[0].isnumeric() or isfloat(row[0]):
                                    trans_file.write(row[0]+'\n')
                                    check_list[ind][ind_lang] = 1
                                    trans_file.close()
                                else:
                                    trans = translator.translate(row[0])
                                    trans_file.write(trans+'\n')
                                    check_list[ind][ind_lang] = 1
                                    iter_factor +=1
                                    trans_file.close()
                            else:
                                if ind != 0:
                                    trans_file.write(splitting_factor+'!_+:;<>,./'+'\n')      
                                else:
                                    trans_file.write('!_+:;<>,./'+splitting_factor+'\n')
                                check_list[ind][ind_lang] = 1
                                trans_file.close()
                            # check_list[ind][ind_lang] = 1
                        except PermissionError:
                            return
                        except FileNotFoundError:
                            return
                        except:
                            # print(f'Trying again for {lang}')
                            time.sleep(5)
                            break
                time.sleep(1)
            try:
                trans_file = open(f'{lang}_files/{lang}.txt','r', encoding='utf-16')
                read_file = list(trans_file.readlines())
                trans_file.close()
                if len(read_file) >= len(chunks):
                    # print('HI')
                    break
            except FileNotFoundError:
                continue
            except PermissionError:
                # print(f'Hello from trans thread {lang}2')
                #  
                return
        while True:
            try:
                if log_flag ==0:
                    log_flag =1
                    txt = open(f'../logs/log{id}.txt','a+',encoding='utf-8')
                    s= f'{lang} translation complete = {str(datetime.now())}\n'
                    txt.write(str(s))
                    txt.close()

                    log_flag = 0
                    break
                else:
                    time.sleep(1)
            except:
                log_flag = 0
                # print('hello')
                return
    except PermissionError:
        return
    except FileNotFoundError:
        return
    # time.sleep(1)


def threads(id,chunks, langs,silence_index,exit_flag):
    recog_thread = Thread(target=recog_chunk, args=(chunks,silence_index,exit_flag,))
# recog_thread.daemon=True
    recog_thread.start()
    thread = [recog_thread]
    # thread=[]
    global check_list
    check_list = [[0 for i in range(len(langs))] for j in range(len(chunks))]
    for lang in langs:
        thread.append(Thread(target=translate, args=(id,langs,lang,chunks,)))
        thread[-1].start()
    for t in thread:
        t.join()
    # return exit_flag

# silence_index = []
# langs = ['hi','fr','zh-CN','pt','de','pl','ru','es','sv','el']

# chunks = ['x' for _ in range(339)]
# os.chdir('audio_analyze60')
# threads(60,chunks,langs,silence_index,0)
# print('Hello')