import random
import cn2an


def read_mm_name():
    mm_name = []
    with open('../../data/lookup/lookup_mm_name.yml', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                mm_name.append(line.strip().replace('- ', ''))
    return mm_name


def read_singers():
    singers = []
    with open('../../data/lookup/lookup_singer.yml', 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                singers.append(line.strip().replace('- ', ''))
    return singers


def generate_data_mm(data, singers, n=200):
    st = [False] * len(data)
    watch = ['想看', '播放']
    listen = ['想听', '播放']
    for _ in range(n):
        value = None
        singer = None
        op = None
        sentence = '- '
        has_op = bool(random.getrandbits(1))
        more = bool(random.getrandbits(1))
        has_value = bool(random.getrandbits(1))
        value_zh = bool(random.getrandbits(1))
        has_singer = bool(random.getrandbits(1))
        data_idx = random.randint(0, len(data) - 1)
        if not st[data_idx]:
            st[data_idx] = True
            if data_idx >= 448:
                if has_op:
                    op = listen[random.randint(0, 1)]
                if has_singer:
                    singer = singers[random.randint(0, len(singers) - 1)]
            else:
                if has_op:
                    op = watch[random.randint(0, 1)]
                if has_value:
                    value = random.randint(1, 20)
                    if value_zh:
                        value = cn2an.an2cn(value)
            if more:
                if op is not None:
                    sentence += '给我' if op == '播放' else '我'
            sentence += f'{"[" + op + "]" + "(operation_mm)" if op is not None else ""}' \
                        f'{"[" + singer + "]" + "(singer)" if singer is not None else ""}' \
                        f'{"的" if more and singer is not None else ""}' \
                        f'[{data[data_idx]}](mm_name)'
            if value is not None:
                if value_zh:
                    sentence += f'[第{value}](value)集'
                else:
                    sentence += f'第[{value}](value)集'
            print(sentence)


def generate_data_feature(n=100):
    patterns = ['- 小软同学[{}](operation_attr)[{}](mode)',
                '- 小冉同学[{}](operation_attr)[{}](mode)',
                '- 小阮同学[{}](operation_attr)[{}](mode)',
                '- 小软小软[{}](operation_attr)[{}](mode)',
                '- 小冉小冉[{}](operation_attr)[{}](mode)',
                '- 小阮小阮[{}](operation_attr)[{}](mode)',
                '- 小软同学[空调](device)[{}](operation_attr)[{}](mode)',
                '- 小冉同学[空调](device)[{}](operation_attr)[{}](mode)',
                '- 小阮同学[空调](device)[{}](operation_attr)[{}](mode)',
                '- 小软小软[空调](device)[{}](operation_attr)[{}](mode)',
                '- 小冉小冉[空调](device)[{}](operation_attr)[{}](mode)',
                '- 小阮小阮[空调](device)[{}](operation_attr)[{}](mode)',
                '- 小软同学把[{}](mode)[{}](operation_attr)',
                '- 小冉同学把[{}](mode)[{}](operation_attr)',
                '- 小阮同学把[{}](mode)[{}](operation_attr)',
                '- 小软小软把[{}](mode)[{}](operation_attr)',
                '- 小冉小冉把[{}](mode)[{}](operation_attr)',
                '- 小阮小阮把[{}](mode)[{}](operation_attr)',
                ]
    features = ['制冷', '制热', '除湿', '送风', '自动', '厨师', '智冷', '之冷', '致冷', '通风']
    on = ['打开', '调到', '调至', '切换']
    texts = set()
    for _ in range(n):
        arr = on
        idx = random.randint(0, len(patterns) - 1)
        if idx <= 11:
            text = patterns[idx].format(arr[random.randint(0, len(arr) - 1)],
                                        features[random.randint(0, len(features) - 1)])
        else:
            text = patterns[idx].format(features[random.randint(0, len(features) - 1)],
                                        arr[random.randint(0, len(arr) - 1)])
        texts.add(text)
    with open('./temp.txt', 'w', encoding='utf-8') as f:
        for t in texts:
            f.write(t + '\n')


def generate_data_wind():
    wind = ['风', '风量', '风速']
    up = ['大点', '调大', '调高']
    down = ['小点', '调小', '调低']
    for w in wind:
        for u in up:
            print('- [{}](operation_attr)'.format(w + u))
            print('- [{}](operation_attr)'.format(u + w))
        print('----------------------------------------')
        for d in down:
            print('- [{}](operation_attr)'.format(w + d))
            print('- [{}](operation_attr)'.format(d + w))
        print('----------------------------------------')


def generate_data_light(n=100):
    suffixes = ['一些', '一点']
    up = ['亮', '调亮', '变亮']
    down = ['暗', '调暗', '变暗']
    light = ['灯', '灯光', '电灯']
    texts = set()
    for _ in range(n):
        suf = bool(random.getrandbits(1))
        has_light = bool(random.getrandbits(1))
        up_down = bool(random.getrandbits(1))
        if up_down:
            arr = up
        else:
            arr = down
        text = f'[{arr[random.randint(0, len(arr) - 1)]}](operation_attr)'
        if has_light:
            text = f'[{light[random.randint(0, len(light) - 1)]}](device)' + text
        if suf:
            text += suffixes[random.randint(0, len(suffixes) - 1)]
        texts.add(text)
    for t in texts:
        print('- ' + t)


def generate_data_set_time(n=100):
    texts = set()
    hour_mins = ['    - 空调定时[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分',
                 '    - 空调定时[{}]{{"entity":"value","role":"hour"}}小时[{}]{{"entity":"value","role":"minute"}}分',
                 '    - 空调定时[{}]{{"entity":"value","role":"hour"}}小时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '    - 空调定时[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '    - 定时[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '    - 定时[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分',
                 '    - 定时[{}]{{"entity":"value","role":"hour"}}小时[{}]{{"entity":"value","role":"minute"}}分',
                 '    - 定时[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分钟', ]

    only_hours = ['    - 空调定时[{}]{{"entity":"value","role":"hour"}}时',
                  '    - 空调定时[{}]{{"entity":"value","role":"hour"}}小时',
                  '    - 定时[{}]{{"entity":"value","role":"hour"}}时',
                  '    - 定时[{}]{{"entity":"value","role":"hour"}}小时', ]

    only_mins = ['    - 空调定时[{}]{{"entity":"value","role":"minute"}}分',
                 '    - 空调定时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '    - 定时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '    - 定时[{}]{{"entity":"value","role":"minute"}}分', ]

    for _ in range(n):
        zh_hour = bool(random.getrandbits(1))
        zh_minute = bool(random.getrandbits(1))
        has_min = bool(random.getrandbits(1))
        has_hour = bool(random.getrandbits(1))
        half_hour = bool(random.getrandbits(1))
        minute = random.randint(1, 59)
        hour = random.randint(1, 10)
        hour_0 = bool(random.getrandbits(1))
        if has_min and has_hour:
            if 25 <= minute <= 35 and half_hour:
                pattern = only_hours[random.randint(0, len(only_hours) - 1)]
                hour = str(cn2an.an2cn(hour)) + '个半' if zh_hour else str(hour) + '个半'
                if hour_0:
                    hour = '半'
                text = pattern.format(hour)
                texts.add(text)
            else:
                if zh_hour:
                    hour = cn2an.an2cn(hour)
                if zh_minute:
                    minute = cn2an.an2cn(minute)
                pattern = hour_mins[random.randint(0, len(hour_mins) - 1)]
                texts.add(pattern.format(hour, minute))
        elif has_min:
            pattern = only_mins[random.randint(0, len(only_mins) - 1)]
            texts.add(pattern.format(minute))
        elif has_hour:
            pattern = only_hours[random.randint(0, len(only_hours) - 1)]
            texts.add(pattern.format(hour))

    with open('../../data/intent/intent_ac_set_time.yml', 'a', encoding='utf-8') as f:
        for t in texts:
            f.write(t + '\n')


def generate_data_hm(n=100):
    texts = set()
    hour_mins = ['[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分',
                 '[{}]{{"entity":"value","role":"hour"}}小时[{}]{{"entity":"value","role":"minute"}}分',
                 '[{}]{{"entity":"value","role":"hour"}}小时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分钟',
                 '[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分',
                 '[{}]{{"entity":"value","role":"hour"}}小时[{}]{{"entity":"value","role":"minute"}}分',
                 '[{}]{{"entity":"value","role":"hour"}}时[{}]{{"entity":"value","role":"minute"}}分钟', ]

    only_hours = ['[{}]{{"entity":"value","role":"hour"}}时',
                  '[{}]{{"entity":"value","role":"hour"}}小时',
                  '[{}]{{"entity":"value","role":"hour"}}时',
                  '[{}]{{"entity":"value","role":"hour"}}小时', ]

    only_mins = ['[{}]{{"entity":"value","role":"minute"}}分',
                 '[{}]{{"entity":"value","role":"minute"}}分钟',
                 '[{}]{{"entity":"value","role":"minute"}}分钟',
                 '[{}]{{"entity":"value","role":"minute"}}分', ]
    suffixes = ['把', '吧']
    prefixes = ['那就', '设定', '就']

    for _ in range(n):
        text = None
        zh_hour = bool(random.getrandbits(1))
        zh_minute = bool(random.getrandbits(1))
        has_min = bool(random.getrandbits(1))
        has_hour = bool(random.getrandbits(1))
        half_hour = bool(random.getrandbits(1))
        suf = bool(random.getrandbits(1))
        pre = bool(random.getrandbits(1))

        minute = random.randint(1, 59)
        hour = random.randint(1, 10)
        hour_0 = bool(random.getrandbits(1))
        if has_min and has_hour:
            if 25 <= minute <= 35 and half_hour:
                pattern = only_hours[random.randint(0, len(only_hours) - 1)]
                hour = str(cn2an.an2cn(hour)) + '个半' if zh_hour else str(hour) + '个半'
                if hour_0:
                    hour = '半'
                text = pattern.format(hour)
            else:
                if zh_hour:
                    hour = cn2an.an2cn(hour)
                if zh_minute:
                    minute = cn2an.an2cn(minute)
                pattern = hour_mins[random.randint(0, len(hour_mins) - 1)]
                text = pattern.format(hour, minute)
        elif has_min:
            pattern = only_mins[random.randint(0, len(only_mins) - 1)]
            text = pattern.format(minute)

        elif has_hour:
            pattern = only_hours[random.randint(0, len(only_hours) - 1)]
            text = pattern.format(hour)
        if text is not None:
            if pre:
                text = prefixes[random.randint(0, len(prefixes) - 1)] + text
            if suf:
                text += suffixes[random.randint(0, len(suffixes) - 1)]
            texts.add(text)

    with open('../../data/intent/intent_ac_set_time.yml', 'a', encoding='utf-8') as f:
        for t in texts:
            f.write('    - ' + t + '\n')


def read_intents(file):
    ret = []
    with open(file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                ret.append(line)
    return ret


def add_wake(examples, fold=3):
    length = len(examples)
    st = [False] * length
    num_sample = int(length / fold)
    for idx in range(length):
        examples[idx] = examples[idx].strip()
    for _ in range(num_sample):
        idx = random.randint(0, length - 1)
        if not st[idx]:
            rand_wake = random.choice(['小软小软', '小软同学', '小冉小冉', '小阮小阮', '小冉同学', '小阮同学'])
            examples[idx] = examples[idx].strip().replace('- ', '')
            examples[idx] = '- ' + rand_wake + examples[idx]
            st[idx] = True
    for ex in examples:
        print(ex)


if __name__ == '__main__':
    generate_data_feature(n=500)
