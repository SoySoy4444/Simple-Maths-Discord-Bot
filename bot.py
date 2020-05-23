# Created 21/05/20
# https://realpython.com/how-to-make-a-discord-bot-python/
# You can't do simple maths under pressure Discord Bot

import os
import discord
from dotenv import load_dotenv
import random
import asyncio

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


usersPlaying = {}
playing = False


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
    if message.author == client.user:
        return

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    global usersPlaying
    global playing

    if message.content == "!maths":
        game_channel = message.channel

        playing = True
        usersPlaying = {}
        time_limit = 10.0
        await message.channel.send("Starting new game... enter !quit to quit game.")

        def wait_for_correct_answer(m):
            # check answer is correct and is sent in the game channel
            return m.content == str(answer_) and m.channel == game_channel

        while playing:
            question = get_question(3)
            await game_channel.send(question)
            answer_ = eval(question)
            try:
                reply = await client.wait_for('message', timeout=time_limit, check=wait_for_correct_answer)
                # if execution continues to here, user has gotten it correct
                await game_channel.send(f"Correct! It's {str(answer_)}!")

                correct_user = reply.author  # get the user who answered correctly
                if correct_user in usersPlaying.keys():  # if the answer is already in the database
                    usersPlaying[correct_user] += 1  # increase the user's score
                else:
                    usersPlaying[correct_user] = 1  # start tracking user score
            except asyncio.TimeoutError:
                if playing:
                    await game_channel.send(f"Too slow! The answer was {answer_}!")

    elif message.content == "!quit":
        playing = False
        await message.channel.send("Thanks for playing!")

        current_max_user, current_max_score = None, 0
        for user, score in usersPlaying.items():
            if score > current_max_score:
                current_max_user, current_max_score = user, score

        await message.channel.send(f"The winner was {current_max_user} with a score of {current_max_score}!")
        # TODO: Add leaderboard?


client.run(TOKEN)
