import random

import cn2an
import datetime


class Device:
    def __init__(self, name):
        self.state = False
        self.name = name

    def is_same_state(self, op):
        return self.state == op

    def turn_on_off(self):
        self.state = not self.state

    def string_invoke(self, method, **kwargs):
        fun = getattr(self, method, None)
        return fun(**kwargs)

    def state_to_str(self):
        if self.state:
            return '打开'
        return '关闭'

    def __str__(self):
        raise NotImplementedError


class AirConditioner(Device):
    def __init__(self, name):
        super().__init__(name)
        self.mode = '自动'
        self.temperature = 25
        self.max_temp = 30
        self.min_temp = 16
        self.strength = 2
        self.str_strength = ['低', '中', '高']
        self.features = {
            '上下扫风': False,
            '左右扫风': False,
            '干燥': False,
            '辅热': False,
            '健康': False,
            '睡眠': False,
        }
        self.time = None

    def up_temp(self):
        if self.temperature == self.max_temp:
            return f'好的，空调温度已调整到最高温度{self.temperature}℃'
        self.temperature += 1
        return f'好的，空调温度已调整到{self.temperature}℃'

    def down_temp(self):
        if self.temperature == self.min_temp:
            return f'好的，空调温度已调整到最低温度{self.temperature}℃'
        self.temperature -= 1
        return f'好的，空调温度已调整到{self.temperature}℃'

    def up_temp_val(self, val):
        val = cn2an.cn2an(val, 'smart')
        if self.temperature + val > self.max_temp:
            self.temperature = self.max_temp
            return f'好的，空调温度已调整到最高温度{self.temperature}℃'
        self.temperature += val
        return f'好的，空调温度已调整到{self.temperature}℃'

    def down_temp_val(self, val):
        val = cn2an.cn2an(val, 'smart')
        if self.temperature - val < self.min_temp:
            self.temperature = self.min_temp
            return f'好的，空调温度已调整到最低温度{self.temperature}℃'
        self.temperature -= val
        return f'好的，空调温度已调整到{self.temperature}℃'

    def up_strength(self):
        if self.strength == 2:
            return '空调已是最高风速'
        self.strength += 1
        return f'好的，空调风速已调整到{self.str_strength[self.strength]}'

    def down_strength(self):
        if self.strength == 0:
            return '空调已是最低风速'
        self.strength -= 1
        return f'好的，空调风速已调整到{self.str_strength[self.strength]}'

    def alter_feat(self, feature, op):
        val = self.features.get(feature, None)
        if val is not None:
            self.features[feature] = op
        if op:
            return f'好的，已打开{feature}'
        else:
            return f'好的，已关闭{feature}'

    def alter_temp(self, val):
        val = cn2an.cn2an(val, 'smart')
        if val > self.max_temp:
            self.temperature = self.max_temp
            return f'好的，空调温度已调整到最高温度{self.temperature}℃'
        if val < self.min_temp:
            self.temperature = self.min_temp
            return f'好的，空调温度已调整到最低温度{self.temperature}℃'
        self.temperature = int(cn2an.cn2an(val, 'smart'))
        return f'好的，空调温度已调整到{self.temperature}℃'

    def alter_mode(self, mode):
        self.mode = mode

    def set_time(self, hour, minute):
        hour = hour.replace('个半', '点五')
        hour = hour.replace('半', '0.5')
        hour = cn2an.cn2an(hour, 'smart')
        hour = int(hour) if int(hour) == hour else hour
        minute = int(cn2an.cn2an(minute, 'smart'))
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=hour, minutes=minute)
        self.time = now + delta
        hour = delta.seconds // 3600
        minute = delta.seconds % 3600 // 60
        return hour, minute

    def strength_to_str(self):
        return self.str_strength[self.strength]

    def __str__(self):
        delta = None
        if self.time is not None:
            delta = self.time - datetime.datetime.now()
            if delta <= datetime.timedelta(hours=0, minutes=0, seconds=0):
                self.turn_on_off()
                text = f'{self.name}定时已到期\n状态：{self.state_to_str()}\n'
                return text

        text = f'{self.name}\n状态：{self.state_to_str()}\n'
        if self.state:
            on_features = ''
            for key in self.features.keys():
                if self.features[key]:
                    on_features += f'{key} '
            text += f'模式：{self.mode}\n温度：{self.temperature}\n风量：{self.strength_to_str()}\n功能：{on_features}\n'
            if delta is not None:
                text += f'定时剩余：{delta.seconds // 3600}:{delta.seconds // 60 % 60}:{delta.seconds % 60}\n'

        return text


class Player(Device):
    def __init__(self, name):
        super().__init__(name)
        self.volume = 40
        self.playing = ''
        self.play_state = False
        self.max_volume = 100
        self.min_volume = 0

    def is_mute(self):
        return self.volume == 0

    def up_volume(self):
        if self.volume + 5 > self.max_volume:
            self.volume = self.max_volume
            return '已是最大音量'
        self.volume += 5
        return '好的，音量已升高'

    def down_volume(self):
        if self.volume - 5 < self.min_volume:
            self.volume = self.min_volume
            return '电视已静音'
        self.volume -= 5
        return '好的，音量已降低'

    def mute(self):
        self.volume = 0
        return '好的，电视已静音'

    def play(self, to_play):
        self.playing = to_play
        self.play_state = True
        return f'好的，将为您播放{to_play}'

    def random_play(self):
        with open(r'D:\COURSE_WORK_Bachelor\毕业设计\final_project\ChatBot\chatbot_drive\data\lookup\lookup_song.yml', 'r',
                  encoding='utf-8') as f:
            lines = f.readlines()
            to_play = random.choice(lines[5:]).replace('    - ', '').strip()
        text = self.play(to_play)
        return text

    def pause(self):
        self.play_state = False
        return '好的，已暂停'

    def replay(self):
        self.play_state = True
        return f'好的，将为您继续播放{self.playing}'

    def quit(self):
        played = self.playing
        self.playing = ''
        self.play_state = False
        return f'好的，已关闭{played}'

    def __str__(self):
        text = f'{self.name}\n状态：{self.state_to_str()}\n'
        if self.state:
            text += f'音量：{self.volume}\n'
            if self.playing:
                text += f'播放状态：{"正在播放" if self.play_state else "暂停"}\n'
                text += f'正在播放：{self.playing}\n'
        return text


class Light(Device):
    def __init__(self, name):
        super().__init__(name)
        self.brightness = 50
        self.max_br = 100
        self.min_br = 0

    def up_bright(self):
        if self.brightness + 5 > self.max_br:
            self.brightness = self.max_br
            return '好的，灯光已为您调到最大亮度'
        self.brightness += 5
        return '好的，灯光已为您调亮'

    def down_bright(self):
        if self.brightness - 5 < self.max_br:
            self.brightness = self.min_br
            self.turn_on_off()
            return '好的，灯光现已关闭'
        self.brightness -= 5
        return '好的，灯光已为您调暗'

    def __str__(self):
        text = f'{self.name}\n状态：{self.state_to_str()}\n'
        if self.state:
            text += f'亮度：{self.brightness}\n'
        return text
