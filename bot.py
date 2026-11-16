import asyncio
import os
import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার বটের টোকেন
TOKEN = "9279326916:AAFUj10LZj054kY_sefZVKNOG05qETxXp3c"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ChangeNOW API এবং আপনার রিসিভিং ওয়ালেট কনফিগারেশন
CHANGENOW_API_KEY = "97306fd8668484c20deb225c773009f63aaf9d464e2b0891d44a279e83dc84a4"
RECEIVING_ADDRESS = "0x8f6358d1900c585b3b7ec36c5a99b5efd3a9a97d"  # Binance USDT BEP-20

# ইউজারের সাময়িক ডেটা সেভ রাখার জন্য ডিকশনারি
user_temp_data = {}

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
        "Doya kore apni koyti coin ba diamond kinte chan, tar poriman (minimum 1) ekhane likhe pathan:",
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

# ChangeNOW Swap API (v2) এর মাধ্যমে এক্সচেঞ্জ/পেমেন্ট তৈরি করার ফাংশন
async def create_changenow_exchange(total_price):
    url = "https://api.changenow.io/v2/exchange"
    headers = {
        "x-changenow-api-key": CHANGENOW_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "fromCurrency": "usdt",
        "toCurrency": "usdt",
        "fromNetwork": "trx",
        "toNetwork": "bsc",
        "fromAmount": str(total_price),
        "address": RECEIVING_ADDRESS,
        "flow": "standard"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            data = await response.json()
            if response.status == 200:
                return data, None
            else:
                error_msg = data.get("message", "Unknown API Error")
                return None, f"Error ({response.status}): {error_msg}"

# ইউজার যখন কয়েনের পরিমাণ লিখে পাঠাবে (Minimum 1 coin = $0.01)
@dp.message(F.text.regexp(r'^\d+$'))
async def process_coin_amount(message: types.Message):
    amount = int(message.text)
    
    if amount < 1:
        await message.answer("⚠️ Minimum 1 coin ($0.01) select korte hobe.")
        return

    price_per_coin = 0.01
    total_price = round(amount * price_per_coin, 2)
    
    user_temp_data[message.from_user.id] = {
        "amount": amount,
        "total_price": total_price
    }
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Pay Now (${total_price:.2f} USDT)", callback_data="make_payment")]
        ]
    )
    
    await message.answer(
        f"✅ Apni **{amount}** ti coin select korechen.\n"
        f"💵 Proti coin-er dam: **$0.01**\n"
        f"💰 Mot mullo (Total Price): **${total_price:.2f} USD**\n\n"
        "Nicher button-e click kore ChangeNOW-er madhyome payment complete korun:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ইউজার "Pay Now" বাটনে ক্লিক করলে যা হবে
@dp.callback_query(F.data == "make_payment")
async def process_payment_callback(callback: types.CallbackQuery):
    user_data = user_temp_data.get(callback.from_user.id)
    
    if not user_data:
        await callback.message.answer("দুঃখিত, আবার প্রথম থেকে কয়েনের পরিমাণ লিখে পাঠান।")
        await callback.answer()
        return
        
    amount = user_data["amount"]
    total_price = user_data["total_price"]
    
    await callback.message.answer("⏳ ChangeNOW পেমেন্ট অ্যাড্রেস তৈরি হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    exchange_data, error = await create_changenow_exchange(total_price)
    
    if exchange_data:
        payin_address = exchange_data.get("payinAddress")
        from_amount = exchange_data.get("fromAmount")
        tx_id = exchange_data.get("id")
        
        payment_msg = (
            f"🧾 **ChangeNOW Payment Invoice**\n\n"
            f"🆔 **Transaction ID:** `{tx_id}`\n"
            f"🪙 **Item:** {amount} Game Coins\n"
            f"💰 **Send Exact Amount:** `{from_amount}` **USDT (TRC-20)**\n\n"
            f"📥 **Deposit Address (Tap to Copy):**\n"
            f"`{payin_address}`\n\n"
            f"⚠️ *শুধুমাত্র USDT (TRC-20) নেটওয়ার্কে পেমেন্ট পাঠাবেন। পেমেন্ট কনফার্ম হলে অটোমেটিক আপনার অর্ডার প্রসেস হবে।*"
        )
        await callback.message.answer(payment_msg, parse_mode="Markdown")
    else:
        await callback.message.answer(
            f"❌ পেমেন্ট তৈরি করতে সমস্যা হয়েছে।\n"
            f"কারণ: `{error}`",
            parse_mode="Markdown"
        )
    
    await callback.answer()

# রেন্ডার পোর্ট ধরে রাখার জন্য মিনি ওয়েব সার্ভার
async def handle(request):
    return web.Response(text="Bot is running 24/7 with ChangeNOW Swap API!")

app = web.Application()
app.router.add_get("/", handle)

async def start_web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# মূল মেইন ফাংশন
async def main():
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())