import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your bot token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("CHAT_ID")

# Global variable to hold the current todo list state (in a production app, use a database)
current_todo_list = []

def create_todo_list():
    todo_list = [
        "Sobh",
        "Dohr",
        "Asr",
        "Maghreb",
        "Icha"
    ]
    formatted_list = "\n".join(todo_list)
    return f"Prayers:\n{formatted_list}", todo_list

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_daily_todo_list(context)

async def send_daily_todo_list(context: ContextTypes.DEFAULT_TYPE):
    global current_todo_list
    todo_message, current_todo_list = create_todo_list()
    
    # Create inline keyboard buttons for the todo list
    keyboard = [[InlineKeyboardButton(task, callback_data=task) for task in current_todo_list]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=todo_message, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    task_name = query.data
    user_name = query.from_user.first_name

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")
    
    response_text = f"{user_name} prayed {task_name} {date} at {time}"
    
    await context.bot.send_message(chat_id=query.message.chat_id, text=response_text)

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()