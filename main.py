from dotenv import load_dotenv
from urllib.request import Request
from discord.ext import commands
import os
import cv2
import numpy as np
import requests
import json
import asyncio
import time
import urllib

load_dotenv()

pokemon_image = ""
seenPokemon = json.loads(requests.get("http://localhost:3005").text)["data"]

def compare_images(img_path, img_path_2):
    req = urllib.request.urlopen(Request(url=img_path, headers={'User-Agent': 'Mozilla/5.0'}))
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    a = cv2.imdecode(arr, -1) # 'Load it as it is'
    req2 = urllib.request.urlopen(Request(url=img_path_2, headers={'User-Agent': 'Mozilla/5.0'}))
    arr2 = np.asarray(bytearray(req2.read()), dtype=np.uint8)
    b = cv2.imdecode(arr2, -1) # 'Load it as it is'
    difference = cv2.subtract(a, b)
    result = not np.any(difference)
    return result


bot = commands.Bot(command_prefix="None", self_bot=True)
bot_spam_1 = commands.Bot(command_prefix='.', self_bot=True)
bot_spam_2 = commands.Bot(command_prefix="None", self_bot=True)

# ------------ BOT LOG ------------


@bot.event
@bot_spam_1.event
@bot_spam_2.event
async def on_ready():
    print('Logged in!')


# ------------ BOT ACTIVITY SPAM EVENT ------------

bots = []
bots.append(bot_spam_1)
bots.append(bot_spam_2)

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
        

# ------------ BOT CATCHER EVENT ------------

@bot.event
async def on_message(message):
    if f'{message.author.name}#{message.author.discriminator}' == "Pokémon#8738":
        if len(message.embeds) and message.embeds[0].image.url:
            given_img_url = message.embeds[0].image.url
            for pokemon in seenPokemon:
                if compare_images(pokemon["imageUrl"], given_img_url):
                    return await bot.get_channel(message.channel.id).send(f'p!c {pokemon["name"]}')
            await bot.get_channel(message.channel.id).send("@here, A wild pokemon appeared!")
            global pokemon_image
            pokemon_image = given_img_url
        elif message.content.startswith("Congratulations") and pokemon_image:
            spliced_words = message.content.split(" ")[8:]
            for word in spliced_words:
                if "!" in word:
                    pokemon_name = " ".join(spliced_words[:spliced_words.index(word) + 1]).replace("!", "")
                    requests.post("http://localhost:3005", json={
                        "name": pokemon_name,
                        "imageUrl": pokemon_image
                    })

loop = asyncio.get_event_loop()
loop.create_task(bot.start(os.getenv("DISCORD_CATCHER")))
loop.create_task(bot_spam_1.start(os.getenv("DISCORD_SPAMMER_1")))
loop.create_task(bot_spam_2.start(os.getenv("DISCORD_SPAMMER_2")))
loop.run_forever()
