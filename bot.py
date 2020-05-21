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

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


answer_ = "XXXXadsadsasasdsadas"
usersPlaying = {}


def get_question(difficulty):  # difficulty is an integer from 1 - 10
    lower_bound = 2
    upper_bound = (difficulty + 2) * 2  # 6 (level 1) - 24 (level 10)

    operators = ["+", "*", "-"]
    question = ""
    question += str(random.randint(lower_bound, upper_bound))

    for _ in range(difficulty//2):
        number = str(random.randint(lower_bound, upper_bound))
        operation = random.choice(operators)
        question += operation + number

    return question


@client.event
async def on_message(message):
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    global answer_
    global usersPlaying

    if message.content == "!maths":
        usersPlaying = {}
        await message.channel.send("Starting new game... enter !quit to quit game.")
        question = get_question(3)
        await message.channel.send(question)
        answer_ = eval(question)

    elif message.content == str(answer_):
        await message.channel.send(f"Correct! It's {str(answer_)}!")
        correct_user = message.author  # get the user who answered correctly

        if correct_user in usersPlaying.keys():  # if the answer is already in the database
            usersPlaying[correct_user] += 1  # increase the user's score
        else:
            usersPlaying[correct_user] = 1  # start tracking user score
        question = get_question(5)
        await message.channel.send(question)
        answer_ = eval(question)

    elif message.content == "!quit":
        await message.channel.send("Thanks for playing!")

        current_max_user, current_max_score = None, -1
        for user, score in usersPlaying.items():
            if score > current_max_score:
                current_max_user, current_max_score = user, score

        await message.channel.send(f"The winner was {current_max_user} with a score of {current_max_score}!")
        # TODO: Add leaderboard?


client.run(TOKEN)
