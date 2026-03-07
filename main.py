import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json
import aiohttp
import certifi
import ssl

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)

UTILS_FILE = "utils.json"

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

data = load_json(UTILS_FILE)

data.setdefault("roles", {})     # stores roles for set and assign


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "whisper sucks" in message.content.lower():
        await message.channel.send(f"{message.author.mention}, shut your lame ass up.")

    await bot.process_commands(message)

# $hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! My name is {ctx.bot.user.mention}!")

role_storage = {}

# sets a role to assign later saves the set to utils.json
@bot.command()
async def set(ctx, role: discord.Role = None):
    guild_id = str(ctx.guild.id)
    if role is None:
        saved_role_id = data["roles"].get(guild_id)

        if not saved_role_id:
            return await ctx.send("No role has been set yet!")

        saved_role = ctx.guild.get_role(saved_role_id)

        if saved_role is None:
            return await ctx.send("The saved role doesn't exist anymore!")

        return await ctx.send(f"Currently set role to: {saved_role.mention}")

    data["roles"][str(ctx.guild.id)] = role.id
    save_json(data, UTILS_FILE)
    await ctx.send(f"Role set to: {role.mention}")

# assign to assign role, role comes from utils.json
@bot.command()
async def assign(ctx):
    role_id = data["roles"][str(ctx.guild.id)]

    if role_id is None:
        await ctx.send("Sadly, no role has been assigned yet...")
        return

    role = ctx.guild.get_role(role_id)

    if role is None:
        await ctx.send("Hey, the role got deleted or doesn't exist anymore?!")
        return

    await ctx.author.add_roles(role)
    await ctx.send(f"You're now officially a {role.mention}!")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="WhisperBot Command's",
        description="Use the prefix ` $ ` for commands.",
        color=0xfdfdfd
    )
    embed.add_field(
        name="Set",
        value="Sets a role using a role ID to used later with assign.",
        inline=False
    )
    embed.add_field(
        name="Assign",
        value="Assigns a role to the user using the command that was set with the previous set command.",
        inline=False
    )
    await ctx.send(embed=embed)

ssl_context = ssl.create_default_context(cafile=certifi.where())

# $yokai {yokaiNumber} to generate image of a yokai
# api doesnt work anymore
@bot.command()
async def yokai(ctx, id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://yokaiwatch-api-production.up.railway.app/api/yokai/{id}",
            ssl=ssl_context
        ) as resp:

            if resp.status == 400:
                return await ctx.send("Not a valid Yokai!")

            if resp.status == 429:
                return await ctx.send("Rate limited! :(")

            if resp.status == 404:
                return  await ctx.send("Yokai not found! Yet...")

            data = await resp.json()
            await ctx.send(data['data']['imageurl'])


bot.run(token, log_handler=handler, log_level=logging.DEBUG)


