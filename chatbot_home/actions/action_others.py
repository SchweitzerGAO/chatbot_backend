from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue
from misc.query.query import query_time_location_weather

g_list = GlobalValue().global_list


class ActionWelcome(Action):

    def name(self) -> Text:
        return 'action_welcome'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if g_list['SESSION_START']:
            return []
        g_list['SESSION_START'] = True
        date, hour, location, weather, min_temp, max_temp, now_temp, now_feel = query_time_location_weather()
        if 6 <= hour < 9:
            greet = f'早上好！今天是{date}，{location}今天{weather},{min_temp}~{max_temp}℃。请问有什么可以帮助你的吗？'
        elif 9 <= hour < 12:
            greet = f'上午好！今天是{date}，{location}今天{weather},{min_temp}~{max_temp}℃。请问有什么可以帮助你的吗？'
        elif 12 <= hour < 18:
            greet = f'下午好！现在温度{now_temp}℃，体感温度{now_feel}℃。请问有什么可以帮助你的吗？'
        elif 18 <= hour <= 23:
            greet = f'晚上好！现在温度{now_temp}℃，体感温度{now_feel}℃。请问有什么可以帮助你的吗？'
        else:
            greet = f'夜深了，要多注意休息哦。现在温度{now_temp}℃，体感温度{now_feel}℃。请问有什么可以帮助你的吗？'
        dispatcher.utter_message(text=greet)

        return []


class ActionGreet(Action):

    def name(self) -> Text:
        return 'action_greet'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        dispatcher.utter_message(response='utter_greet')
        return []


class ActionSelfIntroduction(Action):

    def name(self) -> Text:
        return 'action_self_introduction'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        dispatcher.utter_message(response='utter_self_introduction')
        return []


class ActionGoodbye(Action):

    def name(self) -> Text:
        return 'action_goodbye'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        dispatcher.utter_message(response='utter_goodbye')
        g_list['SESSION_START'] = False
        return [SessionStarted()]


class ActionResponseDeny(Action):

    def name(self) -> Text:
        return 'action_response_deny'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        dispatcher.utter_message(response='utter_response_deny')
        return []
