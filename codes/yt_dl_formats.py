from __future__ import unicode_literals
import youtube_dl
import SI_voorvoegsel
from __init__ import test

NONE = {None, 'none', '', 'None'}
NONE_VALUE = '???'
def get_value(f, key):
    return f[key] if (key in f.keys() and f[key] not in NONE) else None

def formats(url):
    id_list, ext_list, frames_list, bits_list, form_list, fnote_list, size_list, filesize_list, audio_video_list = [], [], [], [], [], [], [], [], []
    opties = []
    ydl = youtube_dl.YoutubeDL({})
    info = ydl.extract_info(url, download=False)
    print(info.keys())
    print(info)
    info = info['entries'][0] if '_type' in info and info['_type'] == 'playlist' and 'entries' in info else info
    titel = info['title'] if 'title' in info.keys() else '???'
    formats = info['formats'] if 'formats' in info.keys() else {}
    for f in formats:
        id = f['format_id'] if 'format_id' in f.keys() else ''  # format code vb.: 249
        id_list.append(id)

        ext = f['ext'] if 'ext' in f.keys() else ''  # extensie vb.: mp4
        ext_list.append(ext)
        
        # framerate in frames per second (fps) vb.: 30
        key = 'fps'
        frames = get_value(f, key)
        frames = str(frames) if frames is not None else NONE_VALUE
        frames += 'fps'
        frames_list.append(frames)
        
        # bitrate in kilobits per seconde (kbps) vb.: 129
        key = 'tbr'
        bits = get_value(f, key)
        bits = str(bits) if bits is not None else NONE_VALUE
        bits += 'kbps'
        bits_list.append(bits)
        
        # format vb.: 1280×720
        key = 'format'
        form = get_value(f, key)
        form = form[len(id)+3:].split(' (')[0] if form is not None else NONE_VALUE
        form_list.append(form)
        
        # format notitie vb.: 720p
        key = 'format_note'
        fnote = get_value(f, key)
        fnote = fnote if fnote is not None else NONE_VALUE
        fnote_list.append(fnote)
        
        key = 'filesize'
        size = get_value(f, key)
        filesize = str(SI_voorvoegsel.SIPrefix(size, 'B').transform(2)) if size is not None else NONE_VALUE
        filesize_list.append(filesize)

        # audio en/of video
        vcodec = f['vcodec'] if 'vcodec' in f.keys() else ''
        acodec = f['acodec'] if 'acodec' in f.keys() else ''
        audio = "audio" if acodec != "none" else ""
        video = "video" if vcodec != "none" else ""
        mid = "+" if (audio and video) else ""
        audio_video = f'{audio}{mid}{video}'
        audio_video_list.append(audio_video)

        optie = [audio_video, ext, bits, filesize]
        if "video" in audio_video:
            optie.extend([form, frames])
        optie_tekst = [f'{opt: <{20}}' for opt in optie]
        optie_tekst = ''.join(optie_tekst)
        opties.append(optie_tekst)
    return titel, id_list[::-1], opties[::-1]


#if test:
#    a = formats("https://www.youtube.com/playlist?list=pls00qt59xosuaunc0ibsb0na2ieoe0dtj")
