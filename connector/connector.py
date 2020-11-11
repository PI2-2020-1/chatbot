import logging
from sanic.request import Request
from telegram import (
    Update,
)
from typing import Dict, Text, Any, Optional

from rasa.core.channels.telegram import TelegramInput

logger = logging.getLogger(__name__)


class CustomTelegramInput(TelegramInput):

    def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
        update = Update.de_json(request.json, self.get_output_channel())
        username = update.effective_message.chat.username
        chat_id = update.effective_message.chat.id
        return [username, chat_id]

   