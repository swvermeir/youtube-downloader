import winreg
import os
import winshell
from __init__ import test

print("Aanmaken: Bureaublad snelkoppeling")
with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
    locatie = winreg.QueryValueEx(key, 'Desktop')[0]  # zie code bij Register-editor -> Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
name = 'youtube downloader'
if test:
    name += ' test'
location = os.path.join(locatie, f'{name}.lnk')
start = os.path.dirname(__file__)  # folderlocatie waar dit bestand instaat
target = os.path.join(start, 'yt_dl_tkinter.py')
icon = os.path.join(start, 'youtube downloader.ico')

shortcut = winshell.shortcut(location)
shortcut.path = target
shortcut.icon_location = icon, 0  # ico file => slecht 1 icon => integer maakt niet uit vb 0
shortcut.working_directory = start
shortcut.write()
print("Aangemaakt: Bureaublad snelkoppeling")
