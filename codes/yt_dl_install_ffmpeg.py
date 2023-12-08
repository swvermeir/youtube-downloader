import requests
import os
from pyunpack import Archive
import shutil
import glob
import time
import re

from youtube_dl.utils import try_get
from __init__ import ffmpeg

ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
name = ffmpeg_url.split('/')[-1]

info = requests.head(ffmpeg_url).headers
versie = info['Location'].split('/')[-1]
if ffmpeg == versie:
    print(f'Requirement already satisfied: {versie}')
else:
    print('Collecting ffmpeg')
    ffmpeg = requests.get(ffmpeg_url, stream=True)  # stream=True maakt het mogelijk om iter_content te gebruiken

    print(f'  Downloading {versie}')
    ffmpeg_zip = open(name, 'wb')  # wb = write bites?
    t_0 = time.perf_counter()
    print('    0MB', end='')
    for i, chunk in enumerate(ffmpeg.iter_content(chunk_size=1048576)):
        if chunk:
            ffmpeg_zip.write(chunk)
            t = time.perf_counter()
            print(f'\r    {i+1}MB {round((i+1)/t, 3):<05}MB/s', end='')
    print()
    ffmpeg_zip.close()
    ffmpeg.close()

    print('Installing collected packages: ffmpeg')
    yt_dl_path = shutil.which('youtube-dl')
    scripts = os.path.dirname(yt_dl_path)
    path = os.path.join(os.path.dirname(__file__), 'zip_extract')
    Archive(name).extractall(path, auto_create_dir=True)

    exes = glob.glob(path + '/**/*.exe', recursive=True)
    for exe in exes:
        shutil.copy(exe, scripts)

    shutil.rmtree(path)
    os.remove(name)

    print(f'Successfully installed {versie.split(".")[0]}')

    # omslachtig ???
    try: 
        init = open("__init__.py", 'r+')
    except:
        init = open("codes/__init__.py", 'r+')
    text = init.read()
    string = 'ffmpeg = '
    value = re.findall('ffmpeg = "(.*)"\n', text)[0]
    text = text.replace(value, versie)
    init.seek(0, 0)
    init.write(text)
