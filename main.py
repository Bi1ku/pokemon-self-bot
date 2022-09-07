from dotenv import load_dotenv
from discord.ext import commands
import os
import cv2
import numpy as np
import requests
import json
import time
import asyncio
from urllib.request import Request
import urllib

load_dotenv()
seenPokemon = json.loads(requests.get("http://localhost:3005").text)["data"]


def fetch_image(image_url):
    req = urllib.request.urlopen(
        Request(url=image_url, headers={'User-Agent': 'Mozilla/5.0'}))
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv2.imdecode(arr, -1)  # 'Load it as it is'


def compare_images(image, compared_image):
    difference = cv2.subtract(image, compared_image)
    return not np.any(difference)


bot = commands.Bot(command_prefix="None", self_bot=True)
bot_spam_1 = commands.Bot(command_prefix='.', self_bot=True)
bot_spam_2 = commands.Bot(command_prefix="None", self_bot=True)

# ------------ BOT LOG ------------


@bot.event
@bot_spam_1.event
@bot_spam_2.event
async def on_ready():
    print("Bot is ready")

# ------------ BOT CATCHER EVENT ------------


@ bot.event
async def on_message(message):
    if f'{message.author.name}#{message.author.discriminator}' == "Pokémon#8738":
        if len(message.embeds) and message.embeds[0].title == "A wild pokémon has аppeаred!":
            wild_pokemon = fetch_image(message.embeds[0].image.url)
            for pokemon in seenPokemon:
                if compare_images(fetch_image(pokemon["imageUrl"]), wild_pokemon):
                    return await message.channel.send(f'p!c {pokemon["name"]}')
            await message.channel.send("@here, A wild pokemon appeared!")
            global pokemon_image
            pokemon_image = message.embeds[0].image.url
        elif message.content.startswith("Congratulations") and pokemon_image:
            spliced_words = message.content.split(" ")[8:]
            for word in spliced_words:
                if "!" in word:
                    pokemon_name = " ".join(
                        spliced_words[:spliced_words.index(word) + 1]).replace("!", "")
                    requests.post("http://localhost:3005", json={
                        "name": pokemon_name,
                        "imageUrl": pokemon_image
                    })

# ------------ BOT ACTIVITY SPAM EVENT ------------


@bot_spam_1.command()
async def start_spam(ctx):
    use_bot = 1
    while 1:
        if use_bot == 1:
            await ctx.send("Hello Spam Bot 2")
            use_bot = 2
        elif use_bot == 2:
            await bot_spam_2.get_channel(ctx.channel.id).send("Hello Spam Bot 1")
            use_bot = 1
        time.sleep(5)

# ------------ MULTIPLE DISCORD BOT ASYNCIO EVENT LOOP ------------

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(loop.create_task(
    bot.start(os.getenv("DISCORD_CATCHER"))), loop.create_task(bot_spam_1.start(os.getenv("DISCORD_SPAMMER_1"))), loop.create_task(bot_spam_2.start(os.getenv("DISCORD_SPAMMER_2")))))
