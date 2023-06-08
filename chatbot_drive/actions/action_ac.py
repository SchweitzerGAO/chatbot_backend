from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue().global_list

ac = g_list['ac']


class ActionACOnOff(Action):
    def name(self) -> Text:
        return 'action_ac_on_off'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            op = tracker.get_slot('operation_onoff')
            op = True if op == '开' else False
            if ac.is_same_state(op):
                dispatcher.utter_message(f'{ac.name}已{ac.state_to_str()}\n{str(ac)}')
            else:
                text = ac.turn_on_off()
                dispatcher.utter_message(f'{text}\n{str(ac)}')
            print(str(ac))
            return [SlotSet('operation_onoff', None)]
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_onoff', None)]


class ActionAlterTemp(Action):
    def name(self) -> Text:
        return 'action_alter_temp'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            if not ac.state:
                dispatcher.utter_message('请先打开空调')
                return []
            op = tracker.get_slot('operation_alter_temp')
            temp = tracker.get_slot('temperature')
            if temp is None:
                if '高' in op:
                    text = ac.alter_up_temp()
                else:
                    text = ac.alter_down_temp()
            else:
                if '高' in op:
                    text = ac.alter_up_temp_val(temp)
                else:
                    text = ac.alter_down_temp_val(temp)
            dispatcher.utter_message(f'{text}\n{str(ac)}')
            print(str(ac))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_alter_temp', None),
                    SlotSet('temperature', None)]


class ActionSetTemp(Action):
    def name(self) -> Text:
        return 'action_set_temp'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            if not ac.state:
                dispatcher.utter_message('请先打开空调')
                return []
            temp = tracker.get_slot('temperature')
            text = ac.set_temp(temp)
            dispatcher.utter_message(f'{text}\n{str(ac)}')
            print(str(ac))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_set_temp', None),
                    SlotSet('temperature', None)]


class ActionAlterStrength(Action):
    def name(self) -> Text:
        return 'action_alter_strength'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            if not ac.state:
                dispatcher.utter_message('请先打开空调')
                return []
            op = tracker.get_slot('operation_alter_strength')
            if '高' in op or '大' in op:
                text = ac.up_strength()
            else:
                text = ac.down_strength()
            dispatcher.utter_message(f'{text}\n{str(ac)}')
            print(str(ac))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_alter_strength', None)]
