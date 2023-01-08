import random
import re

from pymystem3 import Mystem
from sqlalchemy import and_

from bread_bot.common.exceptions.base import NextStepException
from bread_bot.common.models import (
    AnswerEntity,
)
from bread_bot.common.schemas.bread_bot_answers import (
    BaseAnswerSchema,
    TextAnswerSchema,
    PhotoAnswerSchema,
    StickerAnswerSchema,
    VoiceAnswerSchema,
    GifAnswerSchema,
    VideoAnswerSchema,
    VideoNoteAnswerSchema,
)
from bread_bot.common.services.handlers.handler import AbstractHandler
from bread_bot.common.utils.functions import composite_mask
from bread_bot.common.utils.structs import (
    AnswerEntityReactionTypesEnum,
    AnswerEntityContentTypesEnum,
)


class AnswerHandler(AbstractHandler):
    @property
    def condition(self) -> bool:
        return self.message_service and self.message_service.message and self.message_service.message.text

    @staticmethod
    def get_lemmas(keys: list) -> dict[str, str]:
        lemma_system = Mystem()
        keys_to_lemmas = {}
        for key in keys:
            if re.findall(r"[А-я]", key):
                lemma = "".join(lemma_system.lemmatize(key)).strip()
                keys_to_lemmas[lemma] = key
        return keys_to_lemmas

    @staticmethod
    def reformat_groups_from_lemmas(groups: list[str], keys_to_lemmas: dict[str, str]) -> list[str]:
        result = []
        for group_item in groups:
            if group_item in keys_to_lemmas:
                result.append(keys_to_lemmas[group_item])
            else:
                result.append(group_item)
        return result

    def find_keys(self, keys: list, reaction_type: AnswerEntityReactionTypesEnum, message_text: str | None = None):
        """Поиск ключей из БД среди сообщения"""
        keys_to_lemmas = self.get_lemmas(keys=keys)
        if message_text is not None:
            message_text = message_text.lower()
        else:
            message_text = self.message_service.message.text.lower()

        match reaction_type:
            case AnswerEntityReactionTypesEnum.SUBSTRING:
                regex = f"({composite_mask(keys + list(keys_to_lemmas.keys()), split=True)})"
                if keys_to_lemmas:
                    message_text = "".join(Mystem().lemmatize(message_text)).strip()
            case AnswerEntityReactionTypesEnum.TRIGGER:
                regex = f"^({composite_mask(keys)})$"
            case _:
                raise NextStepException("Неподходящий тип данных")

        groups = re.findall(regex, message_text, re.IGNORECASE)
        if len(groups) == 0:
            raise NextStepException("Подходящих ключей не найдено")
        if keys_to_lemmas:
            return self.reformat_groups_from_lemmas(groups=groups, keys_to_lemmas=keys_to_lemmas)
        else:
            return groups

    def check_process_ability(self, check_edited_message: bool = True):
        if not self.condition:
            raise NextStepException("Не подходит условие для обработки")
        if check_edited_message and self.message_service.has_edited_message:
            raise NextStepException("Пропуск отредактированного сообщения")
        if not self.default_answer_pack:
            raise NextStepException("Отсутствуют пакеты с ответами")

    async def process_message(
        self,
        reaction_type: AnswerEntityReactionTypesEnum,
        message_text: str | None = None,
    ) -> BaseAnswerSchema:
        answer_keys = await AnswerEntity.get_keys(
            db=self.db, pack_id=self.default_answer_pack.id, reaction_type=reaction_type
        )
        keys = self.find_keys(keys=answer_keys, reaction_type=reaction_type, message_text=message_text)
        results = None
        for key in keys:
            results = await AnswerEntity.async_filter(
                db=self.db,
                where=and_(
                    AnswerEntity.pack_id == self.default_answer_pack.id,
                    AnswerEntity.reaction_type == reaction_type,
                    AnswerEntity.key == key,
                ),
            )
            if results:
                break

        if not results:
            raise NextStepException("Значения не найдено")

        result: AnswerEntity = random.choice(results)
        base_message_params = dict(
            reply_to_message_id=self.message_service.message.message_id,
            chat_id=self.message_service.message.chat.id,
        )
        match result.content_type:
            case AnswerEntityContentTypesEnum.TEXT:
                return TextAnswerSchema(**base_message_params, text=result.value)
            case AnswerEntityContentTypesEnum.PICTURE:
                return PhotoAnswerSchema(**base_message_params, photo=result.value, caption=result.description)
            case AnswerEntityContentTypesEnum.STICKER:
                return StickerAnswerSchema(**base_message_params, sticker=result.value)
            case AnswerEntityContentTypesEnum.VOICE:
                return VoiceAnswerSchema(**base_message_params, voice=result.value)
            case AnswerEntityContentTypesEnum.ANIMATION:
                return GifAnswerSchema(**base_message_params, animation=result.value)
            case AnswerEntityContentTypesEnum.VIDEO:
                return VideoAnswerSchema(**base_message_params, video=result.value)
            case AnswerEntityContentTypesEnum.VIDEO_NOTE:
                return VideoNoteAnswerSchema(**base_message_params, video_note=result.value)
            case _:
                raise NextStepException("Полученный тип контента не подлежит ответу")

    async def process(self) -> BaseAnswerSchema:
        raise NextStepException("Базовый класс")


class SubstringAnswerHandler(AnswerHandler):
    async def process(self) -> BaseAnswerSchema:
        self.check_process_ability()
        if random.random() > self.default_answer_pack.answer_chance / 100:
            raise NextStepException("Пропуск ответа по проценту срабатывания")

        return await super().process_message(reaction_type=AnswerEntityReactionTypesEnum.SUBSTRING)


class TriggerAnswerHandler(AnswerHandler):
    async def process(self) -> BaseAnswerSchema:
        self.check_process_ability()
        if random.random() > self.default_answer_pack.answer_chance / 100:
            raise NextStepException("Пропуск ответа по проценту срабатывания")

        return await super().process_message(reaction_type=AnswerEntityReactionTypesEnum.TRIGGER)
