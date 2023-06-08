import random
import cn2an

class Stereo:
    def __init__(self, name):
        self.name = name
        self.volume = 40
        self.playing = ''
        self.play_state = False
        self.max_volume = 100
        self.min_volume = 0
        self.play_time = 1

    def is_mute(self):
        return self.volume == 0

    def state_to_str(self):
        if not self.play_state:
            if self.playing == '':
                return '未在播放'
            else:
                return '暂停'
        else:
            return '正在播放'

    def up_volume(self):
        if self.volume + 5 > self.max_volume:
            self.volume = self.max_volume
            return '已是最大音量'
        self.volume += 5
        return '好的，音量已升高'

    def down_volume(self):
        if self.volume - 5 < self.min_volume:
            self.volume = self.min_volume
            return '已静音'
        self.volume -= 5
        return '好的，音量已降低'

    def random_play(self):
        with open(r'D:\COURSE_WORK_Bachelor\毕业设计\final_project\ChatBot\chatbot_drive\data\lookup\lookup_song.yml', 'r',
                  encoding='utf-8') as f:
            lines = f.readlines()
            to_play = random.choice(lines[5:]).replace('    - ','').strip()
        text = self.play(to_play)
        return text

    def play(self, to_play, play_time=None):
        self.playing = to_play
        self.play_state = True
        if play_time is not None:
            play_time = int(cn2an.cn2an(play_time, 'smart'))
            self.play_time = play_time
        if self.play_time == 1:
            return f'好的，将为您播放{to_play}'
        else:
            return f'好的，将为您播放{to_play}{self.play_time}次'

    def pause(self):
        if self.play_state:
            self.play_state = False
            return '好的，已暂停'
        else:
            return '未播放音乐'

    def replay(self):
        if not self.play_state:
            self.play_state = True
            return f'好的，将为您继续播放{self.playing}'
        else:
            return '未暂停音乐'

    def quit(self):
        if self.playing != '':
            played = self.playing
            self.playing = ''
            self.play_state = False
            return f'好的，已关闭{played}'
        else:
            return '未播放音乐'

    def __str__(self):
        text = f'{self.name}\n状态：{self.state_to_str()}\n'
        if self.play_state:
            text += f'音量：{self.volume}\n'
            if self.playing:
                text += f'播放状态：{"正在播放" if self.play_state else "暂停"}\n'
                text += f'正在播放：{self.playing}\n'
                text += f'播放次数：{self.play_time}\n'
        return text
