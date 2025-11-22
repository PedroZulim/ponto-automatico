from datetime import datetime
from typing import List, Tuple

import pandas as pd
import requests


class Feriados:
    def __init__(self, ano: int | None = None) -> None:
        self.ano = ano or datetime.now().year
        self._cache_datas: List[str] | None = None

    def _carregar_feriados(self) -> None:
        if self._cache_datas is not None:
            return

        url = f"https://brasilapi.com.br/api/feriados/v1/{self.ano}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            self._cache_datas = df["date"].to_list()
        else:
            # Se der erro na API, considera sem feriados (melhor que quebrar o script)
            print(f"Não foi possível buscar feriados. Status: {response.status_code}")
            self._cache_datas = []

    def get_feriados(self) -> List[str]:
        self._carregar_feriados()
        return self._cache_datas or []

    def is_feriado_hoje(self) -> bool:
        hoje_str = datetime.today().strftime("%Y-%m-%d")
        return hoje_str in self.get_feriados()

    def can_mark_today(self) -> Tuple[bool, str]:
        """
        Retorna (pode_bater, mensagem).
        Centraliza a lógica de dia útil + feriado.
        """
        hoje_semana = datetime.today().weekday()  # 0 = segunda, 6 = domingo

        if not (0 <= hoje_semana <= 4):
            msg = "Hoje não é dia útil (sábado ou domingo), não vou bater ponto."
            print(msg)
            return False, msg

        if self.is_feriado_hoje():
            msg = "Hoje é feriado, não vou bater ponto."
            print(msg)
            return False, msg

        return True, "Dia útil e não é feriado. Pode bater ponto."
