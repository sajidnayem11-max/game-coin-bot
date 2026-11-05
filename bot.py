import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cryptomus import Client  # ক্রিপ্টোমাস লাইব্রেরি

# আপনার বটের টোকেন এবং ক্রিপ্টোমাস ক্রডেনশিয়াল এখানে বসাবেন
TOKEN = "9279326916:AAFUj10LZj054kY_sefZVKNOG05qETxXp3c"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ক্রিপ্টোমাস ক্লায়েন্ট ইনিশিয়ালাইজেশন
# cryptomus = Client.payment(api_key=PAYMENT_API_KEY, uuid=MERCHANT_UUID)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🪙 Flight Charbe Coins", callback_data="buy_flight")],
            [InlineKeyboardButton(text="💎 Free Fire Diamonds", callback_data="buy_ff")],
            [InlineKeyboardButton(text="💎 Mobile Legends Diamonds", callback_data="buy_ml")]
        ]
    )
    
    await message.answer(
        "Assalamu Alaikum!\n\n"
        "Amader Game Coin & Diamond Store-e apnake shagotom. 🪙💎\n\n"
        "Apni kon game-er item kinte chan, niche theke select korun:",
        reply_markup=keyboard
    )

@dp.callback_query(F.data.in_(["buy_flight", "buy_ff", "buy_ml"]))
async def process_game_selection(callback: types.CallbackQuery):
    game_names = {
        "buy_flight": "Flight Charbe Coins",
        "buy_ff": "Free Fire Diamonds",
        "buy_ml": "Mobile Legends Diamonds"
    }
    
    selected_game = game_names.get(callback.data)
    
    await callback.message.answer(
        f"Apni **{selected_game}** select korechen. 🎮\n\n"
        "Doya kore apni koyti coin ba diamond kinte chan, tar poriman (number) ekhane likhe pathan (jemon: 100 ba 500):",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.message(Command("support"))
async def support_cmd(message: types.Message):
    support_text = (
        "🛠 **Customer Support & Assistance**\n\n"
        "Kono shomossha ba payment related issue- er jonno doya kore amader official support team er sathe jogajog korun:\n\n"
        "👤 **Support Admin:** @ShamiulAzim1701\n\n"
        "Amra apnake sahajjo korar jonno 24/7 prostut royechi!"
    )
    await message.answer(support_text, parse_mode="Markdown")

# ইউজার যখন কয়েনের পরিমাণ লিখে পাঠাবে (মূল পেমেন্ট পেজ এবং বাটন)
@dp.message(F.text.regexp(r'^\d+$'))
async def process_coin_amount(message: types.Message):
    amount = int(message.text)
    
    price_per_coin = 0.01
    total_price = amount * price_per_coin
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Pay Now (${total_price:.2f})", callback_data="make_payment")]
        ]
    )
    
    await message.answer(
        f"✅ Apni **{amount}** ti coin select korechen.\n"
        f"💵 Proti coin-er dam: **$0.01**\n"
        f"💰 Mot mullo (Total Price): **${total_price:.2f} USD**\n\n"
        "Nicher button-e click kore payment complete korun:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ১. রেন্ডার পোর্ট ধরে রাখার জন্য মিনি ওয়েব সার্ভার
async def handle(request):
    return web.Response(text="Bot is running 24/7!")

app = web.Application()
app.router.add_get("/", handle)

async def start_web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ২. মূল মেইন ফাংশন
async def main():
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())