from pyrogram import Client, filters
import requests
import random
import logging

# Setting up basic logging
logging.basicConfig(level=logging.INFO)

app = Client("my_account")


@app.on_message(filters.command("start"))
async def start(client, message):
    greetings = ["Hello!", "Hi there!", "Greetings!", "Welcome!"]
    greeting = random.choice(greetings)

    try:
        # Fetch a random anime picture from Nekos API using JSON response
        res = requests.get("https://api.nekosapi.com/v3/images/random")
        res.raise_for_status()

        data = res.json()
        matching_image_urls = []

        # Iterate over items and get the image_url if description matches
        check = False
        for item in data["items"]:
            for tag in item["tags"]:
                if 'user_enter' in tag["description"]:
                    matching_image_urls.append(item["image_url"])
                    check = True
                    break  # Stop checking other tags if a match is
            if check == True:
                break
        print(matching_image_urls)
        image_url = matching_image_urls[0]
        print(image_url)
        if image_url:
            await message.reply_photo(photo=image_url, caption=greeting)
        else:
            logging.info(f"Response JSON without 'url': {data}")
            await message.reply_text("No image found, but hi!")

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        await message.reply_text("Failed to fetch an image due to an error!")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await message.reply_text("An unexpected error occurred!")


@app.on_message(filters.command("info"))
async def info(client, message):
    user = message.from_user
    user_info = f"ID: {user.id}\nName: {user.first_name} {user.last_name if user.last_name else ''}\nUsername: {user.username}"
    await message.reply_text(user_info)


app.run()
