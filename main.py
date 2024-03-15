# This example requires the 'message_content' intent.
from threading import Thread

import discord
from discord.ext import commands

import settings
import uvicorn
from fastapi import FastAPI
from src import handle_faucet_request
from src.repository.redis_repository import RedisRepository
from src.repository.web3_repository import Web3Repository

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

web3_repository = Web3Repository()
redis_repository = RedisRepository()

app = FastAPI()


@app.get("/metrics")
async def read_root():
    return await web3_repository.get_balance()


# Function to run the Uvicorn server
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


server_thread = Thread(target=run_server)

# Start the server thread
server_thread.start()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.command()
async def faucet(ctx, address):
    # TODO: handle  sending funds to address
    print(f"!faucet {address}")
    await handle_faucet_request.execute(
        ctx,
        address,
        web3_repository,
        redis_repository,
    )


client.run(settings.DISCORD_TOKEN)
