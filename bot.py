import discord
from discord.ext import commands
import random
from poke_api import fetch_move_details
from poke_api import fetch_pokemon_details
from poke_api import fetch_species_details
from config import TYPE_STYLES
from dotenv import load_dotenv
import os


load_dotenv("token.env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",
                   intents=intents,
                   help_command=None,
                   case_insensitive=True)


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


@bot.command()
async def pokemon(ctx, *, name: str):
    pokemon = await fetch_pokemon_details(name)
    if not pokemon:
        return await ctx.send(f"❌ Couldn't find a Pokémon named `{name}`.")

    species = await fetch_species_details(name)
    flavor_text = next(
        (entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
         for entry in species.get("flavor_text_entries", [])
         if entry["language"]["name"] == "en"),
        "No description available."
    )

    types = [t["type"]["name"].capitalize() for t in pokemon["types"]]
    type_line = " ".join(
        f"{TYPE_STYLES.get(t, {'emoji': '❓'})['emoji']} {t}" for t in types
    )
    color = TYPE_STYLES.get(types[0], {}).get("color", 0x5865F2)

    display_name = pokemon["name"].capitalize()
    poke_id = pokemon["id"]
    sprite = pokemon["sprites"]["front_default"]
    stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon["stats"]}
    abilities = ", ".join(a["ability"]["name"].title()
                          for a in pokemon["abilities"])
    height = pokemon["height"] / 10
    weight = pokemon["weight"] / 10

    embed = discord.Embed(
        title=f"{display_name} (#{poke_id})",
        description=f"Type: {type_line}",
        color=color
    )

    if sprite:
        embed.set_thumbnail(url=sprite)

    embed.add_field(name="Abilities",
                    value=abilities or "N/A",
                    inline=True)
    embed.add_field(name="Height",
                    value=f"{height} m",
                    inline=True)
    embed.add_field(name="Weight",
                    value=f"{weight} kg",
                    inline=True)
    embed.add_field(name="Description",
                    value=flavor_text,
                    inline=False)

    stat_labels = {
        "hp": "HP",
        "attack": "Atk",
        "defense": "Def",
        "special-attack": "Sp. Atk",
        "special-defense": "Sp. Def",
        "speed": "Speed"
    }

    total_base_stat = 0
    for stat_key, label in stat_labels.items():
        val = stats.get(stat_key)
        if val is not None:
            embed.add_field(name=label, value=str(val), inline=True)
            total_base_stat += val

    embed.add_field(name="Total", value=str(total_base_stat), inline=False)

    await ctx.send(embed=embed)


@bot.command("help")
async def pokehelp(ctx):
    await ctx.send("Hello, I'm PokeNerd!"
                   "Need some help?\n"
                   'Just type `!pokemon <pokemon>` for Pokémon data\n'
                   'or `!move <move>` to get info about a move.')


@bot.command()
async def steve(ctx):
    cool = random.choice(["cool ❤️", "not cool 😆"])
    await ctx.send(
        f"Hey {ctx.author.mention}, "
        f"Stëve thinks you're {cool}")


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
