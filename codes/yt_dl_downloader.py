# video downloader
import yt_dlp  # yt_dlp is build on youtube_dl
import os
import winreg
from yt_dl_errorhandling import while_errorhandling


def download(url, formatie, formatie_audio=None):
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

    # download
    error = while_errorhandling(yt_dlp.YoutubeDL(ydl_options).download)(url)
    print(isinstance(error, yt_dlp.utils.DownloadError))
    if isinstance(error, yt_dlp.utils.DownloadError):  # Invalid filename
        ydl_options['outtmpl'] = os.path.join(folder, 'untitled.%(ext)s')
        error = while_errorhandling(yt_dlp.YoutubeDL(ydl_options).download)(url)
    os.startfile(folder)
