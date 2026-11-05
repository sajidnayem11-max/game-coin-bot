import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from cryptomus import Client  # ক্রিপ্টোমাস লাইব্রেরি

# আপনার বটের টোকেন এবং ক্রিপ্টোমাস ক্রডেনশিয়াল এখানে বসাবেন
TOKEN = "9279326916:AAEYUtRjvy8zOyvObk4eJ72YzS6ZL5JDh3c"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ক্রিপ্টোমাস ক্লায়েন্ট ইনিশিয়ালাইজেশন
# cryptomus = Client.payment(api_key=PAYMENT_API_KEY, uuid=MERCHANT_UUID)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalamu Alaikum!\n\nAmader Game Coin & Diamond Store-e apnake shagotom. 🪙💎\n\nApni kon game-er item kinte chan, niche theke select korun:")
@dp.message(Command("support"))
async def support_cmd(message: types.Message):
    support_text = (
        "🛠 **Customer Support & Assistance**\n\n"
        "Kono shomossha ba payment related issue- er jonno doya kore amader official support team er sathe jogajog korun:\n\n"
        "👤 **Support Admin:** @ShamiulAzim1701\n\n"
        "Amra apnake sahajjo korar jonno 24/7 prostut royechi!"
    )
    await message.answer(support_text, parse_mode="Markdown")
    
# যখন ইউজার কয়েনের পরিমাণ লিখে পাঠাবে
@dp.message(F.text.regexp(r'^\d+$'))
async def process_coin_amount(message: types.Message):
    amount = message.text
    await message.answer(f"**Flight Charbe Coins** select korechen.\n\nApni {amount} ti coin kinte cheyechan. Ekjon merchant payment link toiri hocche...")
    
    try:
        # এখানে ক্রিপ্টোমাস ইনভয়েস তৈরির API কল হবে
        # invoice = cryptomus.create({
        #     "amount": str(int(amount) * 10), # আপনার প্রাইস অনুযায়ী ক্যালকুলেশন
        #     "currency": "USD",
        #     "order_id": str(message.from_user.id) + "_" + amount
        # })
        # payment_url = invoice['result']['url']
        # await message.answer(f"🔗 Payment Link:\n{payment_url}")
        
        # সাময়িকভাবে টেস্ট করার জন্য ডেমো টেক্সট:
        await message.answer("✅ Apnar pament invoice toiri hoyeche. (Cryptomus API key connect korle ekhane payment link chole ashbe)")
    except Exception as e:
        await message.answer("❌ Payment link toiri korte somossa hoyeche. Doya kore abar chesta korun.")

# ১. রেন্ডার পোর্ট ধরে রাখার জন্য মিনি ওয়েব সার্ভার
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