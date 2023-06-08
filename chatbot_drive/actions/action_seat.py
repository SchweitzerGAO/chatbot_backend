from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list

seats = g_list['seats']

seat_name_dict = {
    '驾驶': 0,
    '副驾驶': 1,
}
seat_position_dict = {
    '座椅调高': 'lift',
    '座椅调低': 'lower',
    '座椅向前': 'forward_pos',
    '座椅向后': 'backward_pos',
    '椅背向前': 'sit_up',
    '椅背向后': 'lay_down',
}


class ActionOperateSeatPosition(Action):
    def name(self) -> Text:
        return 'action_operate_seat_position'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            op_seat = tracker.get_slot('seat_operation')
            name = tracker.get_slot('seat_name')
            if op_seat not in seat_position_dict.keys():
                if '高' in op_seat:
                    op_seat = '座椅调高'
                elif '低' in op_seat:
                    op_seat = '座椅降低'
                elif '前' in op_seat:
                    if '椅背' in op_seat or '靠背' in op_seat or '后背' in op_seat:
                        op_seat = '椅背向前'
                    else:
                        op_seat = '座椅向前'
                elif '后' in op_seat:
                    if '椅背' in op_seat or '靠背' in op_seat or '后背' in op_seat:
                        op_seat = '椅背向后'
                    else:
                        op_seat = '座椅向后'
            if name is not None:
                if name not in seat_name_dict.keys():
                    if '副驾' in name:
                        name = '副驾驶'
                    elif '驾驶' in name:
                        name = '驾驶'
                    else:
                        raise NotImplementedError
                seat = seats[seat_name_dict[name]]
                op_fun = getattr(seat, seat_position_dict[op_seat], None)
                text = op_fun()
                dispatcher.utter_message(f'{text}\n{str(seat)}')
            else:
                for seat in seats:
                    op_fun = getattr(seat, seat_position_dict[op_seat], None)
                    op_fun()
                dispatcher.utter_message(text=f'所有{op_seat[0:2]}已{op_seat[2:]}')
            for seat in seats:
                print(str(seat))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('seat_name', None),
                    SlotSet('seat_operation', None)]


class ActionOperateSeatFeature(Action):
    def name(self) -> Text:
        return 'action_operate_seat_feature'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            text = None
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            op_on_off = tracker.get_slot('operation_onoff')
            op_seat = tracker.get_slot('seat_operation')
            name = tracker.get_slot('seat_name')
            if name is not None:
                seat = seats[seat_name_dict[name]]
                if '开' in op_on_off:
                    if '加热' in op_seat:
                        text = seat.on_heat()
                    elif '通风' in op_seat:
                        text = seat.on_air()
                    else:
                        raise NotImplementedError
                elif '关' in op_on_off:
                    if '加热' in op_seat:
                        text = seat.off_heat()
                    elif '通风' in op_seat:
                        text = seat.off_air()
                    else:
                        raise NotImplementedError
                dispatcher.utter_message(f'{text}\n{str(seat)}')
            else:
                if '开' in op_on_off:
                    for seat in seats:
                        if '加热' in op_seat:
                            seat.on_heat()
                        elif '通风' in op_seat:
                            seat.on_air()
                        else:
                            raise NotImplementedError
                    dispatcher.utter_message(f'座椅{op_seat}已打开')
                else:
                    for seat in seats:
                        if '加热' in op_seat:
                            seat.off_heat()
                        elif '通风' in op_seat:
                            seat.off_air()
                        else:
                            raise NotImplementedError
                    dispatcher.utter_message(f'座椅{op_seat}已打开')
            for seat in seats:
                print(str(seat))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_onoff', None),
                    SlotSet('seat_name', None),
                    SlotSet('seat_operation', None)]
