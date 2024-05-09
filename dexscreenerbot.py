import discord
from discord.ext import commands
import aiohttp
import asyncio

# Discord bot token
TOKEN = '...'

# Intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True

# Initialize Discord client with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# API endpoint
TOKEN_ADDRESS = '0xa0D445dC147f598d63518b5783CA97Cd8Bd9f5Bc'
API_URL = f'https://api.dexscreener.com/latest/dex/tokens/{TOKEN_ADDRESS}'

async def update_bot_name():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Extract FDV (Fully Diluted Valuation) from the response
                        fdv = data['pairs'][0].get('fdv')  # Assuming we're getting data for a single pair

                        # Formatting FDV value
                        formatted_fdv = f"MC - ${fdv / 10**6:.2f}M"

                        # Updating bot's nickname with the formatted FDV
                        for guild in bot.guilds:
                            await guild.me.edit(nick=formatted_fdv)
                            print("Nickname updated to:", formatted_fdv)
                    else:
                        print("Failed to fetch data from the API. Status code:", response.status)
        except Exception as e:
            print("An error occurred:", str(e))

        # Sleep for 10 seconds before next update
        await asyncio.sleep(10)

# Event: Bot is ready
@bot.event
async def on_ready():
    print('Bot is ready!')

# Event: Bot setup
@bot.event
async def on_connect():
    print('Bot connected!')
    bot.loop.create_task(update_bot_name())

# Custom command: /squeak
@bot.command()
async def squeak(ctx):
    print("Squeak command received.")  # Debug print
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    fdv = data['pairs'][0].get('fdv')  # Assuming we're getting data for a single pair
                    formatted_fdv = f"MC - ${fdv / 10**6:.2f}M"
                    await ctx.send(formatted_fdv)
                else:
                    await ctx.send("Failed to fetch data from the API.")
    except Exception as e:
        print("An error occurred:", str(e))
        await ctx.send("An error occurred while processing the command.")

# Run the bot
bot.run(TOKEN)
