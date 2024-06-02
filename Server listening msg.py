from pyrogram import Client, filters, idle

app = Client("my_account")

@app.on_message(filters.text)
async def handler(client, message):
    sender = message.from_user
    print(f"New message from {sender.username}: {message.text}")

async def main():
    await app.start()
    print("Listening for new messages...")
    await idle()  # Keep the client running
    await app.stop()

app.run(main())
