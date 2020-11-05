import requests
import logging

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import random
import time

logger = logging.getLogger(__name__)


DATA_STRING = {
    "PH": "o ph",
    "US": "a umidade do solo",
    "UA": "a umidade do ar",
    "PA": "a pressão atmosférica",
    "T": "a temperatura",
    "V": "a velocidade do vento",
    "IP": "o índice pluviométrico",
}


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


class ActionDadosAtuais(Action):

    def name(self) -> Text:
        return "action_dados_atuais"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Para testes em desenvolvimento
        value = random.randint(20, 45)
        response = {'full_name': 'Geovana'}

        #response = verify_telegram(dispatcher, tracker)
        if not response:
            return []

        data_type = tracker.get_slot("data_type")

        dispatcher.utter_message(
            text="Pegando " + DATA_STRING[data_type] + " para a fazenda de " + response['full_name'] + "...")
        time.sleep(2)

        text = "O valor d" + DATA_STRING[data_type] + " temperatura atual do solo é de" + str(value) + "."

        dispatcher.utter_message(text=text)

        return [SlotSet('data_type', None)]


class ActionParametroIdeais(Action):

    def name(self) -> Text:
        return "action_parametros_ideais"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Para testes em desenvolvimento
        value = random.randint(20, 45)
        response = {'full_name': 'Geovana'}

        #response = verify_telegram(dispatcher, tracker)
        if not response:
            return []

        data_type = tracker.get_slot("data_type")

        dispatcher.utter_message(
            text="Salvando valores ideias d" + DATA_STRING[data_type] + " para a fazenda de " + response['full_name'] + "...")
        time.sleep(2)

        text = "Valores ideais definidos com sucesso. Você será notificado quando o valor estiver fora desses limites."

        dispatcher.utter_message(text=text)

        return [SlotSet('data_type', None)]


