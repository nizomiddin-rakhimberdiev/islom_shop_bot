from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .database import Database
from .i18n import t

db = Database()

def get_categories_keyboard():
    categories = db.get_categories()
    # print(categories)

    if categories:
        builder = InlineKeyboardBuilder()
        for category in categories:
            builder.button(
                text=category[1],
                callback_data=f"category_{category[0]}"
            )
        builder.adjust(3)
        return builder.as_markup()

def get_products_keyboard(category_id):
    products = db.get_products_by_category(category_id)
    # print(products)

    if products:
        builder = InlineKeyboardBuilder()
        for product in products:
            builder.button(
                text=product[1],
                callback_data=f"product_{product[0]}"
            )
        builder.adjust(2)  # Har bir qatorda 2 ta tugma
        return builder.as_markup()

def add_to_cart_btn(product_id, count=1, db=None, user_id=None):
    # center count button label uses count
    add_to_cart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='-', callback_data=f"minus_{product_id}"),
                InlineKeyboardButton(text=str(count), callback_data=f"count_{product_id}"),
                InlineKeyboardButton(text='+', callback_data=f"plus_{product_id}"),
            ],
            [
                InlineKeyboardButton(text=(t(db, user_id, "product_added") if db and user_id else "Savatchaga qo\\'shish"), callback_data=f"add_to_cart_{product_id}")
            ]
        ]
    )
    return add_to_cart

buyurtma= InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="buyutrmaberish", callback_data='buyutrmaberish')]

]
)
til_ozgartirish = InlineKeyboardMarkup(
    inline_keyboard=[

            [InlineKeyboardButton(text="rus", callback_data='rus')],
            [InlineKeyboardButton(text="en", callback_data='en')],
            [InlineKeyboardButton(text="uz", callback_data='uz')],

]
)

def get_orders_keyboard(user_id):
    orders = db.get_orders(user_id)
    # print(orders)

    if orders:
        builder = InlineKeyboardBuilder()
        for order in orders:
            builder.button(
                text=order[6],
                callback_data=f"order_{order[0]}"
            )
        builder.adjust(2)
        return builder.as_markup()