from datetime import datetime
from typing import Tuple
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
        self.timezone = timezone
        self.ano = ano or datetime.now(tz=ZoneInfo(self.timezone)).year

        self.municipal_csv_url = municipal_csv_url
        self.municipal_date_column = municipal_date_column

        self._df_datas_nacionais: pd.DataFrame | None = None
        self._df_datas_municipais: pd.DataFrame | None = None

    def _carregar_feriados_nacionais(self) -> None:
        if self._df_datas_nacionais is not None:
            return

        url = f"https://brasilapi.com.br/api/feriados/v1/{self.ano}"
        try:
            response = requests.get(url, timeout=10)
        except Exception as exc:
            print(f"Erro ao buscar feriados nacionais: {exc}")
            self._df_datas_nacionais = pd.DataFrame(columns=["date", "name", "type"])
            return

        if response.status_code == 200:
            self._df_datas_nacionais = pd.DataFrame(response.json())
        else:
            print(f"Não foi possível buscar feriados. Status: {response.status_code}")
            self._df_datas_nacionais = pd.DataFrame(columns=["date", "name", "type"])

    def _carregar_feriados_municipais(self) -> None:
        if self._df_datas_municipais is not None:
            return

        if not self.municipal_csv_url:
            self._df_datas_municipais = pd.DataFrame(columns=["date", "name", "type"])
            return

        try:
            df = pd.read_csv(
                self.municipal_csv_url,
                on_bad_lines="skip",
                sep=",",
                encoding="utf-8",
                skipinitialspace=True,
            )
        except Exception as exc:
            print(f"Erro ao carregar feriados municipais do Google Sheets: {exc}")
            self._df_datas_municipais = pd.DataFrame(columns=["date", "name", "type"])
            return

        if self.municipal_date_column not in df.columns:
            print(f"A coluna '{self.municipal_date_column}' não existe na planilha de feriados municipais.")
            self._df_datas_municipais = pd.DataFrame(columns=["date", "name", "type"])
            return

        if "year" in df.columns:
            df = df[df["year"] == self.ano]

        self._df_datas_municipais = df

    def get_feriados(self) -> pd.DataFrame:
        self._carregar_feriados_nacionais()
        self._carregar_feriados_municipais()
        return pd.concat([self._df_datas_nacionais, self._df_datas_municipais], ignore_index=True)

    def can_mark_today(self) -> Tuple[bool, str]:
        hoje = datetime.now(tz=ZoneInfo(self.timezone))
        hoje_semana = hoje.weekday()  # 0=seg, 6=dom

        if hoje_semana > 4:
            dia = "sábado" if hoje_semana == 5 else "domingo"
            msg = f"Hoje não é dia útil {dia}, não vou bater ponto."
            print(msg)
            return False, msg

        hoje_str = hoje.strftime("%Y-%m-%d")
        feriados = self.get_feriados()

        if hoje_str in feriados["date"].astype(str).to_list():
            tipos = feriados.loc[feriados["date"].astype(str) == hoje_str, "type"]
            name = feriados.loc[feriados["date"].astype(str) == hoje_str, "name"].iloc[0].strip()
            tipo_txt = tipos.iloc[0] if len(tipos) else "feriado"
            msg = f"Hoje é feriado {tipo_txt} ({name}), não vou bater ponto."
            print(msg)
            return False, msg

        return True, "Dia útil e não é feriado. Pode bater ponto."
