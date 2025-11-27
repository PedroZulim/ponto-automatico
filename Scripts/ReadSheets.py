import pandas as pd

def carregar_feriados_municipais() -> None:
    municipal_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "14-6PkC3XyFaSXk7WcZzsum0uBevVQfp1h063dFEOffE/export?format=csv"
    )
    try:
        df = pd.read_csv(municipal_csv_url)
        print(df.head())
    except Exception as exc:
        print(f"Erro ao carregar feriados municipais do Google Sheets: {exc}")
        return

carregar_feriados_municipais()