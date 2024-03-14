from web3 import AsyncWeb3

import settings


class Web3Repository:
    def __init__(self):
        self.web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_RPC_URL))
        self.account = self.web3_client.eth.account.from_key(settings.PRIVATE_KEY)

    async def send_funds(
        self,
        to_address: str,
        amount_wei: int = settings.FUNDING_AMOUNT_WEI
    ) -> bool:
        try:
            nonce = await self.web3_client.eth.get_transaction_count(self.account.address)

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
            return bool(tx_receipt.get("status"))
        except Exception as e:
            print(e, flush=True)
            return False
