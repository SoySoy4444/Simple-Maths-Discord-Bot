# Created 21/05/20
# https://realpython.com/how-to-make-a-discord-bot-python/
# You can't do simple maths under pressure Discord Bot

import os
import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

answer_ = "XXXXadsadsasasdsadas"
@client.event
async def on_message(message):
    guild = client.guilds[0]

    global answer_

    if "!maths" in message.content:
        await message.channel.send("Starting new game... enter to quit game.")
        question = "4 + 3 + 4"
        await message.channel.send(question)
        answer_ = eval(question)
        print("ANSWER IS", answer_)
        print(type(answer_))

    elif message.content.startswith(str(answer_)):
        await message.channel.send(f"Correct! It's {str(answer_)}!")

        n1 = str(random.randint(3, 9))
        n2 = str(random.randint(3, 9))
        n3 = str(random.randint(3, 9))
        operators = ["+", "*", "-"]
        o1 = random.choice(operators)
        o2 = random.choice(operators)
        question = f"{n1} {o1} {n2} {o2} {n3}"
        await message.channel.send(question)
        answer_ = eval(question)
        print("ANSWER IS", answer_)
        print(type(answer_))

    elif "!quit" in message.content:
        print("TRIGGGG")
        await message.channel.send("Thanks for playing!")
        await message.channel.send("The winner was...")
        pass


client.run(TOKEN)
