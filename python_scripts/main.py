from api_calls.coinpaprika_api import CoinpaprikaAPI 
from api_calls.dune_api import DuneAPI
import data_processing.proccess_data as dp
from utils.helpers import get_last_month_info
import utils.config as config


coinpaprika_api = CoinpaprikaAPI(config.COINPAPRIKA_APIKEY)
dune_api = DuneAPI(config.DUNE_APIKEY)


if __name__ == "__main__":

    last_month = get_last_month_info()


    # Downloading and saving data
    coinpaprika_api.get_monthly_etc_btc_data(last_month)
    coinpaprika_api.get_assets_month_change(month_info=last_month)
    coinpaprika_api.get_mo_commits_df(month_info=last_month, top_x_coins=100)
    coinpaprika_api.get_liquidity_data()
    coinpaprika_api.get_exchanges_data(config.DEX_EXCHANGES, config.DEX_EXCHANGE_SRC_FILE_NAME)
    coinpaprika_api.get_exchanges_data(config.CEX_EXCHANGES, config.CEX_EXCHANGE_SRC_FILE_NAME)
    
    for query_id in config.DUNE_API_QUERIES.values():
        dune_api.api_call(query_id=query_id)


    # Data processing
    dp.transform_assets_and_returns_df()
    dp.create_blockchain_tx_vol_data_table()
    dp.create_active_addresses_data_table()
    dp.transform_and_save_eth_data_table()
    dp.transform_and_save_btc_data_table()        
    dp.transform_liquidity_data_tables(last_month.first_day, last_month.last_day)
    dp.transform_commits_data()
    dp.transform_exchanges_data(config.CEX_EXCHANGE_SRC_FILE_NAME, config.CEX_EXCHANGE_TARGET_FILE_NAME)
    dp.transform_exchanges_data(config.DEX_EXCHANGE_SRC_FILE_NAME, config.DEX_EXCHANGE_TARGET_FILE_NAME)
    print("Success! All data saved, transformed and ready to use.")