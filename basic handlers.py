from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio

app = Client("my_personal")

logging.basicConfig(level=logging.INFO)

@app.on_message()
async def log_message(client, message):
    logging.info(f"Message from {message.from_user.username}: {message.text}")

@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = [[InlineKeyboardButton("Help", callback_data="help")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text("Welcome! Click for help:", reply_markup=reply_markup)

@app.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text("Available commands:\n/start - Start the bot\n/help - Show this help message\n/echo - Echo the message")

@app.on_message(filters.text & ~filters.command(["start", "help"]))
async def echo(client, message):
    await message.reply_text(message.text)

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    if callback_query.data == "help":
        await callback_query.answer("Use /help to get a list of commands.")

@app.on_message(filters.new_chat_members)
async def welcome(client, message):
    for member in message.new_chat_members:
        await message.reply_text(f"Welcome {member.mention}!")

@app.on_message(filters.photo)
async def photo_handler(client, message):
    await message.reply_text("Nice photo!")

app.run()
