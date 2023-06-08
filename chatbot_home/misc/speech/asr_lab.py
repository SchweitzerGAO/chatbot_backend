from paddlespeech.cli.asr.infer import ASRExecutor
from paddlespeech.server.bin.paddlespeech_client import ASROnlineClientExecutor
import librosa
import soundfile as sf

asr = ASRExecutor()
asr_server = ASROnlineClientExecutor()


def resample(path, new_sample_rate=16000):
    signal, sr = librosa.load(path, sr=None)
    wavfile = path.split('/')[-1]
    wavfile = wavfile.split('.')[0]
    file_name = './samples/' + wavfile + '_new.wav'
    new_signal = librosa.resample(signal, sr, new_sample_rate)
    sf.write(file_name, new_signal, new_sample_rate)


def local_asr(file):
    result = asr(audio_file=file)
    print(result)


def server_asr(file):
    res = asr_server(
        input=file,
        server_ip="127.0.0.1",
        port=8090,
        sample_rate=16000,
        lang="zh_cn",
        audio_format="wav")
    print(res)


if __name__ == '__main__':
    local_asr('samples/input2_new.wav')
