import os


COINPAPRIKA_APIKEY = os.environ.get("COINPAPRIKA_APIKEY")
DUNE_APIKEY  = os.environ.get("DUNE_APIKEY")

DATABASE_PATH = os.environ.get("DATABASE_PATH", "/path/to/your/database.db")

DUNE_API_QUERIES = {
    "blockchains_vol": 3345629, # Total volume monthly
    "projects_vol": 3345651, # Total volume monthly 
    "eth_gas_info": 3367146, # Average daily gas price + average gas consumption for transactions on each day in the last month
    "btc_fee": 3363927, # Average daily fee for transactions on each day in the last month
    "eth_active_addresses": 3367836,   # Number of Ethereum active addresses in last month
    "btc_active_addresses": 3367848,   # Number of Bitcoin active addresses in last month
    "avax_active_addresses": 3367850,  # Number of Avalanche active addresses in last month
    "bnb_active_addresses": 3367854,   # Number of active addresses on Binance Smart Chain in last month
    "base_active_addresses": 3367870,  # Number of active addresses on Base in last month
    "matic_active_addresses": 3367866, # Number of active addresses on Polygon in last month
    "arb_active_addresses": 3367874,   # Number of active addresses on Arbitrum in last month
    "op_active_addresses": 3367876,    # Number of active addresses on Optimism in last month 
}   


CEX_EXCHANGES = ['binance', 'coinbase', 'bitforex', 'kraken', 'okx', 'kucoin', 'gateio', 'htx', 'bitfinex', 'bitstamp', 'p2b', 'digifinex',
'bitmart', 'whitebit', 'bitget', 'bitrue', 'lbank', 'deepcoin', 'toobit', 'xt']

DEX_EXCHANGES = ['uniswap-v3', 'uniswap-v2', 'curve-finance', 'pancakeswap-v3-bsc', 'pancakeswap-v2', 'uniswap-arbitrum', 'uniswap-polygon-network',
'uniswap-optimism', 'pancakeswap-v3-ethereum', 'trader-joe', 'trader-joe-v2-arbitrum', 'camelot-v3', 'camelot', 'balancer-v2', 'balancer']


DEX_EXCHANGE_SRC_FILE_NAME ='dex_exchanges_data.csv'
CEX_EXCHANGE_SRC_FILE_NAME ='cex_exchanges_data.csv'


DEX_EXCHANGE_TARGET_FILE_NAME ='dex_data.csv'
CEX_EXCHANGE_TARGET_FILE_NAME ='cex_data.csv'

