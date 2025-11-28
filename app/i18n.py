"""
Simple i18n helper for the shop bot.
Translations stored in TRANSLATIONS dict. Use set_locale/get_locale in Database (db) to persist per-user locale.
Usage: from shop_bot.i18n import t, LANG_KEYBOARD
       await message.answer(t(db, user_id, "welcome"))
"""
from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "uz": {
        "welcome_admin": "Salom Admin",
        "welcome_user": "Assalomu alaykum! Tilni tanlang 👇",
        "hello_user": "Aslomu alekum bratimmm...",
        "ask_category_name": "Kategoriya nomini kiriting:",
        "category_added": "Kategoriya qo‘shildi: {name}",
        "ask_product_name": "Product nomini kiriting:",
        "ask_price": "Narxini kiriting:",
        "ask_description": "Description kiriting:",
        "send_image": "Rasm yuboring:",
        "ask_category_id": "Kategoriya ID kiriting (masalan: 1):",
        "product_added": "Maxshulot savatchaga qo'shildi",
        "choose_category": "Kategoriya birini tanlen:",
        "choose_product": "Maxsulotlardan birini tanlang:",
        "product_caption": "Nom: {name}\n\nTavsif: {description}\n\nNarx: {price} so'm",
        "added_to_cart": "Mahsulot savatchaga qo'shildi: {count} ta, jami narxi: {total} so'm",
        "cart_empty": "Sizning savatchangiz bo'sh.",
        "cart_summary": "{data}\n\nJami: {total} so'm",
        "order_start": "Buyurtma berish uchun sorovlarga javob bering",
        "enter_phone": "Nomeringizni kiriting:",
        "enter_location": "Turar joyingizni aniq kiriting:",
        "ask_payment": "Naqd yoki plastik to‘lovmi?",
        "order_confirmed": "Buyurtmangiz qabul qilindi!\n\n📞 Telefon: {phone}\n📍 Manzil: {lokation}\n💳 To‘lov turi: {payment}\n🛒 Buyurtma:\n{products}",
        "no_orders": "Sizda hali buyurtmalar yo‘q ❗️",
        "choose_order": "Buyurtmalardan birini tanlang: ",
        "order_details_title": "📦 Sizning buyurtmalaringiz:\n\n",
        "language_changed": "Til o'zgartirildi!"
    },
    "en": {
        "welcome_admin": "Hello Admin",
        "welcome_user": "Hello! Select your language 👇",
        "hello_user": "Hello there...",
        "ask_category_name": "Enter category name:",
        "category_added": "Category added: {name}",
        "ask_product_name": "Enter product name:",
        "ask_price": "Enter price:",
        "ask_description": "Enter description:",
        "send_image": "Send an image:",
        "ask_category_id": "Enter category ID (e.g. 1):",
        "product_added": "Product added to cart",
        "choose_category": "Choose a category:",
        "choose_product": "Choose a product:",
        "product_caption": "Name: {name}\n\nDescription: {description}\n\nPrice: {price} UZS",
        "added_to_cart": "Product added to cart: {count} pcs, total price: {total} UZS",
        "cart_empty": "Your cart is empty.",
        "cart_summary": "{data}\n\nTotal: {total} UZS",
        "order_start": "Please answer questions to place an order",
        "enter_phone": "Enter your phone number:",
        "enter_location": "Enter your exact address:",
        "ask_payment": "Cash or card payment?",
        "order_confirmed": "Your order has been received!\n\n📞 Phone: {phone}\n📍 Address: {lokation}\n💳 Payment: {payment}\n🛒 Order:\n{products}",
        "no_orders": "You have no orders yet ❗️",
        "choose_order": "Choose one of the orders: ",
        "order_details_title": "📦 Your orders:\n\n",
        "language_changed": "Language changed!"
    },
    "ru": {
        "welcome_admin": "Привет, админ",
        "welcome_user": "Здравствуйте! Выберите язык 👇",
        "hello_user": "Привет...",
        "ask_category_name": "Введите название категории:",
        "category_added": "Категория добавлена: {name}",
        "ask_product_name": "Введите название продукта:",
        "ask_price": "Введите цену:",
        "ask_description": "Введите описание:",
        "send_image": "Отправьте изображение:",
        "ask_category_id": "Введите ID категории (например: 1):",
        "product_added": "Продукт добавлен в корзину",
        "choose_category": "Выберите категорию:",
        "choose_product": "Выберите продукт:",
        "product_caption": "Название: {name}\n\nОписание: {description}\n\nЦена: {price} сум",
        "added_to_cart": "Товар добавлен в корзину: {count} шт., общая цена: {total} сум",
        "cart_empty": "Ваша корзина пуста.",
        "cart_summary": "{data}\n\nИтого: {total} сум",
        "order_start": "Ответьте на вопросы для оформления заказа",
        "enter_phone": "Введите ваш номер:",
        "enter_location": "Введите ваш адрес:",
        "ask_payment": "Наличные или карта?",
        "order_confirmed": "Ваш заказ принят!\n\n📞 Тел: {phone}\n📍 Адрес: {lokation}\n💳 Оплата: {payment}\n🛒 Заказ:\n{products}",
        "no_orders": "У вас пока нет заказов ❗️",
        "choose_order": "Выберите один из заказов: ",
        "order_details_title": "📦 Ваши заказы:\n\n",
        "language_changed": "Язык изменён!"
    }
}

LANG_KEYBOARD = {
    "inline": [
        [{"text":"🇺🇿 O'zbekcha", "callback":"set_lang_uz"}, {"text":"🇬🇧 English", "callback":"set_lang_en"}, {"text":"🇷🇺 Русский", "callback":"set_lang_ru"}]
    ]
}

def t(db, user_id, key, **kwargs):
    # get user's locale from DB; default to uz
    try:
        locale = db.get_user_locale(user_id) or "uz"
    except Exception:
        locale = "uz"
    text = TRANSLATIONS.get(locale, TRANSLATIONS["uz"]).get(key, key)
    return text.format(**kwargs)