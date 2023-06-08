from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list

mirrors = g_list['mirrors']


class ActionMirror(Action):
    def name(self) -> Text:
        return 'action_operate_mirror'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            mirror_name = tracker.get_slot('mirror_name')
            mirror_operation = tracker.get_slot('mirror_operation')
            if mirror_name is not None:
                if '左' in mirror_name:
                    mirror = mirrors[0]
                else:
                    mirror = mirrors[1]
            else:
                mirror = mirrors
            if '里' in mirror_operation or '内' in mirror_operation:
                if isinstance(mirror, list):
                    for m in mirror:
                        m.inner()
                    text = '好的，两侧后视镜均已向内旋转'
                else:
                    text = mirror.inner()
            elif '外' in mirror_operation:
                if isinstance(mirror, list):
                    for m in mirror:
                        m.outer()
                    text = '好的，两侧后视镜均已向外旋转'
                else:
                    text = mirror.outer()
            else:
                raise Exception
            dispatcher.utter_message(f'{text}\n{str(mirror)}')
            if isinstance(mirror, list):
                for m in mirror:
                    print(str(m))
            else:
                print(str(mirror))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('mirror_name', None), SlotSet('mirror_operation', None)]
