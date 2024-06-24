# video downloader
import yt_dlp  # yt_dlp is build on youtube_dl
import os
import winreg
from yt_dl_errorhandling import while_errorhandling
import subprocess


def download(url, formatie, formatie_audio=None, cookiesfrombrowser=None):
    # downloads folder bepalen
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        downloads = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]  # zie code bij Register-editor -> Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders

    # ydl opties
    if formatie_audio:
        formatie = f'{formatie}+{formatie_audio}'

    folder = os.path.join(downloads, 'filmpjes')
    ydl_options = {'format': formatie,
                   'debug': False,
                   'outtmpl': os.path.join(folder, '%(title)s.%(ext)s')}
    if cookiesfrombrowser:
        ydl_options['cookiesfrombrowser'] = (cookiesfrombrowser, None, None, None)
        
        # close all browser instances
        exe_dict = {'edge': "msedge"}
        browser_exe = exe_dict.get(cookiesfrombrowser, cookiesfrombrowser)
        subprocess.call(f"taskkill /f  /im  {browser_exe}.exe")

    # download
    error = while_errorhandling(yt_dlp.YoutubeDL(ydl_options).download)(url)
    if isinstance(error, yt_dlp.utils.DownloadError):  # Invalid filename
        ydl_options['outtmpl'] = os.path.join(folder, 'untitled.%(ext)s')
        error = while_errorhandling(yt_dlp.YoutubeDL(ydl_options).download)(url)
    os.startfile(folder)
