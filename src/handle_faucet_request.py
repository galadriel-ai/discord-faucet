from datetime import datetime

import settings
from src.repository.redis_repository import RedisRepository
from src.repository.web3_repository import Web3Repository
from web3 import Web3


async def execute(
    ctx,
    address,
    web3_repository: Web3Repository,
    web3_repository_devnet: Web3Repository,
    redis_repository: RedisRepository,
):
    try:
        if not Web3.is_address(address):
            print(f"Invalid input address: {address}", flush=True)
            return

        user_id = str(ctx.author.id)
        last_request_ts = redis_repository.get_numeric(user_id)
        current_ts = int(datetime.utcnow().timestamp())
        if last_request_ts and current_ts - last_request_ts < settings.FUNDING_TIMEOUT_SECONDS:
            print(f"Rate limitted user: {user_id}, address: {address}", flush=True)
            return
        is_funds_sending_success = await web3_repository.send_funds(address)
        is_funds_sending_success_devnet = await web3_repository_devnet.send_funds(address)
        if not is_funds_sending_success or not is_funds_sending_success_devnet:
            print(f"Failed to send funds to address: {address}")
        else:
            redis_repository.set(user_id, current_ts)
    except Exception as e:
        print(e, flush=True)
