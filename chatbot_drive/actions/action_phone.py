from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list

phone = g_list['phone']


class ActionCallNumber(Action):
    def name(self) -> Text:
        return 'action_call_number'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            to = tracker.get_slot('phone_number')
            text = phone.phone_call_number(to)
            dispatcher.utter_message(f'{text}\n{str(phone)}')
            print(str(phone))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('phone_number', None)]


class ActionCallName(Action):
    def name(self) -> Text:
        return 'action_call_name'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            to = tracker.get_slot('name')
            text = phone.phone_call_name(to)
            dispatcher.utter_message(f'{text}\n{str(phone)}')
            print(str(phone))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('name', None)]
