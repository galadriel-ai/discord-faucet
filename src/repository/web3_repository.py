from typing import Optional

from eth_utils import is_checksum_address
from eth_utils import to_checksum_address
from web3 import AsyncWeb3

import settings
from src import api_logger

logger = api_logger.get()


class Web3Repository:
    def __init__(self, rpc_url: str):
        self.web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc_url))
        self.account = self.web3_client.eth.account.from_key(settings.PRIVATE_KEY)

    async def send_funds(
        self,
        to_address: str,
        amount_wei: int = settings.FUNDING_AMOUNT_WEI
    ) -> bool:
        try:
            nonce = await self.web3_client.eth.get_transaction_count(self.account.address)

            if not is_checksum_address(to_address):
                logger.debug(f"Input address {to_address} is not a checksum address, trying to convert..")
                to_address = to_checksum_address(to_address)
            signed_tx = self.web3_client.eth.account.sign_transaction(
                {
                    "chainId": settings.CHAIN_ID,
                    "to": to_address,
                    "nonce": nonce,
                    "gas": 21000,
                    "maxFeePerGas": self.web3_client.to_wei("1", "gwei"),
                    "maxPriorityFeePerGas": self.web3_client.to_wei("1", "gwei"),
                    "value": amount_wei,
                },
                private_key=self.account.key
            )
            tx_hash = await self.web3_client.eth.send_raw_transaction(
                signed_tx.rawTransaction
            )
            tx_receipt = await self.web3_client.eth.wait_for_transaction_receipt(tx_hash)
            is_success = bool(tx_receipt.get("status"))
            if is_success:
                logger.debug(f"Successfully sent funds to {to_address}")
            else:
                logger.debug(f"Failed to send funds to {to_address}")
            return is_success
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

    async def get_balance(self) -> Optional[int]:
        try:
            return await self.web3_client.eth.get_balance(self.account.address)
        except Exception as e:
            logger.error(f"Balance check fail: {e}", exc_info=True)
            return None
