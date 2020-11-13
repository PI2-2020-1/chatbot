import requests
import logging
import json

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


def get_telegram_metadata(tracker):

    # Para desenvolvimento
    # return ["Geovana_RMS", 12344353]

    events = tracker.current_state()['events']
    user_events = []

    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']


def verify_telegram(dispatcher, tracker):

    metadata = get_telegram_metadata(tracker)

    r = requests.get(
        'http://localhost:8000/api/telegram/verification/' + str(metadata[0]) + '/' + str(metadata[1]))

    if r.status_code == 404:
        dispatcher.utter_message(
            text="Usuário não encontrado no sistema A2P2.")
        return None

    return r.json()


def get_station_pk(station_number, plantations_json):
    plantation = plantations_json[0]

    for s in plantation["stations"]:
        if s['number'] == station_number:
            return s['id']


class ActionDadosAtuais(Action):

    def name(self) -> Text:
        return "action_dados_atuais"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = verify_telegram(dispatcher, tracker)
        if not response:
            return [SlotSet('station_number', None)]

        station_pk = get_station_pk(int(tracker.get_slot("station_number")), response['plantations'])

        dispatcher.utter_message(
            text="Pegando dados da fazenda de " + response['full_name'] + "...")

        resp = requests.get('http://localhost:8000/api/latest/' + str(station_pk))

        if not resp:
            dispatcher.utter_message(text="Número de estação incorreto")
            return [SlotSet('station_number', None)]

        values = {}

        r = json.loads(resp.text)

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
            return [SlotSet('data_type', None), SlotSet('max', None), SlotSet('min', None)]

        station_pk = get_station_pk(1, response['plantations'])

        data_type = tracker.get_slot("data_type")
        min_value = tracker.get_slot("min")
        max_value = tracker.get_slot("max")

        dispatcher.utter_message(
            text="Salvando valores ideias d" + DATA_STRING[data_type] + " para a fazenda de " + response['full_name'] + "...")

        data = {"parameter_type": data_type,"min_value": min_value, "max_value": max_value}
        print(data)
        r = requests.post(
            url='http://localhost:8000/api/parameter/' + str(station_pk),
            data=json.dumps(data)
        )

        if not r:
            dispatcher.utter_message(text="Erro")
            return [SlotSet('data_type', None), SlotSet('max', None), SlotSet('min', None)]


        text = "Valores ideais definidos com sucesso. Você será notificado quando o valor estiver fora desses limites."

        dispatcher.utter_message(text=text)

        return [SlotSet('data_type', None), SlotSet('max', None), SlotSet('min', None)]
