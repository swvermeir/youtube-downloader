import os
import subprocess

codes_map = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'codes')
files = ['yt_dl_install.py', 'yt_dl_install_ffmpeg.py', 'yt_dl_desktop_shortcut.py']
for file in files:
    subprocess.run(['py', os.path.join(codes_map, file)])
