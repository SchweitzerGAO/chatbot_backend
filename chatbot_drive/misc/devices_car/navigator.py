class Navigator:
    def __init__(self, name):
        self.name = name
        self.dept = '您的位置'
        self.dest = ''

    def set_locations(self, dest, dept=None):
        self.dest = dest
        if dept is not None:
            self.dept = dept
        return f'好的，已为您规划从{self.dept}到{self.dest}的路线'

    def __str__(self):
        return f'{self.name}\n起点：{self.dept}\n终点：{self.dest}\n'
