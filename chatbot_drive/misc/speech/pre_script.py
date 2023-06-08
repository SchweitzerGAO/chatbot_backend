import os
import time

from paddlespeech.server.bin.paddlespeech_server import ServerExecutor
os.system("start cmd.exe /K rasa run --enable-api --cors * -p 5006")
os.system("start cmd.exe /K rasa run actions -p 5056")
server_executor = ServerExecutor()
server_executor(
        config_file="conf/server_conf_tts.yaml",
        log_file="./log/paddlespeech.log")
time.sleep(30)

