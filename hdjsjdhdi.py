# hrusudhdh.py
# Токен берётся из переменных окружения хостинга
# Всё остальное — внутри

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ===== ТОКЕН ИЗ ПЕРЕМЕННОЙ ОКРУЖЕНИЯ =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Добавь переменную окружения BOT_TOKEN на хостинге.")

# ===== ВСЁ ОСТАЛЬНОЕ =====
CHANNEL_LINK = "https://t.me/+otgte7DKQF40YmMy"
STARS_BUY_URL = "https://split.tg/?ref=UQD06L7Gv3pWk1J8DJ1wUeNsflj30ZmUyuZnb3zknSmVy5J-"

PLANS = {
    "full":   {"label": "50 ГБ", "stars": 600, "crypto": "https://t.me/send?start=IVfBnFlf6v5b"},
    "medium": {"label": "15 ГБ", "stars": 400, "crypto": "https://t.me/send?start=IVCR8jU3BohU"},
    "small":  {"label": "5 ГБ",  "stars": 350, "crypto": None},
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="⭐ Оплатить звёздами", callback_data="menu_stars"))
    kb.row(InlineKeyboardButton(text="🌐 Оплатить криптой",  callback_data="menu_crypto"))
    kb.row(InlineKeyboardButton(text="⭐ Где купить звёзды?", url=STARS_BUY_URL))
    await message.answer(
        "🌿 <b>TENDO</b>\n\n"
        "✅ Автовыдача сразу после оплаты\n"
        "🔒 Безопасная оплата через Telegram Stars\n\n"
        "Выберите способ оплаты:",
        parse_mode="HTML",
        reply_markup=kb.as_markup()
    )


@dp.callback_query(lambda c: c.data == "menu_stars")
async def menu_stars(call: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="50 ГБ — 600 ⭐", callback_data="stars_full"))
    kb.row(InlineKeyboardButton(text="15 ГБ — 400 ⭐", callback_data="stars_medium"))
    kb.row(InlineKeyboardButton(text="5 ГБ  — 350 ⭐", callback_data="stars_small"))
    kb.row(InlineKeyboardButton(text="⭐ Где купить звёзды?", url=STARS_BUY_URL))
    kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_start"))
    await call.message.edit_text(
        "⭐ <b>Оплата звёздами</b>\n\n"
        "После оплаты вы автоматически получите доступ.\n"
        "Выберите объём:",
        parse_mode="HTML",
        reply_markup=kb.as_markup()
    )


@dp.callback_query(lambda c: c.data == "menu_crypto")
async def menu_crypto(call: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    if PLANS["full"]["crypto"]:
        kb.row(InlineKeyboardButton(text="50 ГБ — Оплатить", url=PLANS["full"]["crypto"]))
    if PLANS["medium"]["crypto"]:
        kb.row(InlineKeyboardButton(text="15 ГБ — Оплатить", url=PLANS["medium"]["crypto"]))
    if PLANS["small"]["crypto"]:
        kb.row(InlineKeyboardButton(text="5 ГБ — Оплатить", url=PLANS["small"]["crypto"]))
    kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_start"))
    await call.message.edit_text(
        "🌐 <b>Оплата криптой</b>\n\n"
        "После оплаты свяжитесь с нами для выдачи доступа.\n"
        "Выберите объём:",
        parse_mode="HTML",
        reply_markup=kb.as_markup()
    )


@dp.callback_query(lambda c: c.data.startswith("stars_"))
async def send_invoice(call: types.CallbackQuery):
    key = call.data.replace("stars_", "")
    plan = PLANS.get(key)
    if not plan:
        return
    prices = [LabeledPrice(label="XTR", amount=plan["stars"])]
    await bot.send_invoice(
        chat_id=call.message.chat.id,
        title=f"TENDO — {plan['label']}",
        description=f"Доступ к контенту {plan['label']}. Автовыдача сразу после оплаты ✅",
        payload=f"tendo_{key}",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text=f"⭐ Заплатить {plan['stars']} звёзд", pay=True)
        ]])
    )
    await call.answer()


@dp.pre_checkout_query()
async def pre_checkout(query: types.PreCheckoutQuery):
    await query.answer(ok=True)


@dp.message(lambda m: m.successful_payment is not None)
async def successful_payment(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📁 Получить контент", url=CHANNEL_LINK)
    ]])
    await message.answer(
        "✅ <b>Оплата прошла успешно!</b>\n\n"
        "Нажми кнопку ниже, чтобы получить доступ к контенту 👇",
        parse_mode="HTML",
        reply_markup=kb
    )


@dp.callback_query(lambda c: c.data == "back_start")
async def back_start(call: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="⭐ Оплатить звёздами", callback_data="menu_stars"))
    kb.row(InlineKeyboardButton(text="🌐 Оплатить криптой",  callback_data="menu_crypto"))
    kb.row(InlineKeyboardButton(text="⭐ Где купить звёзды?", url=STARS_BUY_URL))
    await call.message.edit_text(
        "🌿 <b>TENDO</b>\n\n"
        "✅ Автовыдача сразу после оплаты\n"
        "🔒 Безопасная оплата через Telegram Stars\n\n"
        "Выберите способ оплаты:",
        parse_mode="HTML",
        reply_markup=kb.as_markup()
    )


async def main():
    print("✅ Бот TENDO запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())