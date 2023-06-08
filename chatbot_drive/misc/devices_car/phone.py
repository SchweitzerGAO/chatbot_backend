import cn2an


class Phone:
    def __init__(self, name):
        self.name = name
        self.calling = ''

    def phone_call_number(self, to):
        to = int(cn2an.cn2an(to, 'smart'))
        self.calling = to
        return f'好的，正在为您呼叫{to}'

    def phone_call_name(self,to):
        self.calling = to
        return f'好的，正在为您呼叫{to}'

    def __str__(self):
        return f'{self.name}\n正在呼叫{self.calling}\n'
