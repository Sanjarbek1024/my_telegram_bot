from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import requests
from keep_alive import keep_alive

TOKEN = "5954744651:AAGxOmbMsGgMOEoaGCWQH56MMDDXNUc0MLc"

# Kanallar uchun ID
REQUIRED_CHANNELS = [
    {"username": "@Sanjarbeks_notes", "id": "-100XXXXXXXXX"},
    {"username": "@Sanjarbek_Gulomjonov", "id": "-100XXXXXXXXX"}
]

# Kanal obunasini tekshirish funksiyasi
def check_subscription(user_id):
    for channel in REQUIRED_CHANNELS:
        url = f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={channel['id']}&user_id={user_id}"
        response = requests.get(url).json()
        status = response.get("result", {}).get("status", "")
        if status not in ["member", "administrator", "creator"]:
            return False, channel["username"]
    return True, None

# Start komandasi
async def start(update: Update, context):
    user_id = update.effective_user.id
    is_subscribed, channel = check_subscription(user_id)
    if not is_subscribed:
        await update.message.reply_text(
            f"Botdan foydalanish uchun {channel} kanaliga obuna bo‘ling!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Obuna bo‘lish", url=f"https://t.me/{channel[1:]}")]]
            )
        )
        return

    keyboard = [
        [InlineKeyboardButton("Men haqimda", callback_data="about")],
        [InlineKeyboardButton("Kanallarni ko‘rish", callback_data="channels")],
        [InlineKeyboardButton("Qo‘shimcha imkoniyatlar", callback_data="extra")]
    ]
    await update.message.reply_text(
        "Assalomu alaykum! Men @Sanjarbeks_bot. Quyidagilardan birini tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Tugmalarni boshqarish
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_text(
            "👤 *Sanjarbek haqida:*\n\n"
            "🧑‍💻 *Yashash joyi:* Yer sayyorasi"
            "🧑‍💻 *Yoshi*: 17 yosh\n"
            "📚 *Soham*: Finance, BI and AI, Business management. \n"
            "🏆 *Yutuqlar*: SEAMO[Gold and Bronze medals], IELTS 6, SAT __, Iqtidorly camp, NSO[Bronze medal]. Yana yutuqlarim bor, lekin eslolmadim yokida sir.\n"
            "🎯 *Qiziqishlar*: Anig'ini bilmiman, qiziqadigan narsam ham, qiziqmidigan narsam ham judayam ko'p"
        )
    elif query.data == "channels":
        channels = "\n".join([f"🔗 {ch['username']}" for ch in REQUIRED_CHANNELS])
        await query.edit_message_text(f"📢 *Kanallar:* \n\n{channels}")
    elif query.data == "extra":
        await query.edit_message_text("🔧 Bu qism hali ishlab chiqilmoqda!")

# Noto‘g‘ri xabarlar uchun javob
async def unknown(update: Update, context):
    await update.message.reply_text("Kechirasiz, men bu buyruqni tushunmadim. /start ni bosing.")

# Asosiy kod
if __name__ == "main":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("Bot ishlamoqda...")
    keep_alive()
    app.run_polling()
