from api_calls.coinpaprika_api import CoinpaprikaAPI 
from api_calls.dune_api import DuneAPI
import data_processing.proccess_data as dp
from utils.helpers import get_last_month_info, create_env_value, replace_placeholders_in_md_template, add_data_connection_yaml_file
import utils.config as config
import os


coinpaprika_api = CoinpaprikaAPI(config.COINPAPRIKA_APIKEY)
dune_api = DuneAPI(config.DUNE_APIKEY)


if __name__ == "__main__":

    last_month = get_last_month_info()
    NEW_MONTH_ENV = create_env_value(last_month)

    source_dir_prefix = dp.get_dir_prefix("source", NEW_MONTH_ENV)
    target_dir_prefix = dp.get_dir_prefix("target", NEW_MONTH_ENV)
    
    if not os.path.exists(source_dir_prefix):
        os.makedirs(source_dir_prefix)
 
    if not os.path.exists(target_dir_prefix):
        os.makedirs(target_dir_prefix)

    # Set environment value used in the file creation and edition
    # os.environ["NEW_MONTH_NAME"] = NEW_MONTH_ENV
    replace_placeholders_in_md_template(NEW_MONTH_ENV)
    add_data_connection_yaml_file(NEW_MONTH_ENV)


    # # Downloading and saving data
    coinpaprika_api.get_monthly_etc_btc_data(last_month)
    coinpaprika_api.get_assets_month_change(month_info=last_month)
    coinpaprika_api.get_mo_commits_df(month_info=last_month, top_x_coins=100)
    coinpaprika_api.get_liquidity_data()
    coinpaprika_api.get_exchanges_data(config.DEX_EXCHANGES, config.DEX_EXCHANGE_SRC_FILE_NAME)
    coinpaprika_api.get_exchanges_data(config.CEX_EXCHANGES, config.CEX_EXCHANGE_SRC_FILE_NAME)
    
    for query_id in config.DUNE_API_QUERIES.values():
        dune_api.api_call(query_id=query_id)


    # # Data processing
    data_processor = dp.DataProcessor(source_dir_prefix, target_dir_prefix)
    data_processor.transform_assets_and_returns_df()
    data_processor.create_blockchain_tx_vol_data_table()
    data_processor.create_active_addresses_data_table()
    data_processor.transform_and_save_eth_data_table()
    data_processor.transform_and_save_btc_data_table()        
    data_processor.transform_liquidity_data_tables(last_month.first_day, last_month.last_day)
    data_processor.transform_commits_data()
    data_processor.transform_exchanges_data(config.CEX_EXCHANGE_SRC_FILE_NAME, config.CEX_EXCHANGE_TARGET_FILE_NAME)
    data_processor.transform_exchanges_data(config.DEX_EXCHANGE_SRC_FILE_NAME, config.DEX_EXCHANGE_TARGET_FILE_NAME)
    print("Success! All data saved, transformed and ready to use.")