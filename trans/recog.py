import speech_recognition as sr
from pydub import AudioSegment
import time
import csv
import os

def recog_chunk(chunks,silence_index,exit_flag):
    try:
        i = 0
        for chunk in chunks:
            chunk_silent = AudioSegment.silent(duration = 100)
            audio_chunk = chunk_silent + chunk + chunk_silent
            # print("saving chunk{0}.wav".format(i))
            audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")
            filename = 'chunk'+str(i)+'.wav'
            # print("Processing chunk "+str(i))
            file = filename
            # text recognition
            r=sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio_listened = None
                while True:
                    try:
                        audio_listened = r.listen(source)
                        # print('audio heard')
                        # print(audio_listened)
                        break
                    except PermissionError:
                        # print('Thank You for Using Our Service')
                        exit_flag = 1
                        
                        return
                    except FileNotFoundError:
                        return
                    except:
                        # print('Trying again')
                        time.sleep(5)
                        continue
            while True:
                try:
                    rec = r.recognize_google(audio_listened)
                    # sents = segmenter.segment(rec)
                    # print('audio_recognized')
                    # print(rec)
                    # rec1 = '. '.join(sents)
                    os.remove(f"./chunk{i}.wav")
                    final_row = [rec]
                    i+=1
                    break

                except sr.UnknownValueError:
                    # print("Could not understand audio")
                    # global silence_index
                    silence_index.append(i)
                    final_row = [f'@#$%^&*(){len(silence_index)-1}']
                    i+=1
                    break
                except PermissionError:
                    # print('Thank You for Using Our Service')
                    exit_flag = 1

                    return
                except FileNotFoundError:
                    return
                except:
                    print('Trying again in 5 seconds')
                    time.sleep(5)
                    # print('Woke Up')

            try:
                # csv_file = open('op.csv','r', encoding='utf-16')
                csv_file = open('op.csv','a+', encoding='utf-16')
                writer = csv.writer(csv_file)

                writer.writerow(final_row)
                csv_file.close()
            except PermissionError:
                # print(threading.enumerate())
                # print('Thank You for Using Our Service')
                exit_flag = 1

                return
            except FileNotFoundError:
                return
    except PermissionError:
        # print('Thank You for Using Our Service')
        exit_flag = 1
        return
    except FileNotFoundError:
        return