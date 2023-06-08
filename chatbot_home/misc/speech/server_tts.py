from paddlespeech.server.bin.paddlespeech_server import ServerExecutor

if __name__ == '__main__':
    server_executor = ServerExecutor()
    server_executor(
        config_file="conf/server_conf_tts.yaml",
        log_file="./log/paddlespeech.log")
