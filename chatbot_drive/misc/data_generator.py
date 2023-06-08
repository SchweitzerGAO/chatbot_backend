import random
import cn2an

wake_up = ['小软小软，', '小软同学，', '小冉小冉，', '小阮小阮，', '小冉同学，', '小阮同学，']


def lookup_location():
    locations = []
    with open('../data/THUOCL_diming.txt', 'r', encoding='utf-8') as f:
        for line in f:
            loc = line.strip().split()[0]
            print(loc)
            locations.append(loc)
    with open('../data/lookup/lookup_location.yml', 'a', encoding='utf-8') as f:
        for loc in locations:
            f.write(f'    - {loc}\n')


def lookup_name():
    names = []
    length = 500000
    with open('../data/names.csv', 'r', encoding='utf-8') as f:
        for line in f:
            if len(names) >= length:
                break
            else:
                add = bool(random.getrandbits(1))
                if add:
                    names.append(line.strip())
    with open('../data/lookup/lookup_name.yml', 'a', encoding='utf-8') as f:
        for name in names:
            f.write(f'    - {name}\n')


def create_phone_number():
    second = [3, 4, 5, 6, 7, 8, 9][random.randint(0, 6)]
    third = {3: random.randint(0, 9),
             4: [5, 7, 9][random.randint(0, 2)],
             5: [i for i in range(10) if i != 4][random.randint(0, 8)],
             6: random.choice([2, 6]),
             7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
             8: random.randint(0, 9),
             9: [i for i in range(10) if i != 4][random.randint(0, 8)]}[second]

    suffix = random.randint(10000000, 99999999)

    # 拼接手机号
    return f'1{second}{third}{suffix}'


def generate_navigate_data(n=5000):
    sentences = set()
    locations = []
    with open('../data/lookup/lookup_location.yml', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                locations.append(line.strip().replace('- ', ''))
    template_without_departure = [
        '去[{}]{{"entity":"location","role":"destination"}}',
        '到[{}]{{"entity":"location","role":"destination"}}',
        '到[{}]{{"entity":"location","role":"destination"}}怎么走',
        '去[{}]{{"entity":"location","role":"destination"}}怎么走',
        '到[{}]{{"entity":"location","role":"destination"}}的路线是什么',
        '到[{}]{{"entity":"location","role":"destination"}}的路线',
        '去[{}]{{"entity":"location","role":"destination"}}的路线是什么',
        '去[{}]{{"entity":"location","role":"destination"}}的路线',
        '导航到[{}]{{"entity":"location","role":"destination"}}',

    ]
    template_with_departure = [
        '从[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}',
        '从[{}]{{"entity":"location","role":"departure"}}到[{}]{{"entity":"location","role":"destination"}}',
        '从[{}]{{"entity":"location","role":"departure"}}到[{}]{{"entity":"location","role":"destination"}}怎么走',
        '从[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}怎么走',
        '[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}',
        '[{}]{{"entity":"location","role":"departure"}}到[{}]{{"entity":"location","role":"destination"}}',
        '[{}]{{"entity":"location","role":"departure"}}到[{}]{{"entity":"location","role":"destination"}}怎么走',
        '[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}怎么走',
        '从[{}]{{"entity":"location","role":"departure"}}到[{}]{{"entity":"location","role":"destination"}}的路线是什么',
        '[{}]{{"entity":"location","role":"departure"}}到[{}]{{"entity":"location","role":"destination"}}的路线',
        '从[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}的路线是什么',
        '[{}]{{"entity":"location","role":"departure"}}去[{}]{{"entity":"location","role":"destination"}}的路线',
    ]
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        has_dept = bool(random.getrandbits(1))
        dept = random.choice(locations)
        dest = random.choice(locations)
        if has_wake:
            sentence += random.choice(wake_up)
        if has_dept:
            if dept == dest:
                continue
            else:
                sentence += random.choice(template_with_departure).format(dept, dest)
        else:
            sentence += random.choice(template_without_departure).format(dest)
        sentences.add(sentence)
    with open('../data/intent/intent_navigate.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_ac_on_off(n=50):
    template = [
        '[{}](operation_onoff)空调',
        '把空调[{}](operation_onoff)',
    ]
    operation_on = ['打开', '开', '开启']
    operation_off = ['关闭', '关', '关上', '关掉', '关了']
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        on_off = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if on_off:
            sentence += random.choice(template).format(random.choice(operation_on))
        else:
            sentence += random.choice(template).format(random.choice(operation_off))
        sentences.add(sentence)
    with open('../data/intent/intent_ac.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_set_temp(n=250):
    template = [
        '[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '空调[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把空调[{}](operation_set_temp)[{}]{{"entity":"value","role":"temperature"}}度',
    ]
    operation_set_temp = [
        '温度降低到', '温度升高到', '温度升高至', '温度降低至', '温度调整到', '温度调整至', '温度调到', '温度调至',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        is_zh = bool(random.getrandbits(1))
        temperature = random.randint(16, 30)
        if is_zh:
            temperature = cn2an.an2cn(temperature)
        if has_wake:
            sentence += random.choice(wake_up)
        sentence += random.choice(template).format(random.choice(operation_set_temp), temperature)
        sentences.add(sentence)
    with open('../data/intent/intent_ac.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_alter_temp(n=750):
    template_without_temp = [
        '[{}](operation_alter_temp)',
        '[{}](operation_alter_temp)一些',
        '[{}](operation_alter_temp)一点',
        '空调[{}](operation_alter_temp)',
        '把空调[{}](operation_alter_temp)',
        '空调[{}](operation_alter_temp)一些',
        '把空调[{}](operation_alter_temp)一些',
        '空调[{}](operation_alter_temp)一点',
        '把空调[{}](operation_alter_temp)一点',

    ]
    template_with_temp = [
        '[{}](operation_alter_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '空调[{}](operation_alter_temp)[{}]{{"entity":"value","role":"temperature"}}度',
        '把空调[{}](operation_alter_temp)[{}]{{"entity":"value","role":"temperature"}}度',
    ]

    operation_high = [
        '温度上升',
        '温度调高',
        '温度升',
        '温度高',
        '温度升高',
    ]
    operation_low = [
        '温度下降',
        '温度调低',
        '温度低',
        '温度降',
        '温度降低',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        is_zh = bool(random.getrandbits(1))
        with_temp = bool(random.getrandbits(1))
        is_high = bool(random.getrandbits(1))

        temperature = random.randint(1, 5)
        if is_zh:
            temperature = cn2an.an2cn(temperature)
        if has_wake:
            sentence += random.choice(wake_up)
        if with_temp:
            if is_high:
                sentence += random.choice(template_with_temp).format(random.choice(operation_high), temperature)
            else:
                sentence += random.choice(template_with_temp).format(random.choice(operation_low), temperature)
        else:
            if is_high:
                sentence += random.choice(template_without_temp).format(random.choice(operation_high))
            else:
                sentence += random.choice(template_without_temp).format(random.choice(operation_low))

        sentences.add(sentence)
    with open('../data/intent/intent_ac.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_alter_strength(n=250):
    template = [
        '[{}](operation_alter_strength)',
        '[{}](operation_alter_strength)一点',
        '[{}](operation_alter_strength)一些',
        '空调[{}](operation_alter_strength)',
        '空调[{}](operation_alter_strength)一点',
        '空调[{}](operation_alter_strength)一些',
        '把空调[{}](operation_alter_strength)',
        '把空调[{}](operation_alter_strength)一点',
        '把空调[{}](operation_alter_strength)一些',

    ]

    operation_strong = [
        '风大',
        '大点风',
        '风调大',
        '调大风',
        '风调高',
        '调高风',
        '风速大',
        '大点风速',
        '风速调大',
        '调大风速',
        '风速调高',
        '调高风速',
        '风量大',
        '大点风量',
        '风量调大',
        '调大风量',
        '风量调高',
        '调高风量',
        '风速升高',
        '风量升高',
    ]
    operation_weak = [
        '风小',
        '小点风',
        '风调小',
        '调小风',
        '风调低',
        '调低风',
        '风量小',
        '小点风量',
        '风量调小',
        '调小风量',
        '风量调低',
        '调低风量',
        '风速小',
        '小点风速',
        '风速调小',
        '调小风速',
        '风速调低',
        '调低风速',
        '风量降低',
        '风速降低',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        is_strong = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if is_strong:
            sentence += random.choice(template).format(random.choice(operation_strong))
        else:
            sentence += random.choice(template).format(random.choice(operation_weak))
        sentences.add(sentence)
    with open('../data/intent/intent_ac.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_play_song(n=3000):
    singer = []
    song = []
    with open('../data/lookup/lookup_singer.yml', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                singer.append(line.replace('    - ', '').strip())
    with open('../data/lookup/lookup_song.yml', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                song.append(line.replace('    - ', '').strip())
    template_without_singer = [
        '播放[{}](song)[{}]{{"entity":"value","role":"time"}}遍',
        '给我播放[{}](song)[{}]{{"entity":"value","role":"time"}}次',
        '播放[{}](song)[{}]{{"entity":"value","role":"time"}}次',
        '给我播放[{}](song)[{}]{{"entity":"value","role":"time"}}遍',
        '播放[{}](song)',
        '给我播放[{}](song)',
        '想听[{}](song)'
    ]
    template_with_singer = [
        '播放[{}](singer)[{}](song)[{}]{{"entity":"value","role":"time"}}遍',
        '给我播放[{}](singer)[{}](song)[{}]{{"entity":"value","role":"time"}}次',
        '播放[{}](singer)的[{}](song)[{}]{{"entity":"value","role":"time"}}次',
        '给我播放[{}](singer)的[{}](song)[{}]{{"entity":"value","role":"time"}}遍',
        '想听[{}](singer)[{}](song)',
        '想听[{}](singer)的[{}](song)',
        '播放[{}](singer)[{}](song)',
        '给我播放[{}](singer)[{}](song)',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        has_singer = bool(random.getrandbits(1))
        is_zh = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if has_singer:
            idx = random.randint(0, len(template_with_singer) - 1)
            if idx <= 3:
                times = random.randint(2, 5)
                if is_zh:
                    times = cn2an.an2cn(times)
                sentence += template_with_singer[idx].format(random.choice(singer), random.choice(song), times)
            else:
                sentence += template_with_singer[idx].format(random.choice(singer), random.choice(song))
        else:
            idx = random.randint(0, len(template_without_singer) - 1)
            if idx <= 3:
                times = random.randint(2, 5)
                if is_zh:
                    times = cn2an.an2cn(times)
                sentence += template_without_singer[idx].format(random.choice(song), times)
            else:
                sentence += template_without_singer[idx].format(random.choice(song))
        sentences.add(sentence)
    with open('../data/intent/intent_stereo.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_alter_volume(n=250):
    operation_up = [
        '增大音量',
        '调高音量',
        '大点声',
        '大声点',
        '音量增大',
        '音量调高',
        '音量升高',
        '声音大点',
        '声音增大',
        '声音调高',
        '声音调大',
        '声音大',
        '声音大点',
        '声音高',
        '声音高点',
        '音量大',
        '音量大点',
        '音量高',
        '音量高点',
        '音量升高'
    ]
    operation_down = [
        '减小音量',
        '安静点',
        '调小音量',
        '小点声',
        '小声点',
        '声音减小',
        '声音降低',
        '声音调小',
        '声音调低',
        '声音小',
        '声音小点',
        '音量小',
        '音量低',
        '音量低点',
        '声音低',
        '声音低点',
        '音量降低'
    ]
    template = [
        '[{}](operation_alter_volume)',
        '[{}](operation_alter_volume)一些',
        '把[{}](operation_alter_volume)',
        '把[{}](operation_alter_volume)一些',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        is_up = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if is_up:
            sentence += random.choice(template).format(random.choice(operation_up))
        else:
            sentence += random.choice(template).format(random.choice(operation_down))
        sentences.add(sentence)
    with open('../data/intent/intent_stereo.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_pause(n=50):
    pause = [
        '暂停',
        '停止'
    ]
    template = [
        '{}',
        '{}播放',
        '{}这个音乐',
        '{}播放这首歌',
        '{}这首歌',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        sentence += random.choice(template).format(random.choice(pause))
        sentences.add(sentence)
    with open('../data/intent/intent_stereo.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_replay(n=50):
    replay = [
        '播放',
        '重播',
        '恢复播放'
    ]
    template = [
        '{}',
        '{}这个音乐',
        '{}这首歌',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        sentence += random.choice(template).format(random.choice(replay))
        sentences.add(sentence)
    with open('../data/intent/intent_stereo.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_quit(n=50):
    op_quit = [
        '关闭',
        '关',
        '关上',
        '关掉',
        '关了',
        '退出',
    ]
    template = [
        '{}',
        '{}播放',
        '{}这个音乐',
        '{}播放这首歌',
        '{}这首歌',
    ]

    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        sentence += random.choice(template).format(random.choice(op_quit))
        sentences.add(sentence)
    with open('../data/intent/intent_stereo.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_random_play(n=20):
    random_play = [
        '放首歌',
        '播放音乐',
        '放个音乐',
        '随便放个音乐',
        '随便放个歌'
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        sentence += random.choice(random_play)
        sentences.add(sentence)
    with open('../data/intent/intent_stereo.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_call_number(n=1000):
    template = [
        '给[{}](phone_number)打电话',
        '打电话给[{}](phone_number)',
        '拨打[{}](phone_number)',
        '拨[{}](phone_number)',
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        to_zh = bool(random.getrandbits(1))
        one_to_yao = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        number = create_phone_number()
        if to_zh:
            number = cn2an.an2cn(number, 'direct')
        if one_to_yao:
            number = number.replace('一', '幺')

        sentence += random.choice(template).format(number)
        sentences.add(sentence)
    with open('../data/intent/intent_phone.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_call_name(n=2000):
    names = []
    template = [
        '给[{}](name)打电话',
        '打电话给[{}](name)',
        '拨打[{}](name)的电话',
        '拨[{}](name)的电话',
    ]
    with open('../data/lookup/lookup_name.yml', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                names.append(line.replace('    - ', '').strip())
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        sentence += random.choice(template).format(random.choice(names))
        sentences.add(sentence)
    with open('../data/intent/intent_phone.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_operate_roof(n=50):
    template = [
        '[{}](operation_onoff)天窗',
        '把天窗[{}](operation_onoff)',
    ]
    operation_on = ['打开', '开', '开启']
    operation_off = ['关闭', '关', '关上', '关掉', '关了']
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        on_off = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if on_off:
            sentence += random.choice(template).format(random.choice(operation_on))
        else:
            sentence += random.choice(template).format(random.choice(operation_off))
        sentences.add(sentence)
    with open('../data/intent/intent_window.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_operate_window(n=500):
    template_with_pos = [
        '[{}](operation_onoff)[{}](window_position)窗户',
        '[{}](operation_onoff)[{}](window_position)窗',
        '把[{}](window_position)的窗户[{}](operation_onoff)',
        '把[{}](window_position)窗户[{}](operation_onoff)',
        '把[{}](window_position)的窗[{}](operation_onoff)',
        '把[{}](window_position)窗[{}](operation_onoff)',
    ]
    template_without_pos = [
        '[{}](operation_onoff)窗户',
        '把窗户[{}](operation_onoff)',
        '[{}](operation_onoff)窗',
        '把窗[{}](operation_onoff)',
    ]
    operation_on = ['打开', '开', '开启']
    operation_off = ['关闭', '关', '关上', '关掉', '关了']
    window_position = [
        '左后',
        '左侧后方',
        '左后方',
        '左前',
        '左侧前方',
        '左前方',
        '右后',
        '右侧后方',
        '右后方',
        '右前',
        '右侧前方',
        '右前方'
    ]
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        on_off = bool(random.getrandbits(1))
        with_pos = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if with_pos:
            idx = random.randint(0, len(template_with_pos) - 1)
            if idx <= 1:
                if on_off:
                    sentence += template_with_pos[idx].format(random.choice(operation_on),
                                                              random.choice(window_position))
                else:
                    sentence += template_with_pos[idx].format(random.choice(operation_off),
                                                              random.choice(window_position))
            else:
                if on_off:
                    sentence += template_with_pos[idx].format(random.choice(window_position),
                                                              random.choice(operation_on))
                else:
                    sentence += template_with_pos[idx].format(random.choice(window_position),
                                                              random.choice(operation_off))
        else:
            if on_off:
                sentence += random.choice(template_without_pos).format(random.choice(operation_on))
            else:
                sentence += random.choice(template_without_pos).format(random.choice(operation_off))

        sentences.add(sentence)
    with open('../data/intent/intent_window.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_operate_seat_feature(n=500):
    template_with_name = [
        '把[{}](seat_name)的[{}](seat_operation)[{}](operation_onoff)',
        '把[{}](seat_name)[{}](seat_operation)[{}](operation_onoff)',
        '[{}](operation_onoff)[{}](seat_name)的[{}](seat_operation)',
        '[{}](operation_onoff)[{}](seat_name)[{}](seat_operation)'

    ]
    template_without_name = [
        '[{}](operation_onoff)[{}](seat_operation)',
        '把[{}](seat_operation)[{}](operation_onoff)'
    ]
    seat_name = ['驾驶', '副驾驶', '驾驶座', '副驾驶座', '驾驶位', '副驾驶位', '副驾']
    seat_operation = ['座椅加热', '座椅通风', '加热', '通风']
    operation_on = ['打开', '开', '开启']
    operation_off = ['关闭', '关', '关上', '关掉', '关了']
    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        on_off = bool(random.getrandbits(1))
        with_name = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if with_name:
            idx = random.randint(0, len(template_with_name) - 1)
            if idx <= 1:
                if on_off:
                    sentence += template_with_name[idx].format(random.choice(seat_name),
                                                               random.choice(seat_operation),
                                                               random.choice(operation_on))
                else:
                    sentence += template_with_name[idx].format(random.choice(seat_name),
                                                               random.choice(seat_operation),
                                                               random.choice(operation_off))
            else:
                if on_off:
                    sentence += template_with_name[idx].format(random.choice(operation_on),
                                                               random.choice(seat_name),
                                                               random.choice(seat_operation))
                else:
                    sentence += template_with_name[idx].format(random.choice(operation_off),
                                                               random.choice(seat_name),
                                                               random.choice(seat_operation))
        else:
            idx = random.randint(0, len(template_without_name) - 1)
            if idx == 0:
                if on_off:
                    sentence += template_without_name[idx].format(random.choice(operation_on),
                                                                  random.choice(seat_operation))
                else:
                    sentence += template_without_name[idx].format(random.choice(operation_off),
                                                                  random.choice(seat_operation))
            else:
                if on_off:
                    sentence += template_without_name[idx].format(random.choice(seat_operation),
                                                                  random.choice(operation_on))
                else:
                    sentence += template_without_name[idx].format(random.choice(seat_operation),
                                                                  random.choice(operation_off))
        sentences.add(sentence)
    with open('../data/intent/intent_seat.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_seat_up_down(n=200):
    template_with_name = [
        '把[{}](seat_name)[{}](seat_operation)一些',
        '把[{}](seat_name)[{}](seat_operation)',
        '把[{}](seat_name)[{}](seat_operation)一点',
        '[{}](seat_name)[{}](seat_operation)一些',
        '[{}](seat_name)[{}](seat_operation)',
        '[{}](seat_name)[{}](seat_operation)一点',
        '[{}](seat_operation)[{}](seat_name)',
        '[{}](seat_operation)一些[{}](seat_name)',
        '[{}](seat_operation)一点[{}](seat_name)'
    ]
    template_without_name = [
        '把座位[{}](seat_operation)',
        '把座位[{}](seat_operation)一些',
        '把座位[{}](seat_operation)一点',
        '把座椅[{}](seat_operation)',
        '把座椅[{}](seat_operation)一些',
        '把座椅[{}](seat_operation)一点',
        '座位[{}](seat_operation)',
        '座位[{}](seat_operation)一些',
        '座位[{}](seat_operation)一点',
        '座椅[{}](seat_operation)',
        '座椅[{}](seat_operation)一些',
        '座椅[{}](seat_operation)一点'
    ]

    seat_name = ['驾驶', '副驾驶', '驾驶座', '副驾驶座', '驾驶位', '副驾驶位', '副驾']

    operation_up = ['高', '调高', '高度上升', '高度升高', '高度调高', '座椅调高']
    operation_down = ['低', '调低', '高度下降', '高度降低', '高度调低', '座椅调低']

    operation_front = ['前', '向前', '座椅向前']
    operation_back = ['后', '向后', '座椅向后']

    operation_sit = ['椅背向前', '靠背向前', '椅背前', '靠背前', '椅背高', '靠背高', '椅背调高', '靠背调高']
    operation_lay = ['椅背向后', '靠背向后', '椅背后', '靠背后', '椅背低', '靠背低', '椅背调低', '靠背调低']

    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        up_down = bool(random.getrandbits(1))
        with_name = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if with_name:
            idx = random.randint(0, len(template_with_name) - 1)
            if idx <= 5:
                if up_down:
                    sentence += template_with_name[idx].format(random.choice(seat_name),
                                                               random.choice(operation_sit))
                else:
                    sentence += template_with_name[idx].format(random.choice(seat_name),
                                                               random.choice(operation_lay))
            else:
                if up_down:
                    sentence += template_with_name[idx].format(random.choice(operation_sit),
                                                               random.choice(seat_name))
                else:
                    sentence += template_with_name[idx].format(random.choice(operation_lay),
                                                               random.choice(seat_name))
        else:
            idx = random.randint(0, len(template_without_name) - 1)
            if up_down:
                sentence += template_without_name[idx].format(random.choice(operation_sit))
            else:
                sentence += template_without_name[idx].format(random.choice(operation_lay))
        sentences.add(sentence)
    with open('../data/intent/intent_seat.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


def generate_mirror(n=500):
    template_with_name = [
        '把[{}](mirror_name)[{}](mirror_operation)一些',
        '把[{}](mirror_name)[{}](mirror_operation)',
        '把[{}](mirror_name)[{}](mirror_operation)一点',
        '[{}](mirror_name)[{}](mirror_operation)一些',
        '[{}](mirror_name)[{}](mirror_operation)',
        '[{}](mirror_name)[{}](mirror_operation)',
        '[{}](mirror_name)[{}](mirror_operation)一点',
        '[{}](mirror_operation)[{}](mirror_name)',
        '[{}](mirror_operation)[{}](mirror_name)',
        '[{}](mirror_operation)一些[{}](mirror_name)',
        '[{}](mirror_operation)一些[{}](mirror_name)',
        '[{}](mirror_operation)一点[{}](mirror_name)'
    ]

    template_without_name = [
        '把后视镜[{}](mirror_operation)',
        '把后视镜[{}](mirror_operation)一些',
        '把后视镜[{}](mirror_operation)一点',
        '把倒车镜[{}](mirror_operation)',
        '把倒车镜[{}](mirror_operation)一些',
        '把倒车镜[{}](mirror_operation)一点',
        '后视镜[{}](mirror_operation)',
        '后视镜[{}](mirror_operation)一些',
        '后视镜[{}](mirror_operation)一点',
        '倒车镜[{}](mirror_operation)',
        '倒车镜[{}](mirror_operation)一些',
        '倒车镜[{}](mirror_operation)一点'
    ]
    mirror_names = ['左边后视镜', '左侧后视镜', '左方后视镜', '左侧倒车镜', '左方倒车镜', '左边倒车镜',
                    '右边后视镜', '右侧后视镜', '右方后视镜', '右侧倒车镜', '右方倒车镜', '右边倒车镜'
                    ]
    mirror_operations = ['向内转', '朝内转', '向外转', '向里转', '朝里转', '朝外转',
                         '向内', '朝内', '向外', '向里', '朝里', '朝外',
                         '向内旋转', '朝内旋转', '向外旋转', '向里旋转', '朝里旋转', '朝外旋转',
                         '向内调整', '朝内调整', '向外调整', '向里调整', '朝里调整', '朝外调整',
                         ]

    sentences = set()
    while len(sentences) < n:
        sentence = ''
        has_wake = bool(random.getrandbits(1))
        with_name = bool(random.getrandbits(1))
        if has_wake:
            sentence += random.choice(wake_up)
        if with_name:
            idx = random.randint(0, len(template_with_name) - 1)
            if idx <= 6:
                sentence += template_with_name[idx].format(random.choice(mirror_names),
                                                           random.choice(mirror_operations))
            else:
                sentence += template_with_name[idx].format(random.choice(mirror_operations),
                                                           random.choice(mirror_names))
        else:
            sentence += random.choice(template_without_name).format(random.choice(mirror_operations))

        sentences.add(sentence)
    with open('../data/intent/intent_mirror.yml', 'a', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(f'    - {sentence}\n')


if __name__ == '__main__':
    generate_mirror(n=1250)
