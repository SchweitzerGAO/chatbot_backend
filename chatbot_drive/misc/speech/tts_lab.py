from paddlespeech.cli.tts.infer import TTSExecutor
from paddlespeech.server.bin.paddlespeech_client import TTSOnlineClientExecutor

tts = TTSExecutor()
tts_server = TTSOnlineClientExecutor()


def local_tts(text, output):
    tts(text=text, output=output)


def server_tts(text, output, play=False):
    tts_server(
        input=text,
        server_ip='127.0.0.1',
        port=8092,
        protocol='http',
        spk_id=0,
        output=output,
        play=play)


if __name__ == '__main__':
    server_tts('-3℃', './output.wav', True)
