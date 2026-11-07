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

# NOWPayments-এর মাধ্যমে ইনভয়েস তৈরি করার ফাংশন
async def create_nowpayments_invoice(amount, total_price):
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {
        "x-api-key": "BX8B69Z-A5B4PWH-Q85HAH8-135H7K1",
        "Content-Type": "application/json"
    }
    payload = {
        "price_amount": total_price,
        "price_currency": "usd",
        "pay_currency": "usdttrc20",
        "order_id": f"ORDER_{amount}_{int(asyncio.get_event_loop().time())}",
        "order_description": f"{amount} Game Coins Purchase",
        "ipn_url": "https://game-coin-bot.onrender.com/ipn",  # এখানে IPN লিঙ্ক যুক্ত করা হলো
        "success_url": "https://game-coin-bot.onrender.com/success",
        "cancel_url": "https://game-coin-bot.onrender.com/cancel"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("invoice_url"), None
            else:
                err_text = await response.text()
                return None, f"Error Code {response.status}: {err_text}"

# ইউজার "Pay Now" বাটনে ক্লিক করলে যা হবে
@dp.callback_query(F.data == "make_payment")
async def process_payment_callback(callback: types.CallbackQuery):
    invoice_url, error = await create_nowpayments_invoice(100, 2.00)
    
    if invoice_url:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Complete Payment", url=invoice_url)]
            ]
        )
        await callback.message.answer("নিচের লিংকে ক্লিক করে পেমেন্ট সম্পন্ন করুন:", reply_markup=keyboard)
    else:
        await callback.message.answer(f"পেমেন্ট ইনভয়েস তৈরি করতে সমস্যা হচ্ছে।\nডিবাগ এরর: `{error}`", parse_mode="Markdown")
    
    await callback.answer()

# ইউজার যখন কয়েনের পরিমাণ লিখে পাঠাবে
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

# IPN নোটিফিকেশন রিসিভ করার ওয়েব রাউট
async def handle_ipn(request):
    try:
        data = await request.json()
        payment_status = data.get("payment_status")
        order_id = data.get("order_id")
        
        if payment_status in ["finished", "confirmed"]:
            print(f"Payment successful for Order: {order_id}")
            
        return web.json_response({"status": "success"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

# মিনি ওয়েব সার্ভার
async def handle(request):
    return web.Response(text="Bot is running 24/7!")

app = web.Application()
app.router.add_get("/", handle)
app.router.add_post("/ipn", handle_ipn)

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