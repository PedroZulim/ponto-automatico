from datetime import datetime
from typing import List, Tuple
from zoneinfo import ZoneInfo

import pandas as pd
import requests


class Feriados:
    def __init__(
        self,
        ano: int | None = None,
        timezone: str = "America/Sao_Paulo",
        municipal_csv_url: str | None = "https://docs.google.com/spreadsheets/d/14-6PkC3XyFaSXk7WcZzsum0uBevVQfp1h063dFEOffE/export?format=csv",
        municipal_date_column: str = "date",
    ) -> None:
        """
        :param ano: Ano de referência dos feriados. Se None, usa o ano atual.
        :param timezone: Timezone para cálculo de "hoje".
        :param municipal_csv_url: URL CSV público do Google Sheets com feriados municipais.
               Exemplo:
               https://docs.google.com/spreadsheets/d/ID/export?format=csv
        :param municipal_date_column: Nome da coluna da planilha que contém as datas
               dos feriados municipais.
        """
        self.timezone = timezone
        self.ano = ano or datetime.now(tz=ZoneInfo(self.timezone)).year

        # Configuração de feriados municipais
        self.municipal_csv_url = municipal_csv_url
        self.municipal_date_column = municipal_date_column

        # Cache interno
        self._cache_datas_nacionais: List[str] | None = None
        self._cache_datas_municipais: List[str] | None = None

    # ================== FERIADOS NACIONAIS / ESTADUAIS (API) ==================

    def _carregar_feriados_nacionais(self) -> None:
        if self._cache_datas_nacionais is not None:
            return

        url = f"https://brasilapi.com.br/api/feriados/v1/{self.ano}"
        try:
            response = requests.get(url, timeout=10)
        except Exception as exc:
            print(f"Erro ao buscar feriados nacionais: {exc}")
            self._cache_datas_nacionais = []
            return

        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            # A API já retorna "date" em formato YYYY-MM-DD
            self._cache_datas_nacionais = df["date"].to_list()
        else:
            print(f"Não foi possível buscar feriados. Status: {response.status_code}")
            self._cache_datas_nacionais = []

    # ================== FERIADOS MUNICIPAIS (GOOGLE SHEETS) ==================

    def _carregar_feriados_municipais(self) -> None:
        """
        Lê um CSV público (Google Sheets) com feriados municipais.

        Regras esperadas:
        - Há uma coluna com as datas (por padrão "date")
        - Formato aceito: YYYY-MM-DD ou DD/MM/YYYY
        - Opcionalmente, pode haver uma coluna "year" para filtrar pelo ano
        """
        if self._cache_datas_municipais is not None:
            return

        if not self.municipal_csv_url:
            # Se não foi configurada URL, não temos feriados municipais
            self._cache_datas_municipais = []
            return

        try:
            df = pd.read_csv(
                self.municipal_csv_url,
                on_bad_lines='skip',  # Pula linhas mal formatadas
                sep=',',  # Especifica o separador
                encoding='utf-8',  # Especifica a codificação
                skipinitialspace=True  # Remove espaços em branco extras
            )
        except Exception as exc:
            print(f"Erro ao carregar feriados municipais do Google Sheets: {exc}")
            self._cache_datas_municipais = []
            return

        if self.municipal_date_column not in df.columns:
            print(
                f"A coluna '{self.municipal_date_column}' não existe na planilha de feriados municipais."
            )
            self._cache_datas_municipais = []
            return

        # Se existir uma coluna 'year', filtra pelo ano atual (self.ano)
        if "year" in df.columns:
            df = df[df["year"] == self.ano]

        # Normaliza para string "YYYY-MM-DD"
        self._cache_datas_municipais = df["date"].to_list()

    # ================== INTERFACE PÚBLICA ==================

    def get_feriados(self) -> List[str]:
        """
        Retorna lista de datas (YYYY-MM-DD) de todos os feriados:
        - nacionais/estaduais (API)
        - municipais (Google Sheets, se configurado)
        """
        self._carregar_feriados_nacionais()
        self._carregar_feriados_municipais()

        datas_nacionais = self._cache_datas_nacionais or []
        datas_municipais = self._cache_datas_municipais or []

        # Une e remove duplicados
        todas = sorted(set(datas_nacionais + datas_municipais))
        return todas

    def is_feriado_hoje(self) -> bool:
        hoje_str = datetime.now(tz=ZoneInfo(self.timezone)).strftime("%Y-%m-%d")
        return hoje_str in self.get_feriados()

    def can_mark_today(self) -> Tuple[bool, str]:
        """
        Retorna (pode_bater, mensagem).
        Centraliza a lógica de dia útil + feriado (nacional + municipal).
        """
        hoje = datetime.now(tz=ZoneInfo(self.timezone))
        hoje_semana = hoje.weekday()  # 0 = segunda, 6 = domingo

        if not (0 <= hoje_semana <= 4):
            msg = "Hoje não é dia útil (sábado ou domingo), não vou bater ponto."
            print(msg)
            return False, msg

        if self.is_feriado_hoje():
            msg = "Hoje é feriado (nacional/estadual ou municipal), não vou bater ponto."
            print(msg)
            return False, msg

        return True, "Dia útil e não é feriado. Pode bater ponto."
