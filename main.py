import discord
from discord.ext import commands
import time
import random
import os
import requests
from google import genai
intents = discord.Intents.default()
intents.message_content = True
GEMINI_KEY = "gemini-key-here"
ai_client = genai.Client(api_key=GEMINI_KEY)
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.command()
async def cmds(ctx):
    await ctx.send(f"## **Command List**\n### All commands use $ prefix\naiask\ncoinflip\ndice\ndivide ($divide int int)\nhi\nkill\nmentionme\nmoney\nmultiply ($multiply int int)\nmyid\nmyuser\nmydisplay\nping\nshouldi")
@bot.command()
async def dice(ctx):
    await ctx.send(f"You rolled a {random.randint(1, 6)}")
@bot.command()
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"The coin landed on {result}")
@bot.command()
async def hi(ctx):
    hi = random.choice(["hiiiii", "hi", "haaaiiii", "hai"])
    await ctx.send(f"{hi}")
@bot.command()
async def money(ctx):
    rich = random.randint(0,100000)
    await ctx.send(f"You have ${rich}")
@bot.command()
async def shouldi(ctx):
    shouldi = random.choice(["Yes", "No"])
    await ctx.send(f"{shouldi}")
@bot.command()
async def myid(ctx):
    user_id = ctx.author.id
    await ctx.send(f"Your Discord ID is: {user_id}")
@bot.command()
async def myuser(ctx):
    username = ctx.author.name
    await ctx.send(f"Your Discord Username is: {username}")
@bot.command()
async def mydisplay(ctx):
    display = ctx.author.display_name
    globaln = ctx.author.global_name
    await ctx.send(f"Your Server Display Name is: {display}\nYour Global Display Name is: {globaln}")
@bot.command()
async def multiply(ctx, num1: int, num2: int):
    res = num1*num2
    await ctx.send(f"{num1} times {num2} is {res}")
@bot.command()
async def divide(ctx, num1: int, num2: int):
    res = num1/num2
    await ctx.send(f"{num1} divided by {num2} is {res}")
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Ping is {latency}")
@bot.command()
async def mentionme(ctx):
    await ctx.send(ctx.author.mention)
@bot.command()
async def kill(ctx):
    await ctx.send("no kill, kill is bad")
@bot.command(name="aiask")
async def ask_ai(ctx, *, prompt: str):
    async with ctx.typing():
        try:
            response = await ai_client.aio.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=prompt,
                config={
                    'system_instruction': 'You are a helpful, witty assistant in a Discord server. Keep responses concise.'
                }
            )
            answer = response.text
            if not answer:
                await ctx.send("Gemini returned an empty response. Try rephrasing.")
            elif len(answer) > 2000:
                await ctx.send("The response is too long (> 2000 characters) to send in Discord.")
            else:
                await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred while connecting to Gemini: {e}")
bot.run("discord-key-here")
