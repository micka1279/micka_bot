from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

BOT_TOKEN = "7389369003:AAE2cmMX0poh_9krlroyI0Fqty7zAa3uE0Q"
CHANNELS = ['+Mv0etmH7HGFkMDU0', '@Film_Zone_Fr12425', '@actuality_zone1242', '@Film_Zone_Fr1242']

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Tu es automatiquement accepté dans le canal après avoir rejoint ces canaux :\n\n"
    for i, channel in enumerate(CHANNELS, 1):
        if channel.startswith("@"):
            text += f"{i}/ https://t.me/{channel[1:]}\n"
        else:
            text += f"{i}/ https://t.me/{channel}\n"
    text += "\nUne fois que c’est fait clique sur le bouton ci-dessous."
    keyboard = [[InlineKeyboardButton("Vérification ✅", callback_data="verify")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    all_joined = True
    for channel in CHANNELS:
        try:
            chat_id = channel if channel.startswith("@") else "@" + channel
            member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                all_joined = False
                break
        except:
            all_joined = False
            break

    if all_joined:
        await query.answer("Accès accordé ✅")
        await query.edit_message_text("Tu es maintenant accepté ✅")
    else:
        await query.answer("Tu n'as pas rejoint tous les canaux", show_alert=True)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify))
app.run_polling()
