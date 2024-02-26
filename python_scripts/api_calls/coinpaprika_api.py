
import pandas as pd
import httpx
from typing import Any, Dict, List
from utils.helpers import MonthInfo, get_last_month_info, ensure_directory_exists
import os
from datetime import datetime
import time


class CoinpaprikaAPI():
    def __init__(self, api_key: str):   
        self.api_key = api_key
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.data_directory = self.get_saving_directory()
        self.btc_id = "btc-bitcoin"
        self.eth_id = "eth-ethereum"

    
    def get_saving_directory(self) -> str:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        dir_path = os.path.join(script_directory, "../../data/csv/raw")
        ensure_directory_exists(dir_path)
        return dir_path
    
    
    def get_list_of_coins(self) -> Dict[str, Any]:
        with httpx.Client() as client:
            response = client.get('https://api-pro.coinpaprika.com/v1/coins', headers=self.headers)
            response.raise_for_status()
            return response.json()

    
    def get_monthly_coin_data(self, month: MonthInfo, coin_id: str) -> pd.DataFrame:
        try:
            f_day = month.first_day
            l_day = month.last_day
        except Exception as e:
            print(f"ERROR in get_monthly_coin_data: {e}")
            return None

        with httpx.Client() as client:
            response = client.get(f'https://api-pro.coinpaprika.com/v1/coins/{coin_id}/ohlcv/historical?start={f_day}&end={l_day}', headers=self.headers)
            response.raise_for_status()
            monthly_coin_data = pd.DataFrame(response.json())
            return monthly_coin_data

    
    def get_monthly_etc_btc_data(self, month: MonthInfo):
        try:
            f_day = month.first_day
            l_day = month.last_day
            print(self.api_key)

            with httpx.Client() as client:
                btc_response = client.get(f'https://api-pro.coinpaprika.com/v1/coins/{self.btc_id}/ohlcv/historical?start={f_day}&end={l_day}', headers=self.headers)
                eth_response = client.get(f'https://api-pro.coinpaprika.com/v1/coins/{self.eth_id}/ohlcv/historical?start={f_day}&end={l_day}', headers=self.headers)

                if btc_response.status_code == 200 and eth_response.status_code == 200:
                    btc_data_df = pd.DataFrame(btc_response.json())
                    eth_data_df = pd.DataFrame(eth_response.json())

                    btc_data_df.to_csv(os.path.join(self.data_directory, 'btc_data.csv'), index=False)
                    eth_data_df.to_csv(os.path.join(self.data_directory, 'eth_data.csv'), index=False)
                else:
                    print(f"Failed to fetch data: BTC status {btc_response.status_code}, ETH status {eth_response.status_code}")
                    return None

        except httpx.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    def calc_monthly_change(self, asset_data: pd.DataFrame) -> float:
        try:
            open_price = asset_data.iloc[1]['open']
            close_price = asset_data.iloc[-1]['close']
            percentage_change = ((close_price - open_price) / abs(open_price)) * 100
            return round(percentage_change, 2)
        except Exception as e:
            print(f"ERROR in calc_monthly_change: {e}")
            return None


    def get_assets_month_change(self, month_info: MonthInfo, top_x_coins: int = 200) -> pd.DataFrame:
        assets = self.get_list_of_coins()
        all_assets_and_returns = []
        try:
            with httpx.Client() as client:
                tasks = []
                coin_names = []
                for i, coin in enumerate(assets):
                    if i == top_x_coins:
                        break
                    coin_id = coin['id']
                    coin_names.append(coin_id)
                    tasks.append(self.get_monthly_coin_data(month=month_info, coin_id=coin_id))

                coin_data_responses = [task for task in tasks]

                for coin_data_df, coin_name in zip(coin_data_responses, coin_names):
                    if coin_data_df is not None:
                        month_change = self.calc_monthly_change(coin_data_df)
                        all_assets_and_returns.append((month_info.first_day, coin_name, month_change))

                all_assets_and_returns_df = pd.DataFrame(all_assets_and_returns, columns=["month", "coin_name", "month_change"])
                print(all_assets_and_returns)
                print(all_assets_and_returns_df)
                all_assets_and_returns_df.to_csv(os.path.join(self.data_directory, "assets_and_returns_mo.csv"), index=False)
                return all_assets_and_returns_df

        except Exception as e:
            print(f"ERROR in assets_month_change: {e}")
            return 0


    def get_project_mo_commit_data(self, coin_id: str, month: MonthInfo) -> int:
        month_check = month.first_day.strftime('%Y-%m')

        with httpx.Client() as client:
            response = client.get(f'https://api-frontend.coinpaprika.com/coin/{coin_id}/github-stats?monitoring=1', headers=self.headers)
            try:
                data = response.json()
            except:
                return 0

        num_of_commits = 0

        for i in range(len(data) - 1, 0, -1):
            date_str = data[i]['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_formatted = date_obj.strftime('%Y-%m')

            if date_formatted < month_check:
                break

            if date_formatted == month_check:
                num_of_commits += int(data[i]["commits"])

        time.sleep(1)

        return num_of_commits


    def get_mo_commits_df(self, month_info: MonthInfo, top_x_coins: int = 30):
        coins = self.get_list_of_coins()
        month_info = get_last_month_info()
        projects_and_commits_number = []

        with httpx.Client() as client:
            tasks = []
            coin_names = []
            for i, coin in enumerate(coins):
                if i == top_x_coins:
                    break
                coin_id = coin['id']
                coin_names.append(coin_id)
                tasks.append(self.get_project_mo_commit_data(coin_id=coin_id, month=month_info))

            coin_data_responses = [task for task in tasks]

            for commit_number, coin_name in zip(coin_data_responses, coin_names):
                if commit_number is not None:
                    projects_and_commits_number.append((month_info.first_day, coin_name, commit_number))

        projects_and_commits_number_df = pd.DataFrame(projects_and_commits_number)
        projects_and_commits_number_df.columns = ["month", "coin_id", "commits"]
        projects_and_commits_number_df.to_csv(os.path.join(self.data_directory, 'commits_data.csv'), index=False)


    def get_liquidity_data(self, time_period: str = "1q", base_only: int = 1):
        with httpx.Client() as client:
            btc_response = client.get(f'https://graphsv2.coinpaprika.com/currency/market_depth/{self.btc_id}/{time_period}/?quote=USD&span=10&baseOnly={base_only}&monitoring=1', headers=self.headers)
            eth_response = client.get(f'https://graphsv2.coinpaprika.com/currency/market_depth/{self.eth_id}/{time_period}/?quote=USD&span=10&baseOnly={base_only}&monitoring=1', headers=self.headers)

            if btc_response.status_code == 200 and eth_response.status_code == 200:
                # Creating BTC liquidity dataframe
                btc_asks = btc_response.json()[0]['asks']
                btc_bids = btc_response.json()[0]['bids']
                btc_combined_orders = btc_response.json()[0]['combined_orders']

                btc_asks_df = pd.DataFrame(btc_asks, columns=['timestamp', 'asks'])
                btc_bids_df = pd.DataFrame(btc_bids, columns=['timestamp', 'bids'])
                btc_combined_orders_df = pd.DataFrame(btc_combined_orders, columns=['timestamp', 'combined_orders'])

                btc_result_df = pd.merge(btc_asks_df, btc_bids_df, on='timestamp')
                btc_result_df = pd.merge(btc_result_df, btc_combined_orders_df, on='timestamp')

                btc_result_df.to_csv(os.path.join(self.data_directory, 'btc_liq_data.csv'), index=False)

                # Creating ETH liquidity dataframe
                eth_asks = eth_response.json()[0]['asks']
                eth_bids = eth_response.json()[0]['bids']
                eth_combined_orders = eth_response.json()[0]['combined_orders']

                eth_asks_df = pd.DataFrame(eth_asks, columns=['timestamp', 'asks'])
                eth_bids_df = pd.DataFrame(eth_bids, columns=['timestamp', 'bids'])
                eth_combined_orders_df = pd.DataFrame(eth_combined_orders, columns=['timestamp', 'combined_orders'])

                eth_result_df = pd.merge(eth_asks_df, eth_bids_df, on='timestamp')
                eth_result_df = pd.merge(eth_result_df, eth_combined_orders_df, on='timestamp')

                eth_result_df.to_csv(os.path.join(self.data_directory, 'eth_liq_data.csv'), index=False)


    def get_exchange_data(self, exchange_id: str) -> List:
        with httpx.Client() as client:
            response = client.get(f"https://api.coinpaprika.com/v1/exchanges/{exchange_id}", headers=self.headers)
            data = response.json()
            quote_data = data['quotes']['USD']
            vol_last_30d = int(quote_data['adjusted_volume_30d'])
            return [exchange_id, vol_last_30d]
        

    def get_exchanges_data(self, exchanges: List[str], filename: str):
        exchanges_data = []
        for i in exchanges:
            exchange_data = self.get_exchange_data(i)
            exchanges_data.append(exchange_data)

        exchanges_data_df = pd.DataFrame(exchanges_data)
        exchanges_data_df.columns = ["url_name", "vol_30_day_usd"]
        exchanges_data_df.to_csv(os.path.join(self.data_directory, f'{filename}'), index=False)
