import tkinter as tk
import tkinter.ttk
import subprocess
import yt_dl_formats
import yt_dl_downloader
from __init__ import test

# youtube_dl up to date houden
#subprocess.run(["py", "-m", "pip", "install", "--upgrade", "youtube_dl"])

info = {}

window = tk.Tk()
window.wm_iconbitmap('youtube downloader.ico')
window.title("Youtube Downloader")
window.geometry('800x360')

# rij = leeg
r = 0
window.grid_rowconfigure(r, minsize=20)

# rij
r += 1
lbl = tk.Label(window, text='URL:', font=('Arial Bold', 10), anchor='w')
lbl.grid(column=0, row=r, sticky="E")

url_value = tk.StringVar()
txt = tk.Entry(window, textvariable=url_value, width=95, state='normal')
txt.focus()
txt.grid(column=1, row=r, sticky="W", columnspan=6)


def formats():
    titel, id_lijst, opties = yt_dl_formats.formats(url_value.get())
    info['titel'], info['id_lijst'], info['opties'] = titel, id_lijst, opties
    combo['values'] = opties
    combo.current(0)


if test:
    def formats_2():
        opties = info['opties']
        optie_1 = format_value.get()
        aud_vid_1 = optie_1.split()[0]
        if aud_vid_1 == 'audio+video':
            combo['values'] = ['audio+video geselecteerd']
        if aud_vid_1 in ('audio', 'video'):
            aud_vid_2 = 'audio' if aud_vid_1 == 'video' else 'video'
            opties_2 = [optie for optie in opties if optie.split()[0] == aud_vid_2]
            combo_2['values'] = opties_2
            combo_2.current(0)


btn_opt = tk.Button(window, text='url controleren', bg='lightgreen', fg='black', command=formats)
btn_opt.grid(column=8, row=r)

# rij = leeg
r += 1
window.grid_rowconfigure(r, minsize=20)

# rij = titels
r += 1
titels = ["Audio/Video", "Extensie", "Bitrate", "Grootte", "Resolutie", "Framerate"]
tekst = ''
for titel in titels:
    tekst += f'{titel:<{15}}'
tk.Label(window, text=tekst, font=('Arial Bold', 10)).grid(column=1, row=r, sticky="W")

# rij
r += 1
lbl = tk.Label(window, text='Optie 1:', font=('Arial Bold', 10), anchor='w')
lbl.grid(column=0, row=r, sticky="E")

format_value = tk.StringVar()
combo_tekst = 'eerst url controleren'
combo = tk.ttk.Combobox(window, textvariable=format_value, value=[combo_tekst], state='readonly', width=95)
combo.current(0)
combo.grid(column=1, row=r, columnspan=6)

# rij = leeg
r += 1
window.grid_rowconfigure(r, minsize=20)

if test:
    # rij
    r += 1
    lbl = tk.Label(window, text='Optie 2:', font=('Arial Bold', 10), anchor='w')
    lbl.grid(column=0, row=r, sticky="E")

    format_value_2 = tk.StringVar()
    combo_2_tekst = 'eerst optie 1 selecteren'
    combo_2 = tk.ttk.Combobox(window, textvariable=format_value_2, value=[combo_2_tekst], state='readonly', width=95)
    combo_2.current(0)
    combo_2.grid(column=1, row=r, columnspan=6)

    btn_opt_2 = tk.Button(window, text='Extra optie', bg='lightgreen', fg='black', command=formats_2)
    btn_opt_2.grid(column=8, row=r)

    # rij = leeg
    r += 1
    window.grid_rowconfigure(r, minsize=20)

# rij
r += 1


def download():
    optie = format_value.get()
    if optie == combo_tekst:
        feedback2['text'] = 'Eerst url controleren.'
        return

    if test:
        aud_vid = optie.split()[0]

        optie_2 = format_value_2.get()
        aud_vid_2 = optie_2.split()[0]

        if aud_vid == 'audio' and aud_vid_2 == 'video':
            format_id_2 = info['id_lijst'][info['opties'].index(optie)]
            optie = optie_2
        elif aud_vid == 'video' and aud_vid_2 == 'audio':
            format_id_2 = info['id_lijst'][info['opties'].index(optie_2)]
        else:
            format_id_2 = None
    else:
        format_id_2 = None

    format_id = info['id_lijst'][info['opties'].index(optie)]

    yt_dl_downloader.download([url_value.get()], format_id, format_id_2)
    feedback1['text'] = 'Download voltooid!!!'
    feedback2['text'] = 'Controleer downloads folder.'


btn_dl = tk.Button(window, text='Download', bg='orange', fg='black', command=download)
btn_dl.grid(column=1, row=r, columnspan=3)

# rij = leeg
r += 1
window.grid_rowconfigure(r, minsize=20)

# rij
r += 1
feedback1 = tk.Label(window, text='', font=('Arial Bold', 18), fg='green')
feedback1.grid(column=0, row=r, columnspan=8)

# rij
r += 1
feedback2 = tk.Label(window, text='', font=('Arial Bold', 10))
feedback2.grid(column=0, row=r, columnspan=8)

window.mainloop()