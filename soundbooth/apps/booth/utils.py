import os
import pytz
from datetime import datetime
from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from django.conf import settings

CHANNELS = 2
SAMPLE_RATE = 44100
THRESHOLD = 500
CHUNK_SIZE = 2048
FORMAT = pyaudio.paInt16

TEMP_PATH = getattr(settings, 'BOOTH_RECORDING_STORAGE_PATH', '/tmp')
TIME_ZONE = getattr(settings, 'TIME_ZONE', 'American/New_York')

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*SAMPLE_RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*SAMPLE_RATE))])
    return r

def record(duration):
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    duration = int(duration) * 60
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE
    )

    num_silent = 0
    snd_started = False

    r = array('h')


    for i in range(0, int(SAMPLE_RATE / CHUNK_SIZE * duration)):
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        '''
        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break
        '''

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(duration, filename):
    "Records from the microphone and outputs the resulting data to 'path'"
    duration = int(duration)
    if '.wav' not in filename:
        filename = filename + '.wav'

    path = os.path.join(TEMP_PATH, filename)

    sample_width, data = record(duration)
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(data)
    wf.close()
    return path

if __name__ == '__main__':
    print("please speak a word into the microphone")
    record_to_file(10, 'demo.wav')
    print("done - result written to demo.wav")


def get_timezone_offset():
    tz = pytz.timezone(TIME_ZONE)
    dt = datetime.utcnow()
    offset_days = tz.utcoffset(dt).days
    offset = '+'
    if str(offset_days)[0] == '-':
        offset = '-' 
    offset_seconds = tz.utcoffset(dt).seconds
    offset_hours = offset_seconds / 3600.0
    if offset == '-':
        offset_hours = 24 - offset_hours
    return offset, int(offset_hours), int((offset_hours % 1) * 60)
