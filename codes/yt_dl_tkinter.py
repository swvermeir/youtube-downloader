import tkinter as tk
import tkinter.ttk
import subprocess
import yt_dl_formats
import yt_dl_downloader
import threading

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
    def thread_operation():
        titel, id_lijst, opties = yt_dl_formats.formats(url_value.get())
        info['titel'], info['id_lijst'], info['opties'] = titel, id_lijst, opties
        combo['values'] = opties
        combo.current(0)

    # Using separate thread so tkinter is still interactable
    thread = threading.Thread(target=thread_operation)
    thread.start()


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

# rij
r += 1

downloads = tk.IntVar()
completed = tk.IntVar()


def add_one(i: tk.IntVar):
    i.set(i.get() + 1)


def download():
    optie = format_value.get()
    if optie == combo_tekst:
        feedback2['text'] = 'Eerst url controleren.'
        return

    format_id = info['id_lijst'][info['opties'].index(optie)]
    format_id_2 = None

    def thread_operation():
        add_one(downloads)
        yt_dl_downloader.download([url_value.get()], format_id, format_id_2)
        add_one(completed)

        feedback1['text'] = f'({completed.get()}/{downloads.get()}) downloads voltooid!!!'
        feedback2['text'] = 'Controleer downloads folder.'

    thread = threading.Thread(target=thread_operation)
    thread.start()


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
