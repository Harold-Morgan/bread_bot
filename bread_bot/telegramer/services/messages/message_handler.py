# FIXME: Данный модуль переписан на message_receiver.py, но пока что используется. Как перестанет - выпилить модуль.
import asyncio
import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bread_bot.main.settings import MESSAGE_LEN_LIMIT
from bread_bot.telegramer.clients.telegram_client import TelegramClient
from bread_bot.telegramer.exceptions.base import NextStepException
from bread_bot.telegramer.schemas.bread_bot_answers import BaseAnswerSchema, TextAnswerSchema
from bread_bot.telegramer.schemas.telegram_messages import StandardBodySchema
from bread_bot.telegramer.services.member_service import MemberService
from bread_bot.telegramer.services.messages.message_service import MessageService
from bread_bot.telegramer.services.processors import (
    AdminMessageProcessor,
    EditedMessageProcessor,
    MemberCommandMessageProcessor,
    PhrasesMessageProcessor,
    UtilsCommandMessageProcessor,
    VoiceMessageProcessor,

)
from bread_bot.utils.helpers import chunks

logger = logging.getLogger(__name__)


async def get_message_service(request_body: StandardBodySchema) -> Optional[MessageService]:
    try:
        message_service = MessageService(request_body=request_body)
    except NextStepException:
        return
    except Exception as e:
        logger.error("Error while handle message_service process", exc_info=e)
        return
    else:
        return message_service


async def send_messages_to_chat(message: BaseAnswerSchema):
    telegram_client = TelegramClient()
    message_parts = []
    # Если сообщение очень длинное для текстового формата - бьем на чанки и выполняем асинхронную отправку
    if isinstance(message, TextAnswerSchema) and message.text and len(message.text) > MESSAGE_LEN_LIMIT:
        for chunk in chunks(message.text, MESSAGE_LEN_LIMIT):
            message_parts.append(
                TextAnswerSchema(
                    text=chunk,
                    chat_id=message.chat_id,
                    reply_to_message_id=message.reply_to_message_id,
                )
            )
        if len(message_parts) > 0:
            await asyncio.gather(*[
                telegram_client.send_message_by_schema(message_part) for message_part in message_parts
            ])
        return
    else:
        await telegram_client.send_message_by_schema(message)


async def process_telegram_message(db: AsyncSession, request_body: StandardBodySchema):
    message_service = await get_message_service(request_body=request_body)
    try:
        member_service = MemberService(db=db, message=message_service.message)
    except Exception as e:
        logger.error("Error while handle member_service process", exc_info=e)
        return
    await member_service.process()

    if message_service is None:
        return
    # Выполнение цепочкой до первого успешного.
    for Processor in [
        EditedMessageProcessor,
        VoiceMessageProcessor,
        AdminMessageProcessor,
        MemberCommandMessageProcessor,
        UtilsCommandMessageProcessor,
        PhrasesMessageProcessor,
    ]:
        message = await Processor(message_service=message_service, member_service=member_service).process()
        if message is not None:
            break

    if message is None:
        logger.error("Result answer schema is None: %s", message_service.request_body.dict())
        return

    try:
        await send_messages_to_chat(message)
    except Exception as e:
        logger.error("Error while sending message", exc_info=e)
