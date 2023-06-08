from paddlespeech.cli.asr import ASRExecutor
from paddlespeech.cli.tts import TTSExecutor
from paddlespeech.server.bin.paddlespeech_client import TTSOnlineClientExecutor


class GlobalValue:
    _instance = None
    global_list = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            orig = super(GlobalValue, cls)
            cls._instance = orig.__new__(cls)
        if not cls._instance.global_list:
            cls.global_list = dict()
            cls.global_list['SESSION_START'] = False
            cls.global_list['TTS_SERVER'] = TTSOnlineClientExecutor()
            cls.global_list['TTS'] = TTSExecutor()
            cls.global_list['ASR'] = ASRExecutor()
            cls.global_list['INTENT_URL'] = 'http://localhost:5005/model/parse'
            cls.global_list['RES_URL'] = 'http://localhost:5005/webhooks/rest/webhook'
        return cls._instance
