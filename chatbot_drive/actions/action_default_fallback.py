from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return 'action_default_fallback'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        dispatcher.utter_message(response='utter_default')
        return [UserUtteranceReverted()]
