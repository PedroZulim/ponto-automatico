import json
import os
from datetime import time
from pathlib import Path
from typing import Dict, Any


class Config:
    """Classe para carregar e gerenciar as configurações do sistema."""

    def __init__(self, config_path: str | None = None) -> None:
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            config_path: Caminho para o arquivo config.json.
                        Se None, procura na raiz do projeto.
        """
        if config_path is None:
            # Tenta encontrar config.json na raiz do projeto (um nível acima de Scripts/)
            script_dir = Path(__file__).parent
            config_path = script_dir.parent / "config.json"
        
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Carrega o arquivo de configuração JSON."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: {self.config_path}\n"
                "Certifique-se de que o arquivo config.json existe na raiz do projeto."
            )
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Erro ao ler o arquivo de configuração: {e}\n"
                "Verifique se o JSON está formatado corretamente."
            )
        
        self._validate_config()

    def _validate_config(self) -> None:
        """Valida se todas as configurações necessárias estão presentes."""
        required_keys = ["horarios", "sistema"]
        for key in required_keys:
            if key not in self._config:
                raise ValueError(f"Configuração obrigatória '{key}' não encontrada em config.json")
        
        # Valida estrutura de horários
        horarios = self._config["horarios"]
        for periodo in ["entrada", "saida"]:
            if periodo not in horarios:
                raise ValueError(f"Configuração de '{periodo}' não encontrada em horarios")
            
            periodo_config = horarios[periodo]
            required_periodo_keys = ["horario_exato", "janela_inicio", "janela_limite"]
            for key in required_periodo_keys:
                if key not in periodo_config:
                    raise ValueError(
                        f"Configuração '{key}' não encontrada em horarios.{periodo}"
                    )

    def _parse_time(self, time_str: str) -> time:
        """Converte string HH:MM em objeto time."""
        try:
            h, m = map(int, time_str.split(":"))
            return time(h, m)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Formato de horário inválido: {time_str}. Use HH:MM") from e

    # Propriedades para horários de entrada
    @property
    def entrada_horario_exato(self) -> str:
        """Horário exato de entrada (formato HH:MM)."""
        return self._config["horarios"]["entrada"]["horario_exato"]

    @property
    def entrada_janela_inicio(self) -> time:
        """Início da janela de entrada."""
        return self._parse_time(self._config["horarios"]["entrada"]["janela_inicio"])

    @property
    def entrada_janela_limite(self) -> time:
        """Limite da janela de entrada."""
        return self._parse_time(self._config["horarios"]["entrada"]["janela_limite"])

    # Propriedades para horários de saída
    @property
    def saida_horario_exato(self) -> str:
        """Horário exato de saída (formato HH:MM)."""
        return self._config["horarios"]["saida"]["horario_exato"]

    @property
    def saida_janela_inicio(self) -> time:
        """Início da janela de saída."""
        return self._parse_time(self._config["horarios"]["saida"]["janela_inicio"])

    @property
    def saida_janela_limite(self) -> time:
        """Limite da janela de saída."""
        return self._parse_time(self._config["horarios"]["saida"]["janela_limite"])

    # Propriedades do sistema
    @property
    def timezone(self) -> str:
        """Timezone do sistema."""
        return self._config["sistema"]["timezone"]

    @property
    def intervalo_verificacao(self) -> int:
        """Intervalo de verificação em segundos."""
        return self._config["sistema"]["intervalo_verificacao_segundos"]

    @property
    def modo_headless(self) -> bool:
        """Se o navegador deve rodar em modo headless."""
        return self._config["sistema"]["modo_headless"]

    def reload(self) -> None:
        """Recarrega o arquivo de configuração."""
        self._load_config()

    def get_raw_config(self) -> Dict[str, Any]:
        """Retorna o dicionário completo de configurações."""
        return self._config.copy()
