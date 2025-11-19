from datetime import datetime

import pandas as pd
import requests


class Feriados:
    def __init__(self):
        self.ano = datetime.now().year

    def get_feriados(self):
        url = f"https://brasilapi.com.br/api/feriados/v1/{self.ano}"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame(response.json())['date'].to_list()
