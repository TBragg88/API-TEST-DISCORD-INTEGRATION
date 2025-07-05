import discord
from discord.ext import commands
from poke_api import fetch_move_details

from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv("token.env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"🟢 {bot.user.name} has connected to Discord!")


@bot.command()
async def move(ctx, *, move_name: str):
    move_name = move_name.lower().replace(" ", "-")

    move = await fetch_move_details(move_name)
    if move:
        raw_name = move["name"]
        display_name = raw_name.replace("-", " ").title()
        type_ = move["type"]["name"].title()
        accuracy = move["accuracy"]
        power = move["power"] or "N/A"
        pp = move["pp"]
        description = next(
            (entry["flavor_text"] for entry in move["flavor_text_entries"]
             if entry["language"]["name"] == "en"),
            "No description found."
        )
        message = (
            f"**{display_name}**\n"
            f"Type: {type_}\n"
            f"Accuracy: {accuracy}\n"
            f"Power: {power}\n"
            f"PP: {pp}\n"
            f"Description: {description}"
        )
        await ctx.send(message)
    else:
        await ctx.send(f"Couldn't find a move called `{move_name}`!")


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
