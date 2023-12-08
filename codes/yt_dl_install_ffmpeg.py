import pyunpack
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
if ffmpeg == versie and False:
    print(f'Requirement already satisfied: {versie}')
else:
    print('Collecting ffmpeg')
    print(f'  Downloading {versie}')
    with requests.get(ffmpeg_url, stream=True) as ffmpeg, open(name, 'wb') as ffmpeg_zip:  # stream=True maakt het mogelijk om iter_content te gebruiken
        t_0 = time.perf_counter()
        print('    0MB', end='')
        for i, chunk in enumerate(ffmpeg.iter_content(chunk_size=1048576)):
            if chunk:
                ffmpeg_zip.write(chunk)
                t = time.perf_counter() - t_0
                print(f'\r    {i+1}MB {round((i+1)/t, 3):<05}MB/s', end='')
        print()

    yt_dl_path = shutil.which('youtube-dl')
    scripts = os.path.dirname(yt_dl_path)
    path = os.path.join(os.path.dirname(__file__), 'zip_extract')
    patool_path = shutil.which('patool')
    Archive(name).extractall(path, auto_create_dir=True, patool_path=patool_path)

    exes = glob.glob(path + '/**/*.exe', recursive=True)
    for exe in exes:
        shutil.copy(exe, scripts)

    print(path)
    shutil.rmtree(path)
    os.remove(name)

    print(f'Successfully installed {versie.split(".")[0]}')

    # write ffmpeg variable in __init__ file
    init_file = "__init__.py"
    if not os.path.exists(init_file):
        init_file = os.path.join("codes", init_file)
    
    with open(init_file, 'r') as f:
        text = f.read()
        
    string = 'ffmpeg = "{}"\n'
    value = re.findall(string.format("(.*)"), text)[0]
    old_line = string.format(value)
    new_line = string.format(versie)
    text = text.replace(old_line, new_line)
    
    with open(init_file, 'w') as f:
        f.write(text)
