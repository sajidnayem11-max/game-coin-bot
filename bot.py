import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "9279326916:AAEYUtRjvy8zOyvObk4eJ72YzS6ZL5JDh3c" # Apnar telegram bot token

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # Multi-product main menu
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪙 Flight Charbe Coins", callback_data="buy_flight")],
        [InlineKeyboardButton(text="💎 Free Fire Diamonds", callback_data="buy_ff")],
        [InlineKeyboardButton(text="💎 Mobile Legends Diamonds", callback_data="buy_ml")]
    ])
    
    await message.reply(
        "👋 Assalamu Alaikum!\n\n"
        "🎮 Amader Game Coin & Diamond Store-e apnake shagotom. 🪙💎\n\n"
        "👇 Apni kon game-er item kinte chan, niche theke select korun:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def process_product_selection(callback: types.CallbackQuery):
    product_type = callback.data
    
    if product_type == "buy_flight":
        text = "🪙 **Flight Charbe Coins** selec korechen.\n\nKoy ti coin kinte chan tar songkha likhe pathan:"
    elif product_type == "buy_ff":
        text = "💎 **Free Fire Diamonds** select korechen.\n\nApanar Free Fire Player ID (UID) ebong package poriman din:"
    elif product_type == "buy_ml":
        text = "💎 **Mobile Legends Diamonds** select korechen.\n\nApnar ML User ID ebong Zone ID pathan:"
        
    await callback.message.answer(text)
    await callback.answer()

async def main():
    print("Bot multiple product menu sohokare cholche...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher

# আপনার বটের টোকেন এবং ডিসপ্যাচার ইনিশিয়ালাইজেশন
TOKEN = "9279326916:AAEYUtRjvy8zOyvObk4eJ72YzS6ZL5JDh3c"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ১. রেন্ডার পোর্ট ধরে রাখার জন্য মিনি ওয়েব সার্ভার
async def handle(request):
    return web.Response(text="Bot is running 24/7!")

app = web.Application()
app.router.add_get("/", handle)

async def start_web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))  # Render স্বয়ংক্রিয়ভাবে PORT ভেরিয়েবল দিয়ে দেয়
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ২. মূল মেইন ফাংশন যেখানে asyncio.gather ব্যবহার করা হয়েছে
async def main():
    # একসাথে ওয়েব সার্ভার এবং বটের পোলিং রান করবে
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())