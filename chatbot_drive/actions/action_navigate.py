from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list

navigator = g_list['navigator']


class ActionNavigate(Action):
    def name(self) -> Text:
        return 'action_navigate'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            dept = tracker.get_slot('departure')
            dest = tracker.get_slot('destination')
            text = navigator.set_locations(dest, dept)
            dispatcher.utter_message(f'{text}\n{str(navigator)}')
            print(str(navigator))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('departure', None), SlotSet('destination', None)]
