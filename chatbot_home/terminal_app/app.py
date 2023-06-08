import json
import time

import pyaudio
import requests
import wave
import audioop

import threading

import queue
from actions.global_val import GlobalValue

'''
globals
'''
g_list = GlobalValue().global_list
tts = g_list['TTS_SERVER']
asr = g_list['ASR']
waked = False
entered = 0

message_queue = queue.Queue()
answer_queue = queue.Queue()
intent_queue = queue.Queue()

active = True


def post(url, data=None):
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode(encoding="utf-8")
    r = requests.post(url=url, data=data)
    r = json.loads(r.text)
    return r


def record_and_save_blocking():
    global waked
    global entered
    lower = 0
    frames = []
    form = pyaudio.paInt16
    channels = 1
    sr = 16000
    block_size = 2048
    threshold = 300
    wait_time = 5
    recorder = pyaudio.PyAudio()
    stream = recorder.open(format=form,
                           channels=channels,
                           rate=sr,
                           input=True)
    now = time.time()
    while True:
        data = stream.read(block_size)
        rms = audioop.rms(data, 2)
        if rms >= threshold:
            break
        if time.time() - now > wait_time:
            waked = False
            entered = 0
            return False

    print('recording')
    while True:
        frames.append(data)
        data = stream.read(block_size)
        rms = audioop.rms(data, 2)
        if rms < threshold:
            lower += 1
        else:
            lower = 0
        if lower >= 15:
            break
    with wave.open('./input.wav', 'wb') as f:
        print('saving')
        f.setnchannels(channels)
        f.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        f.setframerate(sr)
        f.writeframes(b''.join(frames))

    stream.stop_stream()
    stream.close()
    recorder.terminate()
    return True


def s2t(file='./input.wav'):
    text = None
    has_voice = record_and_save_blocking()
    if has_voice:
        text = asr(audio_file=file)
    message_queue.put(text)


def t2s(texts, output=False, play=True):
    if isinstance(texts, list):
        for text in texts:
            print(f'\033[0;34;40mXiaoRuan: {text}\033[0m')
            tts(
                input=text,
                server_ip='127.0.0.1',
                port=8092,
                protocol='http',
                spk_id=0,
                output='./output.wav' if output else None,
                play=play)
    else:
        print(f'\033[0;34;40mXiaoRuan: {texts}\033[0m')
        tts(
            input=texts,
            server_ip='127.0.0.1',
            port=8092,
            protocol='http',
            spk_id=0,
            output='./output.wav' if output else None,
            play=play)


def generate_answer(prompt, res_url):
    res = post(res_url, data={'sender': 'user', 'message': prompt})
    answers = []
    for item in res:
        if item['text']:
            answers.append(item['text'])
    answer_queue.put(answers)


def get_intent(prompt, intent_url):
    intent = post(intent_url, data={'text': prompt})
    intent = intent['intent']['name']
    intent_queue.put(intent)


class ThreadSTT(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global active
        print('Start s2t thread')
        while active:
            s2t()  # 进行 ASR 操作
            print('[Prompt] Stored')


class ThreadRasa(threading.Thread):
    def __init__(self, res_url, intent_url):
        super().__init__()
        self.res_url = res_url
        self.intent_url = intent_url

    def run(self):
        global waked
        global entered
        global active
        print('Start rasa thread')
        wake_up = ('小软', '小阮', '小冉')
        while active:
            prompt = message_queue.get()
            if prompt is None or prompt == '':
                continue
            if prompt.startswith(wake_up):
                waked = True
            if waked:
                entered += 1
                print('[Prompt] Got')
                print(f'User: {prompt}')
                generate_answer(prompt, self.res_url)
                print('[Answer] Generated')

                get_intent(prompt, self.intent_url)
                print('[Intent] Inferred')
                if entered >= 2:
                    waked = False
                    entered = 0
            else:
                continue


class ThreadTTS(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global active
        print('Start t2s thread')
        while active:
            texts = answer_queue.get()[0].split('\n')[0]
            print(texts)
            print('[Answer] Got')
            t2s(texts)  # 进行TTS操作
            if intent_queue.get() == 'goodbye':
                active = False
                exit(0)


def chat_voice_multi_thread():
    intent_url = g_list['INTENT_URL']
    res_url = g_list['RES_URL']
    execute_chat_text(intent_url, res_url, '/restart')

    generate_answer('开机', res_url)
    answers = answer_queue.get()
    t2s(answers)

    thread_s2t = ThreadSTT()
    thread_rasa = ThreadRasa(res_url, intent_url)
    thread_t2s = ThreadTTS()

    threads = []
    thread_s2t.start()
    thread_rasa.start()
    thread_t2s.start()
    threads.append(thread_s2t)
    threads.append(thread_rasa)
    threads.append(thread_t2s)

    for thread in threads:
        thread.join()


def execute_chat_text(intent_url, res_url, prompt):
    if prompt is None or prompt == '':
        return True
    intent = post(intent_url, data={'text': prompt})
    intent = intent['intent']['name']
    res = post(res_url, data={'sender': 'user', 'message': prompt})
    for item in res:
        if item['text']:
            print(f'\033[0;34;40mXiaoRuan: {item["text"]}\033[0m')

    if intent == 'goodbye':
        return False
    return True


if __name__ == '__main__':
    # record_and_save_blocking()
    # s2t()
    # chat()
    chat_voice_multi_thread()
