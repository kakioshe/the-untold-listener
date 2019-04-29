import json
import wave
import pyaudio
import boto3
import os

def record(filename):
    form_1 = pyaudio.paInt16
    chans = 1
    samp_rate = 44100
    chunk = 4096
    record_secs = 5
    dev_index = 2
    wav_output_filename = filename
    audio = pyaudio.PyAudio()
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
    print("recording")
    frames = []
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)
    print("finished recording")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    
def uploadFile(bucket, emotion, file):
    s3 = boto3.resource('s3',
                        aws_access_key_id = os.environ['ACCESS_ID'],
                        aws_secret_access_key = os.environ['ACCESS_KEY'])

    data = open(file, 'rb')
    s3.Bucket(bucket).put_object(Key='{}/{}'.format(emotion,file), Body=data)


