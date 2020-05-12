# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import random

class ActionTemperatura(Action):

    def name(self) -> Text:
        return "action_temperatura"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        value = random.randint(20, 45)
        text = "A temperatura atual do solo é de {} graus.".format(value)

        dispatcher.utter_message(text=text)

        return []

class ActionUmidade(Action):

    def name(self) -> Text:
        return "action_umidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        value = random.randint(0, 100)
        text = "A umidade atual do solo é de {}%.".format(value)

        dispatcher.utter_message(text=text)

        return []

class ActionPH(Action):

    def name(self) -> Text:
        return "action_ph"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        value = random.randint(1, 10)
        text = "O ph atual do solo é de {}.".format(value)

        dispatcher.utter_message(text=text)

        return []

