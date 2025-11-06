import asyncio
from cdp import CdpClient
from dotenv import load_dotenv

load_dotenv()

async def list_evm_balances():
    """Retrieves and prints token balances for a managed EVM account."""
    
    # ⚠️ NOTE: Replace 'MyAccountName' with the name of one of your CDP EVM Accounts.
    ACCOUNT_NAME = "MyAccountName" 
    # NOTE: Replace 'base' with your desired network (e.g., 'ethereum', 'base-sepolia').
    NETWORK = "base"

    try:
        async with CdpClient() as cdp:
            print(f"\n--- Fetching Balances for Account: {ACCOUNT_NAME} on {NETWORK} ---")
            
            # 1. Retrieve the specific EVM Account
            account = await cdp.evm.get_or_create_account(name=ACCOUNT_NAME)
            print(f"✅ Found Account Address: {account.address}")

            # 2. Call list_token_balances on the account object
            balances_response = await account.list_token_balances(network=NETWORK)
            
            print("\n💰 Token Balances:")
            if balances_response and balances_response.balances:
                for balance_info in balances_response.balances:
                    amount = int(balance_info.amount.amount)
                    decimals = balance_info.amount.decimals
                    symbol = balance_info.token.symbol
                    
                    # Convert the raw amount (wei/smallest unit) to a standard amount
                    standard_amount = amount / (10**decimals)
                    
                    print(f"  - {symbol}: {standard_amount:f}")
            else:
                print(f"ℹ️ No non-zero token balances found for {account.address} on {NETWORK}.")

    except Exception as e:
        print(f"❌ Error listing balances: {e}")

# --- Main Execution Flow ---
async def main():
    # You can keep the original cdp client test if you like
    # cdp = CdpClient()
    # await cdp.close()
    
    # Call the new function
    await list_evm_balances()

# The original execution line remains the same
if __name__ == '__main__':
    asyncio.run(main())
