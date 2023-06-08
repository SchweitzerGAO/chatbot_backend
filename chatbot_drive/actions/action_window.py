from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list

windows = g_list['windows']

window_loc_dict = {
    '左前方': 1,
    '左后方': 2,
    '右前方': 3,
    '右后方': 4,
}


class ActionOperateRoof(Action):
    def name(self) -> Text:
        return 'action_operate_roof'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            op = tracker.get_slot('operation_onoff')
            roof = windows[0]
            if '开' in op:
                text = roof.on()
            else:
                text = roof.off()
            dispatcher.utter_message(f'{text}\n{str(roof)}')
            print(str(roof))
        except Exception as e:
            print(e)
            dispatcher.utter_message('utter_default')
        finally:
            return [SlotSet('departure', None), SlotSet('destination', None)]


class ActionOperateWindow(Action):
    def name(self) -> Text:
        return 'action_operate_window'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            op = tracker.get_slot('operation_onoff')
            loc = tracker.get_slot('window_position')
            if loc is not None:
                window = windows[window_loc_dict[loc]]
                if '开' in op:
                    text = window.on()
                else:
                    text = window.off()
                dispatcher.utter_message(f'{text}\n{str(window)}')
            else:
                if '开' in op:
                    for window in windows[1:]:
                        window.on()
                    dispatcher.utter_message('好的，所有窗户均已打开')
                else:
                    for window in windows[1:]:
                        window.off()
                    dispatcher.utter_message('好的，所有窗户均已关闭')
            for window in windows[1:]:
                print(str(window))
        except Exception as e:
            print(e)
            dispatcher.utter_message('utter_default')
        finally:
            return [SlotSet('operation_onoff', None), SlotSet('window_position', None)]



