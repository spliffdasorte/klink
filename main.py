import discord
import asyncio
import os
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="k.", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"[BOT] {bot.user} online")

    for f in sorted(os.listdir("cogs")):
        if f.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{f[:-3]}")
                print(f"[COG] {f[:-3]} ✓")
            except Exception as e:
                print(f"[COG] {f[:-3]} ✗ {e}")

    try:
        await bot.tree.sync()
        print("[CMD] Slash sync ✓")
    except Exception as e:
        print(f"[CMD] Sync ✗ {e}")

asyncio.run(bot.start(token))