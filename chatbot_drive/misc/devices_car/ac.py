import cn2an


class AirConditioner:
    def __init__(self, name):
        self.temperature = 25
        self.max_temp = 30
        self.min_temp = 16
        self.strength = 2
        self.state = False
        self.name = name

    def is_same_state(self, op):
        return self.state == op

    def turn_on_off(self):
        self.state = not self.state
        return f'好的，空调已{self.state_to_str()}'

    def state_to_str(self):
        if self.state:
            return '打开'
        return '关闭'

    def alter_up_temp(self):
        if self.temperature == self.max_temp:
            return f'好的，空调温度已调整到最高温度{self.temperature}℃'
        self.temperature += 1
        return f'好的，空调温度已调整到{self.temperature}℃'

    def alter_down_temp(self):
        if self.temperature == self.min_temp:
            return f'好的，空调温度已调整到最低温度{self.temperature}℃'
        self.temperature -= 1
        return f'好的，空调温度已调整到{self.temperature}℃'

    def alter_up_temp_val(self, val):
        val = int(cn2an.cn2an(val, 'smart'))
        if self.temperature + val > self.max_temp:
            self.temperature = self.max_temp
            return f'好的，空调温度已调整到最高温度{self.temperature}℃'
        self.temperature += val
        return f'好的，空调温度已调整到{self.temperature}℃'

    def alter_down_temp_val(self, val):
        val = int(cn2an.cn2an(val, 'smart'))
        if self.temperature - val < self.min_temp:
            self.temperature = self.min_temp
            return f'好的，空调温度已调整到最低温度{self.temperature}℃'
        self.temperature -= val
        return f'好的，空调温度已调整到{self.temperature}℃'

    def up_strength(self):
        if self.strength == 7:
            return '空调已是最高风速'
        self.strength += 1
        return f'好的，空调风速已调整到{self.strength}'

    def down_strength(self):
        if self.strength == 0:
            self.turn_on_off()
            return '空调已是最低风速'
        self.strength -= 1
        return f'好的，空调风速已调整到{self.strength}'

    def set_temp(self, val):
        val = cn2an.cn2an(val, 'smart')
        if val > self.max_temp:
            self.temperature = self.max_temp
            return f'好的，空调温度已调整到最高温度{self.temperature}℃'
        if val < self.min_temp:
            self.temperature = self.min_temp
            return f'好的，空调温度已调整到最低温度{self.temperature}℃'
        self.temperature = int(cn2an.cn2an(val, 'smart'))
        return f'好的，空调温度已调整到{self.temperature}℃'

    def __str__(self):
        text = f'{self.name}\n状态：{self.state_to_str()}\n'
        if self.state:
            text += f'温度：{self.temperature}\n风量：{self.strength}\n'
        return text
