"""Пересылка сообщения от пользователя инспекторам"""

from aiogram import Router, F
from aiogram.types import Message, ContentType
from filters.user import IsUser
from handlers.eyewitness.logic import (
    save_user_message,
    send_message_to_employees,
)
from keyboards.eyewitness import KB as eyewitness_kb


router = Router()


@router.message(F.text, ~F.text.startswith("/"), IsUser())
async def get_message_from_user(message: Message) -> None:
    """Обработчик сообщения от пользователя"""
    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.ANIMATION, IsUser())
async def get_animation_from_user(message: Message) -> None:
    """Обработчик видео от пользователя"""
    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.VIDEO, IsUser())
async def get_video_from_user(message: Message) -> None:
    """Обработчик видео от пользователя"""
    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.PHOTO, IsUser())
async def get_photo_from_user(message: Message) -> None:
    """Обработчик фотографий от пользователя"""
    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


@router.message(F.content_type == ContentType.LOCATION, IsUser())
async def get_location_from_user(message: Message) -> None:
    """Обработчик локации от пользователя"""
    await answer(message=message)
    await send_message_to_employees(
        bot=message.bot, user_message=save_user_message(message=message)
    )


async def answer(message: Message):
    """Стандартный ответ для очевидца"""

    await message.answer(
        text="Спасибо за обращение. "
        "Мы его уже передали инспекторам. "
        "Вы можете отправить фотографии или видео с места происшествия. "
        "Если хотите отправить геолокацию, нажмите кнопку ниже: "
        "<b>Отправить геолокацию</b>",
        reply_markup=eyewitness_kb,
        parse_mode="HTML",
    )
