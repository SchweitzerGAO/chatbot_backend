from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.global_val import GlobalValue

g_list = GlobalValue.global_list

stereo = g_list['stereo']


class ActionRandomPlay(Action):
    def name(self) -> Text:
        return 'action_random_play'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        text = stereo.random_play()
        dispatcher.utter_message(f'{text}\n{str(stereo)}')
        print(str(stereo))
        return []


class ActionPlaySong(Action):
    def name(self) -> Text:
        return 'action_play_song'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            singer = tracker.get_slot('singer')
            song = tracker.get_slot('song')
            times = tracker.get_slot('time')
            to_play = song
            if singer is not None:
                to_play = f'{singer}的' + to_play
            text = stereo.play(to_play, times)
            dispatcher.utter_message(f'{text}\n{str(stereo)}')
            print(str(stereo))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('singer', None),
                    SlotSet('song', None)]


class ActionPause(Action):
    def name(self) -> Text:
        return 'action_pause'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        text = stereo.pause()
        dispatcher.utter_message(f'{text}\n{str(stereo)}')
        print(str(stereo))
        return []


class ActionReplay(Action):
    def name(self) -> Text:
        return 'action_replay'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        text = stereo.replay()
        dispatcher.utter_message(f'{text}\n{str(stereo)}')
        print(str(stereo))
        return []


class ActionQuit(Action):
    def name(self) -> Text:
        return 'action_quit'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        if not g_list['SESSION_START']:
            return [SessionStarted()]
        text = stereo.quit()
        dispatcher.utter_message(f'{text}\n{str(stereo)}')
        print(str(stereo))
        return []


class ActionAlterVolume(Action):
    def name(self) -> Text:
        return 'action_alter_volume'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        try:
            if not g_list['SESSION_START']:
                return [SessionStarted()]
            op = tracker.get_slot('operation_alter_volume')
            if '高' in op or '大' in op:
                text = stereo.up_volume()
            elif '低' in op or '小' in op:
                text = stereo.down_volume()
            else:
                raise NotImplementedError
            dispatcher.utter_message(f'{text}\n{str(stereo)}')
            print(str(stereo))
        except Exception as e:
            print(e)
            dispatcher.utter_message(response='utter_default')
        finally:
            return [SlotSet('operation_alter_volume', None)]
