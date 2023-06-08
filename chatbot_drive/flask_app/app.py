import librosa
from flask import Flask, request, jsonify
from flask_cors import CORS

from actions.global_val import GlobalValue
from terminal_app.app import post

import base64

app = Flask(__name__)
CORS(app)

g_list = GlobalValue.global_list
res_url = g_list['RES_URL']

asr = g_list['ASR']
tts = g_list['TTS']


@app.route('/text_chat', methods=['POST'])
def text_chat():
    data = {'sender': request.json['sender'], 'message': request.json['message']}
    res = post(res_url, data)
    ret = []
    for item in res:
        if item['text']:
            texts = item['text'].split('\n')
            ret.append(texts[0])
            if len(texts) > 1:
                ret.append('\n'.join(texts[1:]))
    return jsonify({'code': 200, 'data': ret})


@app.route('/voice_chat_home', methods=['POST'])
def voice_chat():
    length = 0
    audio = b''
    wake_up = ('小软', '小阮', '小冉')
    input_file = request.files.get('input')
    if input_file is None:
        return jsonify({'code': 400, 'message': u'音频上传失败'})
    input_file.save('./input.wav')
    message = asr('./input.wav')
    print(message)
    data = {'sender': 'user', 'message': message}
    res = []
    if message.startswith(wake_up):
        res = post(res_url, data)
    ret = []
    for item in res:
        if item['text']:
            texts = item['text'].split('\n')
            ret.append(texts[0])
            if len(texts) > 1:
                ret.append('\n'.join(texts[1:]))
    if '开机' in message:
        if len(ret) > 0 and ret[0].startswith('好的'):
            ret = []
    if len(ret) > 0:
        tts(text=ret[0], output='./output.wav')
        length = librosa.get_duration(filename='./output.wav')
        with open('./output.wav', 'rb') as f:
            audio = f.read()

    return jsonify(
        {'code': 200, 'file': base64.b64encode(audio).decode() if len(ret) > 0 else None, 'length': int(length),
         'data': ret})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
