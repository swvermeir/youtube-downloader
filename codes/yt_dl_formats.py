from __future__ import unicode_literals
import yt_dlp
import SI_voorvoegsel
import logging
from typing import Any
from yt_dl_errorhandling import while_errorhandling

logging.basicConfig(level=logging.INFO)
NONE = frozenset({None, 'none', '', 'None'})
NONE_VALUE = '???'


def get_value(f, key, none_value: Any = NONE_VALUE, none_list=NONE):
    value = f.get(key, none_value)
    return value if value not in none_list else none_value


def get_estimate_duration(formats):
    estimate = 0
    amount = len(formats)
    for f in formats:
        key = 'duration'
        duration = get_value(f, key, none_value=0)
        fragments = get_value(f, 'fragments', none_value=[])
        for frag in fragments:
            duration += get_value(frag, key, none_value=0)
        estimate += duration
        if not duration:
            amount -= 1
    return estimate / amount if amount else 0


def formats(url):
    id_list, ext_list, frames_list, bits_list, form_list, fnote_list, duration_list, filesize_list, audio_video_list = [], [], [], [], [], [], [], [], []
    opties = []
    ydl = yt_dlp.YoutubeDL({})
    info = while_errorhandling(ydl.extract_info)(url, download=False)
    
    logging.info("Available video formats found, select your options.")
    logging.debug(info.keys())
    logging.debug(info)
    
    entries = info.get('entries')
    playlist = info.get('_type') == 'playlist'
    if playlist and entries:
        info = entries[0]
    
    titel = info.get('title', NONE_VALUE)
    formats = info.get('formats', {})
    estimate_duration = get_estimate_duration(formats)
    for f in formats:
        id = f.get('format_id', '')  # format code vb.: 249
        id_list.append(id)

        ext = f.get('ext', '')  # extensie vb.: mp4
        ext_list.append(ext)
        
        # framerate in frames per second (fps) vb.: 30
        key = 'fps'
        frames = get_value(f, key)
        frames = str(frames)
        frames += 'fps'
        frames_list.append(frames)
        
        # bitrate in kilobits per seconde (kbps) vb.: 129
        key = 'tbr'
        bits_number = get_value(f, key, none_value=0)
        bits = str(bits_number) if bits_number else NONE_VALUE
        bits += 'kbps'
        bits_list.append(bits)
        
        # format vb.: 1280×720
        key = 'format'
        form = get_value(f, key)
        form = form[len(id)+3:].split(' (')[0]
        form_list.append(form)
        
        # format notitie vb.: 720p
        key = 'format_note'
        fnote = get_value(f, key)
        fnote_list.append(fnote)
        
        key = 'duration'
        duration = get_value(f, key, none_value=0)
        fragments = get_value(f, 'fragments', none_value=[])
        for frag in fragments:
            duration += get_value(frag, key, none_value=0)
        if not duration:
            duration = estimate_duration
        duration_list.append(duration)
        
        key = 'filesize'
        size = get_value(f, key, none_value=None)
        estimated_size = duration * bits_number * 125  # 1kbps = 1000bps = 125Bps
        size = size if size is not None else estimated_size if estimated_size else None
        filesize = str(SI_voorvoegsel.SIPrefix(size, 'B').transform(2)) if size not in NONE else '???B'
        if estimated_size:
            filesize = '~' + filesize
        filesize_list.append(filesize)

        # audio en/of video
        vcodec = f.get('vcodec', '')
        acodec = f.get('acodec', '')
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
