import sys
from pathlib import Path

# Adiciona o diretório Scripts ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

from Config import Config
from Feriados import Feriados


def main() -> None:
    # Carrega configurações
    config = Config()
    
    feriados = Feriados(timezone=config.timezone)
    print(feriados.get_feriados())  # Carrega os feriados para cache



if __name__ == "__main__":
    main()
