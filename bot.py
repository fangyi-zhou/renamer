import os
import re

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
RENAME_REGEX = re.compile(r"^[Ii]'m (\w+)$")


if TOKEN is None:
    raise RuntimeError("Bot TOKEN not set")

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    match = re.match(RENAME_REGEX, message.content)
    if match:
        name = match[1]
        try:
            await client.http.change_nickname(message.guild.id, message.author.id, name)
            await message.channel.send(f"Hello {name}!")
        except discord.errors.Forbidden:
            await message.channel.send(
                f"Hello {name}! I do not have permission to change your name"
            )


client.run(TOKEN)
