import requests
import logging

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import random
import time

logger = logging.getLogger(__name__)


def get_telegram_username(tracker):
    events = tracker.current_state()['events']
    user_events = []
    
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']


def verify_telegram(dispatcher, tracker):
    r = requests.get(
        'http://localhost:8000/api/telegram/verification/' + get_telegram_username(tracker))

    if r.status_code == 404:
        dispatcher.utter_message(
            text="Usuário não encontrado no sistema A2P2.")
        return None

    return r.json()


class ActionTemperatura(Action):

    def name(self) -> Text:
        return "action_temperatura"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = verify_telegram(dispatcher, tracker)

        if not response:
            return []

        dispatcher.utter_message(
            text="Pegando a temperatura para a fazenda de " + response['full_name'] + " ...")
        time.sleep(2)

        value = random.randint(20, 45)
        text = "A temperatura atual do solo é de {} graus.".format(value)

        dispatcher.utter_message(text=text)

        return []


class ActionUmidade(Action):

    def name(self) -> Text:
        return "action_umidade"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = verify_telegram(dispatcher, tracker)

        if not response:
            return []

        dispatcher.utter_message(
            text="Pegando a umidade para a fazenda de " + response['full_name'] + " ...")
        time.sleep(2)

        value = random.randint(0, 100)
        text = "A umidade atual do olo é de {}%.".format(value)

        dispatcher.utter_message(text=text)

        return []


class ActionPH(Action):

    def name(self) -> Text:
        return "action_ph"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = verify_telegram(dispatcher, tracker)

        if not response:
            return []

        dispatcher.utter_message(
            text="Pegando o ph para a fazenda de " + response['full_name'] + " ...")
        time.sleep(2)

        value = random.randint(1, 10)
        text = "O ph atual do solo é de {}.".format(value)

        dispatcher.utter_message(text=text)

        return []
