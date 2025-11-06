from cdp import CdpClient
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Initialize the CDP client, which automatically loads
    # the API Key and Wallet Secret from the environment
    # variables.
    cdp = CdpClient()
    await cdp.close()


asyncio.run(main())
