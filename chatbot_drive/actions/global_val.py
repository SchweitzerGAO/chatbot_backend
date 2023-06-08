from paddlespeech.cli.asr import ASRExecutor
from paddlespeech.cli.tts import TTSExecutor
from paddlespeech.server.bin.paddlespeech_client import TTSOnlineClientExecutor
from misc.devices_car import *


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
            cls.global_list['RES_URL'] = 'http://localhost:5006/webhooks/rest/webhook'
            cls.global_list['TTS_SERVER'] = TTSOnlineClientExecutor()
            cls.global_list['TTS'] = TTSExecutor()
            cls.global_list['ASR'] = ASRExecutor()
            cls.global_list['ac'] = AirConditioner('空调')
            cls.global_list['stereo'] = Stereo('音箱')
            cls.global_list['phone'] = Phone('电话')
            cls.global_list['navigator'] = Navigator('导航')
            cls.global_list['windows'] = [Window('天窗'), Window('左前方'), Window('左后方'), Window('右前方'),
                                          Window('右后方')]
            cls.global_list['seats'] = [Seat('驾驶'), Seat('副驾驶')]
            cls.global_list['mirrors'] = [Mirror('左'), Mirror('右')]

        return cls._instance
