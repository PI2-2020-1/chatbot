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
    "3": "o ph do solo",
    "4": "a umidade do solo",
    "5": "a umidade do ar",
    "1": "a pressão atmosférica",
    "2": "a temperatura do ar",
    "0": "a velocidade do vento",
    "6": "o índice pluviométrico",
}

def get_telegram_username(tracker):

    # Para desenvolvimento
    return "Geovana_RMS"

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

        response = verify_telegram(dispatcher, tracker)
        if not response:
            return [SlotSet('station_number', None)]

        dispatcher.utter_message(
            text="Pegando dados da fazenda de " + response['full_name'] + "...")

        r = requests.get(
            'http://localhost:8000/api/latest/' 
            + str(response['stations'][int(tracker.get_slot("station_number"))]['id'])).json()

        if not r:
            dispatcher.utter_message(text="Número de estação incorreto")
            return [SlotSet('station_number', None)]

        values = {}

        for obj in r:
            values[obj['parameter']] = str(obj['value'])
    
        text = "Os valores mais recentes da estação " + tracker.get_slot('station_number') + " são:\n"\
            "Vento: " + values[0] + "\n"\
            "Pressão do Ar: " + values[1] + "\n"\
            "Temperatura do Ar: " + values[2] + "\n"\
            "Ph do Solo: " + values[3] + "\n"\
            "Umidade do Solo: " + values[4] + "\n"\
            "Umidade do Ar: " + values[5] + "\n"\
            "Índice Pluviométrico: " + values[6] + "\n"\

        dispatcher.utter_message(text=text)

        return [SlotSet('station_number', None)]


class ActionParametroIdeais(Action):

    def name(self) -> Text:
        return "action_parametros_ideais"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = verify_telegram(dispatcher, tracker)
        if not response:
            return []

        data_type = tracker.get_slot("data_type")

        dispatcher.utter_message(
            text="Salvando valores ideias d" + DATA_STRING[data_type] + " para a fazenda de " + response['full_name'] + "...")
        time.sleep(2)

        text = "Valores ideais definidos com sucesso. Você será notificado quando o valor estiver fora desses limites."

        dispatcher.utter_message(text=text)

        return [SlotSet('data_type', None), SlotSet('max', None), SlotSet('min', None)]


