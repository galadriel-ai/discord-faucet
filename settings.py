from dotenv import load_dotenv
import os

load_dotenv()

APPLICATION_NAME = "DISCORD_FAUCET"
LOG_FILE_PATH = "logs/logs.log"

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

FUNDING_AMOUNT_WEI: int = int(os.getenv("FUNDING_AMOUNT_WEI", 0.1 * 10 ** 18))
FUNDING_TIMEOUT_SECONDS = int(os.getenv("FUNDING_TIMEOUT_SECONDS", 12 * 3600))  # 12 hours

CHAIN_ID = int(os.getenv("CHAIN_ID"))
WEB3_DEVNET_RPC_URL = os.getenv("WEB3_DEVNET_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
