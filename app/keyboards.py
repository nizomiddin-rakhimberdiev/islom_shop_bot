from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .i18n import t

def admin_menu(db, user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(db, user_id, "ask_category_name"))],
            [KeyboardButton(text="📦 " + t(db, user_id, "ask_product_name"))]
        ],
        resize_keyboard=True
    )

def menu(db, user_id):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(db, user_id, "choose_product")),
                KeyboardButton(text="Byurtmalar"),
            ],
            [
                KeyboardButton(text="Savatcha"),
                KeyboardButton(text="Tilni o'zgartirish")
            ]
        ],
        resize_keyboard=True
    )


