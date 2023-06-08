device_dict = {
    '电视': 'tv',
    '空调': 'ac',
    '灯': 'light',
    '音量升高': 'tv',
    '音量降低': 'tv',
    '温度升高': 'ac',
    '温度降低': 'ac',
    '风量升高': 'ac',
    '风量降低': 'ac',
    '亮度升高': 'light',
    '亮度降低': 'light',
    '调整': 'ac',
    '开': 'ac',
    '关': 'ac',
}
op_onoff_dict = {
    '开': True,
    '关': False,
}

op_attr_dict = {
    '音量升高': 'up_volume',
    '音量降低': 'down_volume',
    '静音': 'mute',
    '温度升高': ['up_temp_val', 'up_temp'],
    '温度降低': ['down_temp_val', 'down_temp'],
    '风量升高': 'up_strength',
    '风量降低': 'down_strength',
    '亮度升高': 'up_bright',
    '亮度降低': 'down_bright',
    '调整': ['alter_temp']
}

op_mm_dict = {
    '播放': ['replay', 'play'],
    '暂停': 'pause',
    '关': 'quit',
}
