import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from .database import Database
from .keyboards import admin_menu, menu
from .inline_keyboard import get_categories_keyboard, get_products_keyboard, add_to_cart_btn, buyurtma, get_orders_keyboard
from .states import YetkazibberishState
from .states import AddCategoryState, AddProductState
from .i18n import t, LANG_KEYBOARD
import datetime

TOKEN = "7565458272:AAFuzHXmsa9uqBUxXckk4paQTClgQ33Xjfs"

bot = Bot(TOKEN)
dp = Dispatcher()
db = Database()

ADMIN_IDS = [726130790, ]

async def download_photo(file_id: str, bot: Bot, save_dir: str = "images") -> str:
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path.split("/")[-1]

    os.makedirs(save_dir, exist_ok=True)

    destination = os.path.join(save_dir, file_name)
    await bot.download_file(file_path, destination)
    return destination


@dp.message(F.text == "/start")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not db.get_user_locale(user_id):
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='set_lang_uz'),
                types.InlineKeyboardButton(text='🇬🇧 English', callback_data='set_lang_en'),
                types.InlineKeyboardButton(text='🇷🇺 Русский', callback_data='set_lang_ru'),
            ]
        ])
        await message.answer(t(db, user_id, "welcome_user"), reply_markup=kb)


    if user_id in ADMIN_IDS:
        await message.answer(t(db, user_id, "welcome_admin"), reply_markup=admin_menu(db, user_id))
    else:
        await message.answer(t(db, user_id, "hello_user"), reply_markup=menu(db, user_id))


@dp.callback_query(F.data.startswith('set_lang_'))
async def set_language(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = call.data.split('_')[-1]
    db.set_user_locale(user_id, lang)
    await call.message.answer(t(db, user_id, "language_changed"))
    await call.answer()


@dp.message(F.text == "➕ Add Category")
async def ask_category(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "ask_category_name"))
    await state.set_state(AddCategoryState.name)


@dp.message(AddCategoryState.name)
async def save_category(message: types.Message, state: FSMContext):
    category_name = message.text
    db.add_category(category_name)
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "category_added").format(name=category_name), reply_markup=admin_menu(db, user_id))
    await state.clear()


@dp.message(F.text == "📦 Add Product")
async def ask_product_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "ask_product_name"))
    await state.set_state(AddProductState.name)


@dp.message(AddProductState.name)
async def product_set_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "ask_price"))
    await state.set_state(AddProductState.price)


@dp.message(AddProductState.price)
async def product_set_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "ask_description"))
    await state.set_state(AddProductState.description)


@dp.message(AddProductState.description)
async def product_set_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "send_image"))
    await state.set_state(AddProductState.image)


@dp.message(AddProductState.image)
async def product_set_image(message: types.Message, state: FSMContext):
    if not message.photo:
        user_id = message.from_user.id
        return await message.answer(t(db, user_id, "send_image"))

    photo_id = message.photo[-1].file_id
    image_path = await download_photo(photo_id, bot)

    await state.update_data(image=image_path)
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "ask_category_id"))
    await state.set_state(AddProductState.category)


@dp.message(AddProductState.category)
async def product_finish(message: types.Message, state: FSMContext):
    category_id = int(message.text)

    data = await state.get_data()
    db.add_products(
        name=data["name"],
        price=float(data["price"]),
        description=data["description"],
        image=data["image"],
        category_id=category_id
    )
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "product_added"))
    await state.clear()


@dp.message(F.text == "Maxsulotlardan birini tanlang:")
async def ask_category2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(t(db, user_id, "choose_category"), reply_markup=get_categories_keyboard())

@dp.callback_query(F.data.startswith('category_'))
async def category_handler(call: types.CallbackQuery):
    category_id = call.data.split('_')[1]
    products_btn = get_products_keyboard(category_id)
    await call.message.answer(t(db, call.from_user.id, "choose_product"), reply_markup=products_btn)


@dp.callback_query(F.data.startswith('product_'))
async def product_handler(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[1])
    product = db.get_product(product_id)
    name = product[1]
    description = product[3] or ""
    price = product[2]
    # image_path = product[4]
    image = product[4]
    caption = t(db, call.from_user.id, "product_caption", name=name, description=description, price=price)
    await call.message.answer_photo(photo=image, caption=caption, reply_markup=add_to_cart_btn(product_id, db=db, user_id=call.from_user.id))


@dp.callback_query(F.data.startswith("plus_"))
async def plus_handler(call: types.CallbackQuery):
    product_id = call.data.split("_")[1]
    old_count = int(call.message.reply_markup.inline_keyboard[0][1].text)
    new_count = old_count + 1
    new_kb = add_to_cart_btn(product_id, new_count, db=db, user_id=call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=new_kb)
    await call.answer()


@dp.callback_query(F.data.startswith("minus_"))
async def minus_handler(call: types.CallbackQuery):
    product_id = call.data.split("_")[1]
    old_count = int(call.message.reply_markup.inline_keyboard[0][1].text)
    if old_count == 1:
        await call.answer()
        return
    new_count = old_count - 1
    new_kb = add_to_cart_btn(product_id, new_count, db=db, user_id=call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=new_kb)
    await call.answer()


@dp.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart_handler(call: types.CallbackQuery):
    product_id = int(call.data.split("_")[3])
    count = int(call.message.reply_markup.inline_keyboard[0][1].text)
    product = db.get_product(product_id)
    total_price = product[2] * count
    user_id = call.from_user.id
    db.add_cart_item(user_id, product_id, count, total_price)
    await call.message.answer(t(db, user_id, "added_to_cart", count=count, total=total_price))


@dp.message(F.text == 'Savatcha')
async def savatcha_handler(message: types.Message):
    user_id = message.from_user.id
    cart_items = db.get_cart_items(user_id)
    if not cart_items:
        await message.answer(t(db, user_id, "cart_empty"))
        return
    data = ""
    total = 0
    for item in cart_items:
        product = db.get_product(item[3])
        name = product[1]
        count = item[2]
        total_price = item[2]
        data += f"{name} - {count} dona. {total_price} so'm\n"
        total += total_price

    await message.answer(t(db, user_id, "cart_summary", data=data, total=total), reply_markup=buyurtma)


@dp.callback_query(F.data == 'buyutrmaberish')
async def buyurtma_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(t(db, call.from_user.id, "order_start"))
    await call.message.answer(t(db, call.from_user.id, "enter_phone"))
    await state.set_state(YetkazibberishState.phone)


@dp.message(YetkazibberishState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(t(db, message.from_user.id, "enter_location"))
    await state.set_state(YetkazibberishState.lokation)


@dp.message(YetkazibberishState.lokation)
async def get_location(message: types.Message, state: FSMContext):
    await state.update_data(lokation=message.text)
    await message.answer(t(db, message.from_user.id, "ask_payment"))
    await state.set_state(YetkazibberishState.tolov_turi)


@dp.message(YetkazibberishState.tolov_turi)
async def get_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    phone = data['phone']
    lokation = data['lokation']
    payment = message.text
    cart_items = db.get_cart_items(user_id)
    products_text = ""
    total = 0
    for item in cart_items:
        product = db.get_product(item[3])
        name = product[1]
        count = item[1]
        total_price = item[2]
        products_text += f"{name} - {count} dona. {total_price} so'm\n"
        total += total_price

    products_text += f"Jami: {total} so'm"
    sana = str(datetime.datetime.now())
    db.add_order(user_id, products_text, phone, lokation, payment, sana)
    db.clear_cart_items(user_id)

    await message.answer(
        t(db, user_id, "order_confirmed", phone=phone, lokation=lokation, payment=payment, products=products_text)
    )
    await state.clear()

@dp.message(F.text == "Byurtmalar")
async def get_orders_handler(message: types.Message):
    user_id = message.from_user.id
    orders = db.get_orders(user_id)

    if not orders:
        await message.answer(t(db, user_id, "no_orders"))
    else:
        orders_btn = get_orders_keyboard(user_id)
        await message.answer(t(db, user_id, "choose_order"), reply_markup=orders_btn)

@dp.callback_query(F.data.startswith('order_'))
async def get_orders_handler(call: types.CallbackQuery):
    id = int(call.data.split("_")[1])
    order = db.get_orders_by_id(id)

    text = t(db, call.from_user.id, "order_details_title")
    products = order[2]
    phone = order[3]
    location = order[4]
    payment = order[5]
    sana = order[6]

    text += (
            f"🕒 Sana: {sana}\n"
            f"{products}\n"
            f"📞 Tel: {phone}\n"
            f"📍 Manzil: {location}\n"
            f"💳 To‘lov: {payment}\n"
            f"--------------------------------------\n"
        )

    await call.message.answer(text)


@dp.message(F.text == "Tilni o'zgartirish")
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if db.get_user_locale(user_id):
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='set_lang_uz'),
                types.InlineKeyboardButton(text='🇬🇧 English', callback_data='set_lang_en'),
                types.InlineKeyboardButton(text='🇷🇺 Русский', callback_data='set_lang_ru'),
            ]
        ])
        await message.answer(t(db, user_id, "welcome_user"), reply_markup=kb)

    if user_id in ADMIN_IDS:
        await message.answer(t(db, user_id, "welcome_admin"), reply_markup=admin_menu(db, user_id))
    else:
        await message.answer(t(db, user_id, "hello_user"), reply_markup=menu(db, user_id))


async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())