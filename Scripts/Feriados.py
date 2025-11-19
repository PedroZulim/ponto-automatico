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

    def can_mark(self):
        # Segunda (0) até sexta (4)
        hoje = datetime.today().weekday()
        if not (0 <= hoje <= 4):
            print("Hoje não é dia útil, não vou bater ponto.")
            return False
        elif self.get_feriados().__contains__(datetime.today().strftime('%Y-%m-%d')):
            print("Hoje é feriado, não vou bater ponto.")
            return False
        return True
