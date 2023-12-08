import requests
import os
from pyunpack import Archive
import shutil
import glob
import time
import re
from local_variables import read_json, write_json
from SI_voorvoegsel import SIPrefix
from youtube_dl.utils import try_get

local_vars = read_json() or {}
ffmpeg = local_vars.get('ffmpeg')

ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
name = ffmpeg_url.split('/')[-1]

info = requests.head(ffmpeg_url).headers
versie = info['Location'].split('/')[-1]
if ffmpeg == versie:
    print(f"Requirement already satisfied: {versie}")
else:
    print("Collecting ffmpeg")
    print(f"  Downloading {versie}")
    with requests.get(ffmpeg_url, stream=True) as ffmpeg, open(name, 'wb') as ffmpeg_zip:  # stream=True maakt het mogelijk om iter_content te gebruiken
        t0 = time.perf_counter()
        total_size = 0
        t1 = t0
        f = 0.25
        between_speed = 0
        print("    0MB", end='')
        for i, chunk in enumerate(ffmpeg.iter_content(chunk_size=1048576)):
            if chunk:
                ffmpeg_zip.write(chunk)
                t2 = time.perf_counter()
                total_size += chunk
                current_speed = len(chunk) / (t2 - t1)
                average_speed = total_size / (t2 - t0)
                between_speed = current_speed * f + between_speed * (1 - f)
                print(f"\r    {SIPrefix(total_size, 'B').transform(2):>8} {round(SIPrefix(current_speed, 'B/s').transform(3)):>11}", end='')
                t1 = t2
        print()

    yt_dl_path = shutil.which('youtube-dl')
    scripts = os.path.dirname(yt_dl_path)
    path = os.path.join(os.path.dirname(__file__), 'zip_extract')
    patool_path = shutil.which('patool')
    Archive(name).extractall(path, auto_create_dir=True, patool_path=patool_path)

    exes = glob.glob(path + '/**/*.exe', recursive=True)
    for exe in exes:
        shutil.copy(exe, scripts)

    shutil.rmtree(path)
    os.remove(name)

    print(f"Successfully installed {versie.split('.')[0]}")

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
