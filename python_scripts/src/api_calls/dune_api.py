from dune_client.client import DuneClient
from dune_client.query import QueryBase
from utils.helpers import ensure_directory_exists
import pandas as pd
import os 
import time


class DuneAPI:
    def __init__(self, api_key: str):
        self.dune_client = DuneClient(api_key=api_key)
        self.data_directory = self.get_saving_directory()


    def get_saving_directory(self) -> str:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        dir = os.path.join(script_directory, "../../data/csv/raw")
        ensure_directory_exists(dir)
        return dir


    def api_call(self, query_id: int, max_retries: int = 10, delay_s: int = 60) -> pd.DataFrame:
        
        for attempt in range(max_retries + 1):
            try:
                query = QueryBase(query_id=query_id)
                results_df = self.dune_client.run_query_dataframe(query)
                        
                csv_path = os.path.join(self.data_directory, f"{query_id}.csv")
                results_df.to_csv(csv_path, index=False)

                return results_df
            
            except Exception as e:
                print(f"Error while making Dune API call or saving it to .csv file: {e}")
                print(f"Error on attempt {attempt + 1}/{max_retries + 1}.")
                if attempt < max_retries:
                    print(f"Retrying in {delay_s} seconds...")
                    time.sleep(delay_s)
                    
                else:
                    print("Max retries reached. Giving up.")
                    return None
            
