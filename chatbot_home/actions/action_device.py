from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, SessionStarted
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue
from misc.intel_device.devices import *
from misc.mapping_dict import *

g_list = GlobalValue().global_list

ac = AirConditioner(name='空调')
tv = Player(name='电视')
light = Light(name='灯')
g_list['ac'] = ac
g_list['tv'] = tv
g_list['light'] = light


def on_off(device_name_cn, operation, dispatcher: CollectingDispatcher):
    operation = op_onoff_dict.get(operation, None)
    if operation is None:
        dispatcher.utter_message(text='我不明白您要做什么，请再说一次好吗？')
        return
    device_name = device_dict.get(device_name_cn, None)
    if device_name is None:
        dispatcher.utter_message(text='我不明白您要操作什么设备，请再说一次好吗？')
        return
    device = g_list[device_name]
    if device.is_same_state(operation):
        dispatcher.utter_message(
            text=f'{device.name}已{device.state_to_str()}，无法再次进行{device.state_to_str()}操作\n{str(device)}')
    else:
        device.turn_on_off()
        dispatcher.utter_message(text=f'好的，已为您{device.state_to_str()}{device.name}\n{str(device)}')
        print(str(device))
        if isinstance(device, Player) and device.state:
            dispatcher.utter_message(text='想看些或听些什么呢？')


def modify_attr(device_name_cn, operation, temperature, mode, feature, dispatcher: CollectingDispatcher):
    op = None
    device = None
    if mode is not None:
        device = ac
        op = ['alter_mode']
    if feature is not None:
        device = ac
        operation = op_onoff_dict.get(operation, None)
        if operation is None:
            operation = True
        op = ['alter_feat']

    if device is None:
        device_name = device_dict.get(device_name_cn, None)
        if device_name is None:
            device_name = device_dict.get(operation, None)
        if device_name is None:
            dispatcher.utter_message(text='我不明白您要操作什么设备，请再说一次好吗？')
            return
        device = g_list[device_name]
    if not device.state:
        dispatcher.utter_message(text=f'{device.name}已{device.state_to_str()},请开启{device.name}\n{str(device)}')
        return

    op = op_attr_dict.get(operation, None) if op is None else op
    if op is None:
        dispatcher.utter_message(text='我不明白您要做什么，请再说一次好吗？')
        return
    if isinstance(op, str):
        resp = device.string_invoke(op)
    else:
        if temperature is not None:
            resp = device.string_invoke(op[0], val=temperature)
        elif mode is not None:
            resp = device.string_invoke(op[0], mode=mode)
        elif feature is not None:
            resp = device.string_invoke(op[0], feature=feature, op=operation)
        else:
            resp = device.string_invoke(op[1])
    dispatcher.utter_message(text=f'{resp}\n{str(device)}')
    print(str(device))


def operate_mm(operation, mm_name, episode, singer, dispatcher: CollectingDispatcher):
    device = tv
    if not device.state:
        dispatcher.utter_message(text=f'{device.name}已{device.state_to_str()},请开启{device.name}\n{str(device)}')
        return

    op = op_mm_dict.get(operation, None)
    if op is None:
        if mm_name is not None:
            op = op_mm_dict.get('播放', None)
        else:
            dispatcher.utter_message(text='我不明白您要做什么，请再说一次好吗？')
            return
    if isinstance(op, str):
        resp = device.string_invoke(op)
        dispatcher.utter_message(text=resp)
    else:
        if mm_name is None:
            if not device.play_state and device.playing:
                resp = device.string_invoke(op[0])
                dispatcher.utter_message(text=resp)
                print(str(device))
                return
            else:
                dispatcher.utter_message(text='未暂停任何视频或音频，无法恢复播放\n')
                return
        if episode is None:
            if singer is None:
                to_play = f' {mm_name}'
            else:
                to_play = f' {singer}的{mm_name}'
        else:
            if len(episode) > 1:
                episode = episode[1:]
            to_play = f'{mm_name} 第{int(cn2an.cn2an(episode, "smart"))}集'
        resp = device.string_invoke(op[1], to_play=to_play)
        dispatcher.utter_message(text=f'{resp}\n{str(device)}')
    print(str(device))


def ac_set_time(hour, minute, dispatcher: CollectingDispatcher):
    device = ac
    if not device.state:
        dispatcher.utter_message(text=f'{device.name}已{device.state_to_str()},请开启{device.name}\n{str(device)}')
        return
    form_h, form_m = device.set_time(hour, minute)
    if form_h == 0:
        dispatcher.utter_message(text=f'好的，空调已定时{form_m}分钟，之后空调将自动关闭\n{str(device)}')
    elif form_m == 0:
        dispatcher.utter_message(text=f'好的，空调已定时{form_h}小时，之后空调将自动关闭\n{str(device)}')
    else:
        dispatcher.utter_message(text=f'好的，空调已定时{form_h}小时{form_m}分钟，之后空调将自动关闭\n{str(device)}')
    print(str(device))


class ActionTurnOnOff(Action):
    def name(self) -> Text:
        return 'action_turn_on_off'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            operation = tracker.get_slot('operation_onoff')
            if operation is None:
                operation = tracker.get_slot('operation_mm')
            device = tracker.get_slot('device')
            on_off(device, operation, dispatcher)
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [
                SlotSet('operation_onoff', None),
                SlotSet('operation_mm', None),
                SlotSet('device', None),
            ]


class ActionModifyAttr(Action):
    def name(self) -> Text:
        return 'action_modify_attr'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            device = tracker.get_slot('device')
            operation = tracker.get_slot('operation_attr')
            if operation is None:
                operation = tracker.get_slot('operation_onoff')
            temperature = tracker.get_slot('temperature')
            mode = tracker.get_slot('mode')
            feature = tracker.get_slot('feature')
            modify_attr(device, operation, temperature, mode, feature, dispatcher)
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('temperature', None),
                    SlotSet('operation_attr', None),
                    SlotSet('operation_onoff', None),
                    SlotSet('device', None),
                    SlotSet('mode', None),
                    SlotSet('feature', None)
                    ]


class ActionOperateMM(Action):
    def name(self) -> Text:
        return 'action_operate_mm'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            operation = tracker.get_slot('operation_mm')
            if operation is None:
                operation = tracker.get_slot('operation_onoff')
            mm_name = tracker.get_slot('mm_name')
            episode = tracker.get_slot('episode')
            singer = tracker.get_slot('singer')
            operate_mm(operation, mm_name, episode, singer, dispatcher)
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_mm', None),
                    SlotSet('operation_onoff', None),
                    SlotSet('mm_name', None),
                    SlotSet('episode', None),
                    SlotSet('singer', None),
                    ]


class ActionRandomPlay(Action):
    def name(self) -> Text:
        return 'action_random_play'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        if not tv.state:
            dispatcher.utter_message('电视已关闭，请先打开电视')
        else:
            text = tv.random_play()
            print(str(tv))
            dispatcher.utter_message(text=text)
        return []


class ActionACSetTime(Action):
    def name(self) -> Text:
        return 'action_ac_set_time'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            h = tracker.get_slot('hour')
            m = tracker.get_slot('minute')
            ac_set_time(h, m, dispatcher)
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [
                SlotSet('hour', None),
                SlotSet('minute', None),
            ]


class ValidateACSetTimeForm(FormValidationAction):
    def name(self) -> Text:
        return 'validate_ac_set_time_form'

    def validate_hour(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        m = tracker.get_slot('minute')
        if slot_value is None and m is None:
            return {'hour': None, 'minute': None}
        if slot_value is None and m is not None:
            return {'hour': '0'}
        else:
            if m is None:
                return {'minute': '0'}
            return {'hour': slot_value, 'minute': m}

    def validate_minute(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        h = tracker.get_slot('hour')
        if slot_value is None and h is None:
            return {'hour': None, 'minute': None}
        if slot_value is None and h is not None:
            return {'minute': '0'}
        else:
            if h is None:
                return {'hour': '0'}
            return {'hour': h, 'minute': slot_value}
