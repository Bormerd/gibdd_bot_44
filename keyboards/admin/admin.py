"""Клавиатуры для Администратора"""

from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from database.models import User, Admin, Role, UserRole, Patrol
from filters.inspector import IsInspector


ADMIN_KEYBOARD = [
    [
        KeyboardButton(text="Добавить инспектора"),
        KeyboardButton(text="Показать инспекторов"),
    ],
    [
        KeyboardButton(text="Добавить администратора"),
        KeyboardButton(text="Показать администраторов"),
    ],
]


def get_keyboard_by_user(user: User):
    """Кнопки для клавиатуры администратора"""

    admin: Admin = Admin.get_or_none(user=user)
    keyboard = ADMIN_KEYBOARD + [
        [
            (
                KeyboardButton(text="Не получать сообщения очевидцев")
                if admin and admin.is_notify
                else KeyboardButton(text="Получать соощения очевидцев")
            )
        ]
    ]
    return keyboard


def get_kb_by_user(user: User):
    """Клавиатура администратора"""
    keyboard = get_keyboard_by_user(user)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def get_kb_by_show_employees(role: Role, page: int, limit: int = 10):
    """Возвращает клавиатуру пользователей"""

    role_object = role if isinstance(role, Role) else Role.get_by_id(role)

    inspector_in_patrol = {
        p.inspector_id
        for p in Patrol.select(Patrol.inspector)
        .where(Patrol.end.is_null())
    } if IsInspector.role == role_object else set()

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=(f"{'🚨 ' if ur.user.id in inspector_in_patrol else ''}"
                      f"{ur.user.full_name}"
                      ),
                callback_data=f"user_info_{ur.user.id}",
            )
        ]
        for ur in UserRole.select()
        .where(UserRole.role == role_object)
        .offset((page - 1) * limit)
        .limit(limit)
    ]
    last_row = []
    if page > 1:
        last_row.append(
            InlineKeyboardButton(
                text="Назад",
                callback_data=f"users_page_{role}_{page-1}",
            )
        )

    last_row.append(
        InlineKeyboardButton(
            text=f"Страница: {page}",
            callback_data="alert",
        )
    )

    if len(inline_keyboard) == limit:
        last_row.append(
            InlineKeyboardButton(
                text="Вперед",
                callback_data=f"users_page_{role}_{page+1}",
            )
        )

    if last_row:
        inline_keyboard.append(last_row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
