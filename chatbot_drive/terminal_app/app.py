import audioop
import datetime
import json
import queue
import threading
import time
import wave

import pyaudio
import requests

from actions.global_val import GlobalValue

'''
globals
'''
g_list = GlobalValue.global_list
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


'''
recording & de-noising
'''


def record_and_save_blocking():
    global waked
    global entered
    lower = 0
    frames = []
    form = pyaudio.paInt16
    channels = 2
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




'''
STT & NLP & TTS
'''


def s2t():
    text = None
    has_voice = record_and_save_blocking()
    if has_voice:
        text = asr(audio_file='./input.wav')
    message_queue.put(text)


def t2s(texts, output=True, play=True):
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
            # lock_msg.acquire()
            start = datetime.datetime.now()
            s2t()
            end = datetime.datetime.now()
            print('[Prompt] Stored')
            # print(f'<STT>: {(end - start).seconds} sec')
            # lock_msg.release()


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
            start = datetime.datetime.now()
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

                # lock_intent.acquire()
                get_intent(prompt, self.intent_url)
                print('[Intent] Inferred')
                # lock_intent.release()

                if entered >= 2:
                    waked = False
                    entered = 0
            end = datetime.datetime.now()
            # print(f'<NLP>: {(end - start).seconds} sec')


class ThreadTTS(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global active
        print('Start t2s thread')
        while active:
            start = datetime.datetime.now()
            texts = answer_queue.get()
            print('[Answer] Got')
            t2s(texts)
            if intent_queue.get() == 'goodbye':
                active = False
                exit(0)
            end = datetime.datetime.now()
            # print(f'<TTS>: {(end - start).seconds} sec')


def execute_chat_voice(intent_url, res_url):
    global waked
    global entered
    s2t()
    prompt = message_queue.get()

    wake_up = ('小软', '小阮', '小冉')
    if prompt is None or prompt == '':
        return True

    intent = post(intent_url, data={'text': prompt})
    intent = intent['intent']['name']
    if prompt.startswith(wake_up):
        waked = True
    if waked:
        entered += 1
        print(f'User: {prompt}')
        res = post(res_url, data={'sender': 'user', 'message': prompt})
        for item in res:
            if item['text']:
                t2s(item['text'])
        if entered >= 2:
            waked = False
            entered = 0
        if intent == 'goodbye':
            return False
    return True


def chat_voice_multi_thread():
    intent_url = 'http://localhost:5006/model/parse'
    res_url = 'http://localhost:5006/webhooks/rest/webhook'
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


def chat():
    intent_url = 'http://localhost:5006/model/parse'
    res_url = 'http://localhost:5006/webhooks/rest/webhook'
    cont = True
    voice = True
    execute_chat_text(intent_url, res_url, '/restart')
    if voice:
        generate_answer('开机', res_url)
        answers = answer_queue.get()
        t2s(answers)
    else:
        execute_chat_text(intent_url, res_url, '开机')
    while cont:
        voice_in_loop = voice
        if voice_in_loop:
            cont = execute_chat_voice(intent_url, res_url)
        else:
            prompt = input('User: ')
            cont = execute_chat_text(intent_url, res_url, prompt)


if __name__ == '__main__':
    chat_voice_multi_thread()
