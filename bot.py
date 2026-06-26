import os
from telegram import ReplyKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")

BUTTONS = [
    ["New shift with PTI", "Add Break"],
    ["Add drive time", "Add shift time"],
    ["New cycle", "New Shift with PTI + New Cycle"],
    ["Request a callback", "Add PTI"],
    ["⚠️⚠️⚠️ DOT INSPECTION ⚠️⚠️⚠️", "New shift without PTI"],
    ["New Shift with PTI + Cycle hours", "Cycle hours"],
    ["Scheduled New Shift", "Only Fix Logs (don't add time)"],
]

VALID = {btn for row in BUTTONS for btn in row}

KEYBOARD = ReplyKeyboardMarkup(
    BUTTONS,
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Choose action..."
)


async def menu(update, context):
    try:
        await update.message.delete()
    except Exception:
        pass
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Choose:",
        reply_markup=KEYBOARD
    )


async def handle(update, context):
    text = update.message.text
    if text not in VALID:
        return


async def post_init(app):
    await app.bot.set_my_commands([
        BotCommand("menu", "Open quick actions")
    ])


def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot started! Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
