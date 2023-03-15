import os
import shutil

# os.chdir('audio_analyze')
def merge(id,langs,orig_path):
    os.chdir('..')
    try:
        os.mkdir(f'output{id}')
    except FileExistsError:
        pass
    try:
        os.chdir(f'audio_analyze{id}')
    except PermissionError:
        return
    except FileNotFoundError:
        return
    
    # for lang in langs:
    #     os.system(f'ffmpeg -i {lang}_files/{lang}_audio.wav -y {lang}_files/{lang}_audio.mp3')

    if len(langs) != 0:
        cmd = f'ffmpeg -loglevel panic -i {orig_path} '
        for i in range(len(langs)):
            cmd += f'-i {langs[i]}_files/{langs[i]}_audio.wav '
        cmd+='-map 0 '
        for i in range(len(langs)):
            cmd+=f'-map {i+1} '

        for i in range(len(langs)):
            if langs[i]=='hi': cmd+=f'-metadata:s:a:{i+1} language=hin '
            elif langs[i]=='gu': cmd+=f'-metadata:s:a:{i+1} language=guj '
            elif langs[i]=='fr': cmd+=f'-metadata:s:a:{i+1} language=fra '
            elif langs[i]=='ko': cmd+=f'-metadata:s:a:{i+1} language=kor '
            elif langs[i]=='bn': cmd+=f'-metadata:s:a:{i+1} language=ben '
            elif langs[i]=='zh-CN': cmd+=f'-metadata:s:a:{i+1} language=zho '
            elif langs[i]=='pt': cmd+=f'-metadata:s:a:{i+1} language=por '
            elif langs[i]=='de': cmd+=f'-metadata:s:a:{i+1} language=deu '
            elif langs[i]=='pl': cmd+=f'-metadata:s:a:{i+1} language=pol '
            elif langs[i]=='ar': cmd+=f'-metadata:s:a:{i+1} language=ara '
            elif langs[i]=='ru': cmd+=f'-metadata:s:a:{i+1} language=rus '
            elif langs[i]=='es': cmd+=f'-metadata:s:a:{i+1} language=spa '
            elif langs[i]=='sv': cmd+=f'-metadata:s:a:{i+1} language=swe '
            elif langs[i]=='la': cmd+=f'-metadata:s:a:{i+1} language=lat '
            elif langs[i]=='el': cmd+=f'-metadata:s:a:{i+1} language=ell '
            # elif langs[i]=='ja': cmd+=f'-metadata:s:a:{i+1} language=jpn '    
        cmd += f'-c:v copy -c:a ac3 -preset veryfast -y ../output{id}/final_trans.mkv'
        # print(cmd)
        try:
            os.system(cmd)
            os.chdir('..')

            shutil.rmtree(f'audio_analyze{id}')
            os.remove(f'{id}.mp4')
        except:
            pass
        
# os.chdir('audio_analyze6')
# langs = ['hi','fr','zh-CN','pt','de','pl','ru','es','sv','el']
# # langs = ['hi','de','el','es','fr']
# orig_path = '../java.mp4'
# merge(6,langs,orig_path)

