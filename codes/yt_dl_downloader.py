# video downloader
import youtube_dl
import os
import requests
import winreg
from __init__ import test


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
    youtube_dl.YoutubeDL(ydl_options).download(url)
    os.startfile(folder)

#download(["https://www.youtube.com/watch?v=XZXZUH4iGLo&ab_channel=RKGAMING"], 160, 140)


# testcodes
test, testtest = False, False

if test:
    readfile = open('Opgeslagen settings.txt', 'r')
    settingboek = {}
    for regel in readfile.readlines():
        naam, locat, format, audio_ext, video_ext = regel.split(',')
        settingboek[naam] = {'location': locat, 'formatie': format, 'aud_ext': audio_ext, 'vid_ext': video_ext}

    print(f'\nPresettings:')
    for setting in settingboek:
        print(f'    {setting}')
    presetting = input('Druk op "Enter" om over te slaan\n'
                       'Opgeslagen setting = ').lower()


    # outtmpl bepalen
    locatieboek = {'muziek': '%Muziek%',
                   'dope': 'D:/gebruiker hdd/Music/Dope/Python',
                   'videos': '%Video\'s%',
                   'downloads': '%Downloads%'}

    if not presetting:
        print('\nShortkeys:')
        for locatie in locatieboek:
            print(f'    {locatie} = {locatieboek[locatie]}')
        location = input('downloadlocatie (met "/"): ')
    else:
        location = settingboek[presetting]['location']
    if location.lower() in locatieboek.keys():
        location = locatieboek[location.lower()]


    # format bepalen
    if not presetting:
        print('Mogelijkheden:\n'
              '   "video" = enkel video\n'
              '   "video+audio" = video en audio te samen\n'
              '   "video,audio" = video en audio apart\n'
              '   "" = "all" = video,audio,video+audio\n')
        formatie = input('bestandentypen: ')
    else:
        formatie = settingboek[presetting]['formatie']

    if formatie == '':
        formatie = 'all'
    keepvideo = bool('all' in formatie)
    formatie = formatie.replace('all', 'video+audio').replace('audio', f'bestaudio').replace('video', f'bestvideo')


    # postprocessing
    aud_ext, vid_ext = '', ''
    if 'audio' in formatie:
        if not presetting:
            print('\next vb.: m4a, wav, mp3,...')
            aud_ext = input("Audio converteren naar ext = ")
        else:
            aud_ext = settingboek[presetting]['aud_ext']

    if 'video' in formatie:
        if not presetting:
            print('\next vb.: mp4, avi,...')
            vid_ext = input("Video converteren naar ext = ")
        else:
            aud_ext = settingboek[presetting]['aud_ext']


    # setting opslaan of niet
    save_settings = input('Deze settings opslaan? (j/n): ')[0].lower()
    if save_settings == 'j':
        appendfile = open('Opgeslane settings.txt', 'a')
        setting_name = input('Settings opslaan onder deze naam: ').lower()
        print(f'{setting_name},{location},{formatie},{aud_ext},{vid_ext}')


    # url
    urls = input("\nIndien meerdere urls, scheid met spaties."
                 "\nUrls (playlist url kan ook) = ")
    urls = urls.split()


    # playlist info
    noplaylist = not bool('list=' in urls)
    pls, ple = None, None
    start, end = None, None
    if not noplaylist:
        print('\nPlaylistlink gedetecteerd.\n'
              'Niks invullen om gans de playlist te downloaden.')
        playlist_stand = input('videonummers in playlist: start, einde: ')
        if playlist_stand:
            start, end = playlist_stand.split()
            pls, ple = 'playliststart', 'playlistend'


    # ydl opties
    ydl_options = {'format': formatie,
                   'noplaylist': noplaylist,
                   pls: start,
                   ple: end,
                   'keepvideo': keepvideo,
                   'outtmpl': f"{location}/%(title)s/%(title)s.%(ext)s",
                   'postprocessor': [{'key': 'FFmpegExtractAudio',
                                      'preferredcodec': aud_ext},
                                     {'key': 'FFmpegVideoConvertor',
                                      'preferredcodec': vid_ext}]}

    # download
    youtube_dl.YoutubeDL(ydl_options).download(urls)


if testtest:
    command = 'py - m youtube_dl'
    help = ('!help', '!help ', 'help', '!h', '! help', '!hulp', '! hulp')
    print('Typ "!help" voor meer uitleg.')
    # outtmpl bepalen
    locatieboek = {}
    scheider = ','
    textfile = open('Opgeslagen locaties.txt', 'r')
    for regel in textfile.readlines():
        naam, path = regel.split(scheider)
        locatieboek[naam] = path
    print('\nShortkeys:')
    if locatieboek:
        for locatie in locatieboek:
            print(f'    {locatie} = {locatieboek[locatie]}')
    else:
        print(f'    Nog geen opgeslan locaties')
    trigger = ', save '
    print(f'Voeg "{trigger}naam" achteraan toe om deze locatie op te slaan onder "naam"')
    location = input('downloadlocatie: ')
    while location.lower() in help:
        print('De downloadlocatie is de plaats in je bestanden waar je de video wilt downloaden.\n'
              'Voobeeld:\n'
              '   C:\\Gebruikers\\...\\gedownloade videos\n'
              'Je kan de locatie van een bestand of map vinden bij de eigenschappen\n'
              '(Selecteer het bestand, druk dan op rechtermuisknop en dan vind je onderaan "Eigenschappen")\n'
              '\n'
              f'Je kan ook locaties die je invult meteen opslaan door "{trigger}naam" direct na de locatie te typen.\n'
              f'Hierbij is naam de naam waarmee je deze locatie wilt opslaan.\n'
              f'Eens je dit gedaan hebt kan je de locatie terug gebruiken door enkel "naam" te typen.')
        location = input('downloadlocatie: ')
    if trigger in location:
        writefile = open('Opgeslane locaties.txt', 'a')
        location, name = location.split(trigger)
        print(name + scheider + location, file=writefile)

    if location.lower() in locatieboek.keys():
        location = locatieboek[location.lower()]

    # url
    urls = input("\nIndien meerdere urls, scheid met spaties."
                 "\nUrls (playlist url kan ook): ")
    sites = ('!sites', '!site', '!website', '!websites')
    while urls.lower() in (help or sites):
        if urls.lower() in help:
            print('Hier kan je enkele dingen doen:\n'
                  '   1. Vul de url in van een youtube video\n'
                  '         vb.: https://www.youtube.com/watch?v=JybquKZ4XXc\n'
                  '   2. Vul de url in van een youtube playlist\n'
                  '         vb.: https://www.youtube.com/playlist?list=PLqhuEBzGxuuFOgO4w3Cpwc1g2Kqb9qL12\n'
                  '   3. Vul de urls in van meerdere youtube video\'s en/of playlists\n'
                  '         vb.: https://www.youtube.com/watch?v=JybquKZ4XXc https://www.youtube.com/playlist?list=PLqhuEBzGxuuFOgO4w3Cpwc1g2Kqb9qL12\n'
                  '   4. Probeer de url van een niet-youtube video'
                  '         typ "!sites" om de supported sites te zien (druk Ctrl+F om te zoeken')
        if urls.lower() in sites:
            link = "https://ytdl-org.github.io/youtube-dl/supportedsites.html"
            res = requests.get(link)
            html_page = res.content
            html_str = str(html_page, encoding='utf-8')
            titel = html_str.split('<p>')[1].split('</p>')[0]
            print(titel)
            li_lijst = html_str.split('<ul>')[1].split('</ul>')[0]
            lijst = li_lijst.split('<li>')[1:]
            for regel in lijst:
                tekst = regel.split('</li>')[0].replace('<b>', '').replace('</b>', '')
                print('   ' + tekst)
        urls = input('urls: ')

    # login
    login = input('Login verplicht? (j/n): ')
    while login in help:
        print('Typ "j" indien de gegeven url niet toegankelijk is zonder login gegevens.\n'
              'Anders kan je "n" typen of gewoon enter drukken om over te slaan.')
        login = input('Login verplicht? (j/n): ')
    if login.lower()[0] in 'jy':
        username = input('Gebruikersnaam: ')
        password = input('Wachtwoord: ')
        command += f' -u "{username}" -p "{password}"'

    # cmd command
    print('\n')
    location += '\\%(title)s\\%(title)s.%(ext)s'
    command += f' -o "{location}" {urls} -k'
    os.system(f'cmd /k {command}')
