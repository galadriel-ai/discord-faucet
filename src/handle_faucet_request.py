from datetime import datetime

from web3 import Web3

import settings
from src import api_logger
from src.repository.redis_repository import RedisRepository
from src.repository.web3_repository import Web3Repository

logger = api_logger.get()


async def execute(
    ctx,
    address,
    web3_repository: Web3Repository,
    redis_repository: RedisRepository,
):
    try:
        if not Web3.is_address(address):
            logger.debug(f"Invalid input address: {address}")
            return

        user_id = str(ctx.author.id)
        last_request_ts = redis_repository.get_numeric(user_id)
        current_ts = int(datetime.utcnow().timestamp())
        if last_request_ts and current_ts - last_request_ts < settings.FUNDING_TIMEOUT_SECONDS:
            logger.debug(f"Rate limitted user: {user_id}, address: {address}")
            return
        is_funds_sending_success = await web3_repository.send_funds(address)
        if not is_funds_sending_success:
            logger.error(f"Failed to send funds to address: {address}")
        else:
            redis_repository.set(user_id, current_ts)
    except Exception as e:
        logger.debug(e)
