import pandas as pd
import os 
from datetime import datetime


##### GETTING RIGHT DIRECTORY PREFIX FOR I/O OPERATIONS #######
def get_dir_prefix(type: str, filename) -> str:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    if type == "source":
        dir_prefix = os.path.join(script_directory, "../data/csv/raw/")
    elif type == "target":
        dir_prefix = os.path.join(script_directory, f"../../evidence_project/sources/{filename}/")
    return dir_prefix


############## DATA PROCESSING CLASS #############

class DataProcessor:
    def __init__(self, source_dir_prefix, target_dir_prefix):
        self.source_dir_prefix = source_dir_prefix
        self.target_dir_prefix = target_dir_prefix

    # Helper function for changing names to a more human format eth-ethereum -> symbol = ETH, new_coin_name = Ethereum 
    @staticmethod
    def transform_coin_name_and_add_symbol(coin_name: str): #coin_name example from Coinpaprika API request -> eth-ethereum
        coin_name_parts = coin_name.split('-')
        symbol = coin_name_parts[0].upper()
        new_coin_name = ' '.join(coin_name_parts[1:]).title()
        return symbol, new_coin_name


    @staticmethod
    def transform_exchange_name(exchange_name: str) -> str:
        exchange_name_parts = exchange_name.split('-')
        new_exchange_name = ' '.join(exchange_name_parts).title()
        return new_exchange_name


    @staticmethod
    def convert_ms_timestamp_s(timestamp_in_ms):
        timestamp = timestamp_in_ms / 1000
        return timestamp


    @staticmethod
    def wei_to_gwei(wei):
        return wei / 10**9


    @staticmethod
    def btc_to_satoshi(btc_amount):
        satoshi_amount = btc_amount * 100000000
        return satoshi_amount
    

    def transform_assets_and_returns_df(self) -> pd.DataFrame:
        source_file = os.path.join(self.source_dir_prefix, "assets_and_returns_mo.csv")
        target_file = os.path.join(self.target_dir_prefix, "coins_and_returns.csv")

        coins_df = pd.read_csv(source_file)
        coins_df[['symbol', 'new_coin_name']] = coins_df['coin_name'].apply(lambda x: pd.Series(self.transform_coin_name_and_add_symbol(x)))

        list_of_copies = ['WBTC', 'BTCB', 'STETH', 'WETH', 'RETH', 'WPLS', 'WBNB', 'CBETH', 'STSOL', 'SAVAX']
        filtered_df = coins_df[~coins_df['symbol'].isin(list_of_copies)]

        filtered_df.to_csv(target_file, index=False)


    def create_blockchain_tx_vol_data_table(self):
        source_file = os.path.join(self.source_dir_prefix, "3345629.csv")
        target_file = os.path.join(self.target_dir_prefix, "blockchain_tx_vol_data.csv")

        blockchains_volume_df = pd.read_csv(source_file)
        blockchains_volume_df['total_volume'] = blockchains_volume_df['total_volume'].round(0)
        blockchains_volume_df['month'] = pd.to_datetime(blockchains_volume_df['month']).dt.strftime('%Y-%m-%d')
        blockchains_volume_df['blockchain'] = blockchains_volume_df['blockchain'].replace({'avalanche_c': 'avalanche'})

        blockchains_volume_df.to_csv(target_file, index=False)


    def create_active_addresses_data_table(self):
        active_wallets_files = [3367836, 3367876, 3367854, 3367866, 3367870, 3367874, 3367876, 3367850, 3367848] #file names / query IDs for dune endpoints returning num of active wallets
        active_addresses_data = []    

        for file in active_wallets_files:
            active_addresses_df = pd.read_csv(f"{self.source_dir_prefix}{file}.csv")
            address_count = active_addresses_df['unique_address_count'][0]
            name = active_addresses_df['name'][0]
            active_addresses_data.append((name, address_count))

        active_addresses_df = pd.DataFrame(active_addresses_data, columns=['name', 'active_addresses'])
        active_addresses_df.to_csv(f'{self.target_dir_prefix}active_addresses.csv', index=False)


    def transform_and_save_eth_data_table(self):
        gas_data_df = pd.read_csv(f'{self.source_dir_prefix}3367146.csv')
        gas_data_df['avg_daily_gas_price'] = gas_data_df['avg_daily_gas_price'].map(self.wei_to_gwei).round(2)
        gas_data_df['fee'] = (gas_data_df['avg_gas_used']*gas_data_df['avg_daily_gas_price']).round() # calculates avg transaction fee in GWEI

        eth_data_df = pd.read_csv(f'{self.source_dir_prefix}eth_data.csv')
        eth_data_df['date'] = pd.to_datetime(eth_data_df['time_open']).dt.strftime('%Y-%m-%d')
        eth_data_df['fee'] = gas_data_df['fee']
        eth_data_df = eth_data_df.drop(columns=["time_open", "time_close", "high", "low"])
        eth_data_df['open'] = eth_data_df['open'].round(2)
        eth_data_df['close'] = eth_data_df['close'].round(2)

        eth_data_df.to_csv(f"{self.target_dir_prefix}eth_data.csv", index=False)


    def transform_and_save_btc_data_table(self):
        fee_df = pd.read_csv(f'{self.source_dir_prefix}3363927.csv')
        fee_df['fee'] = fee_df['fee'].map(self.btc_to_satoshi).round(0) 

        btc_data_df = pd.read_csv(f'{self.source_dir_prefix}btc_data.csv')
        btc_data_df['date'] = pd.to_datetime(btc_data_df['time_open']).dt.strftime('%Y-%m-%d')
        btc_data_df['fee'] = fee_df['fee']
        btc_data_df = btc_data_df.drop(columns=["time_open", "time_close", "high", "low"])
        btc_data_df['open'] = btc_data_df['open'].round(2)
        btc_data_df['close'] = btc_data_df['close'].round(2)

        btc_data_df.to_csv(f"{self.target_dir_prefix}btc_data.csv", index=False)


    def transform_liquidity_data_tables(self, month_start: datetime.date, month_end: datetime.date):
        month_start_dt = datetime.combine(month_start, datetime.min.time())
        month_end_dt = datetime.combine(month_end, datetime.max.time())

        month_start_ts = month_start_dt.timestamp()
        month_end_ts = month_end_dt.timestamp()

        btc_liquidity_df = pd.read_csv(f"{self.source_dir_prefix}btc_liq_data.csv")
        eth_liquidity_df = pd.read_csv(f"{self.source_dir_prefix}eth_liq_data.csv")

        btc_liquidity_df['timestamp'] = btc_liquidity_df['timestamp'].map(self.convert_ms_timestamp_s)
        eth_liquidity_df['timestamp'] = eth_liquidity_df['timestamp'].map(self.convert_ms_timestamp_s)

        btc_liquidity_df_filtered = btc_liquidity_df[(btc_liquidity_df['timestamp'] >= month_start_ts) & (btc_liquidity_df['timestamp'] <= month_end_ts)].copy()
        eth_liquidity_df_filtered = eth_liquidity_df[(eth_liquidity_df['timestamp'] >= month_start_ts) & (eth_liquidity_df['timestamp'] <= month_end_ts)].copy()

        btc_liquidity_df_filtered.loc[:, 'timestamp'] = pd.to_datetime(btc_liquidity_df_filtered['timestamp'], unit='s')
        eth_liquidity_df_filtered.loc[:, 'timestamp'] = pd.to_datetime(eth_liquidity_df_filtered['timestamp'], unit='s')

        btc_liquidity_df_filtered.rename(columns={'timestamp':'time'}, inplace=True)
        eth_liquidity_df_filtered.rename(columns={'timestamp':'time'}, inplace=True)

        btc_liquidity_df_filtered.to_csv(f"{self.target_dir_prefix}btc_liquidity_data.csv", index=False)
        eth_liquidity_df_filtered.to_csv(f"{self.target_dir_prefix}eth_liquidity_data.csv", index=False)


    def transform_commits_data(self):
        commits_df = pd.read_csv(f"{self.source_dir_prefix}commits_data.csv")
        commits_df[['symbol', 'coin_name']] = commits_df['coin_id'].apply(lambda x: pd.Series(self.transform_coin_name_and_add_symbol(x)))
        commits_df = commits_df.drop(columns=["coin_id"])
        commits_df.to_csv(f"{self.target_dir_prefix}project_commits_data.csv", index=False)


    def transform_exchanges_data(self, source_file_name: str, target_file_name: str):
        exchanges_data = pd.read_csv(f"{self.source_dir_prefix}{source_file_name}")
        exchanges_data['name'] = exchanges_data['url_name'].apply(lambda x: pd.Series(self.transform_exchange_name(x)))
        exchanges_data.to_csv(f"{self.target_dir_prefix}{target_file_name}", index=False)

