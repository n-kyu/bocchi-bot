import os
from pyexpat import model
import random
import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
DISCORD_BOT_TOKEN=os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")


intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key=OPENAI_API_KEY

#Emoticons List
emoticons = [
    "૮(˶╥︿╥)ა",
    "(╥﹏╥)",
    "(╥ᆺ╥；)",
    "(◉ ᴖ ◉)",
    "(⊃◜⌓◝⊂)",
    "(─ ‿ ─)",
    "🗿",
    "😳"
]

async def search_history_channel(channel, limit=10):
    messages_list = []
    async for message in channel.history(limit=limit, oldest_first=True):

        messages_list.append({
            "role": "user" if message.author.id != bot.user.id else "system",
            "content": message.content
        })
    return messages_list


def asking_gpt(gptmessage):

    response = openai.ChatCompletion.create(
        messages=gptmessage,
        model="gpt-3.5-turbo-16k",
        temperature=0.8,
        max_tokens=1000
    )

    return response.choices[0].message.content


@bot.event
async def on_ready():
        print(f"{bot.user.name} is ready!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    async with message.channel.typing():
        history_messages = await search_history_channel(message.channel)
        response = asking_gpt(history_messages)

        emoticon = random.choice(emoticons)
        response_with_emoticon = f"{response} {emoticon}"

        await message.reply(response_with_emoticon)

    await bot.process_commands(message)



bot.run(DISCORD_BOT_TOKEN)