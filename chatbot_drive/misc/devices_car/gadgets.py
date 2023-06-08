class Window:
    def __init__(self, name):
        self.name = name
        self.state = False

    def on(self):
        if self.state:
            return f'{self.name}窗户已打开'
        else:
            self.state = True
            return f'好的，{self.name}窗户已打开'

    def off(self):
        if not self.state:
            return f'{self.name}窗户已关闭'
        else:
            self.state = False
            return f'好的，{self.name}窗户已关闭'

    def state_to_str(self):
        return '打开' if self.state else '关闭'

    def __str__(self):
        return f'{self.name}窗户\n状态：{self.state_to_str()}\n'


class Seat:
    def __init__(self, name):
        self.name = name
        self.features = {
            '座椅加热': False,
            '座椅通风': False,
        }
        self.position = {
            '座椅位置': 0,
            '椅背角度': 90,
            '座椅高度': 0,
        }
        self.max_pos = 4
        self.min_pos = -4
        self.max_angle = 150
        self.min_angle = 90
        self.max_height = 5
        self.min_height = -5

    def on_heat(self):
        self.features['座椅通风'] = False
        self.features['座椅加热'] = True
        return f'好的，{self.name}座椅加热已打开'

    def off_heat(self):
        self.features['座椅加热'] = False
        return f'好的，{self.name}座椅加热已关闭'

    def on_air(self):
        self.features['座椅通风'] = True
        self.features['座椅加热'] = False
        return f'好的，{self.name}座椅通风已打开'

    def off_air(self):
        self.features['座椅通风'] = False
        return f'好的，{self.name}座椅通风已关闭'

    def forward_pos(self):
        if self.position['座椅位置'] == self.max_pos:
            return '无法再向前调整该座椅'
        self.position['座椅位置'] += 1
        return f'好的，{self.name}座椅已向前调整'

    def backward_pos(self):
        if self.position['座椅位置'] == self.min_pos:
            return '无法再向后调整该座椅'
        self.position['座椅位置'] -= 1
        return f'好的，{self.name}座椅已向后调整'

    def lift(self):
        if self.position['座椅高度'] == self.max_height:
            return '无法再调高该座椅'
        self.position['座椅高度'] += 1
        return f'好的，{self.name}座椅已调高'

    def lower(self):
        if self.position['座椅高度'] == self.min_height:
            return '无法再调低该座椅'
        self.position['座椅高度'] -= 1
        return f'好的，{self.name}座椅已调低'

    def lay_down(self):
        if self.position['椅背角度'] == self.max_angle:
            return '无法再向后调整该座椅椅背'
        self.position['椅背角度'] += 10
        return f'好的，{self.name}椅背已向后调整'

    def sit_up(self):
        if self.position['椅背角度'] == self.min_angle:
            return '无法再向前调整该座椅椅背'
        self.position['椅背角度'] -= 10
        return f'好的，{self.name}椅背已向前调整'

    def __str__(self):
        text = ''
        text += f'{self.name}座位\n'
        text += ('座椅通风：打开\n' if self.features['座椅通风'] else '座椅通风：关闭\n')
        text += ('座椅加热：打开\n' if self.features['座椅加热'] else '座椅加热：关闭\n')
        for key in self.position.keys():
            text += f'{key}：{self.position[key]}\n'
        return text


class Mirror:
    def __init__(self, name):
        self.name = name
        self.min_angle = 60
        self.max_angle = 120
        self.angle = 90

    def outer(self):
        if self.angle + 2 > self.max_angle:
            self.angle = self.max_angle
        else:
            self.angle += 2
        return f'好的，{self.name}侧后视镜已向外旋转'

    def inner(self):
        if self.angle - 2 < self.min_angle:
            self.angle = self.min_angle
        else:
            self.angle -= 2
        return f'好的，{self.name}侧后视镜已向内旋转'

    def __str__(self):
        text = ''
        text += f'{self.name}后视镜\n'
        text += f'角度：{self.angle}\n'
        return text
