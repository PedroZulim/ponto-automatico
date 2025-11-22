from datetime import datetime
import os
from typing import Tuple

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from Feriados import Feriados


class PontoBot:
    def __init__(self, feriados: Feriados | None = None, headless: bool = True) -> None:
        self.feriados = feriados or Feriados()
        self.headless = headless

        # Carrega .env localmente (no GitHub usa secrets)
        load_dotenv()

        self.username = os.getenv("APDATA_USERNAME")
        self.password = os.getenv("APDATA_PASSWORD")

        if not self.username or not self.password:
            print(
                "ATENÇÃO: APDATA_USERNAME e/ou APDATA_PASSWORD não configurados. "
                "Bater ponto irá falhar."
            )

    def _build_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=chrome_options)
        print("Navegador aberto!")
        return driver

    def bater_ponto(self, periodo: str | None = None) -> Tuple[str, str]:
        """
        Tenta bater ponto AGORA.
        Retorna (status, mensagem):

        status:
          - "Sucesso"
          - "Ignorado"
          - "Erro"
        """
        pode_bater, msg_validacao = self.feriados.can_mark_today()
        if not pode_bater:
            # Não tenta nem abrir navegador
            return "Ignorado", msg_validacao

        if not self.username or not self.password:
            return "Erro", (
                "Usuário/senha APDATA não encontrados nas variáveis de ambiente. "
                "Configure APDATA_USERNAME e APDATA_PASSWORD."
            )

        driver = self._build_driver()
        wait = WebDriverWait(driver, 30)  # espera até 30s pros elementos aparecerem

        try:
            driver.get("https://cliente.apdata.com.br/dicon/")
            print("Página carregada!")

            # Carregamento inicial da página
            # (tempo extra para certeza em ambientes mais lentos)
            from time import sleep
            sleep(4)

            # espera o botão inicial ficar clicável
            btn = wait.until(
                ec.presence_of_element_located((By.ID, "button-1021"))
            )
            btn.send_keys(Keys.RETURN)

            sleep(2)

            # espera os campos de usuário e senha aparecerem
            usuario = wait.until(
                ec.presence_of_element_located((By.NAME, "userName_relogio_8001"))
            )
            senha = wait.until(
                ec.presence_of_element_located((By.NAME, "password_relogio_8001"))
            )
            bater = wait.until(
                ec.presence_of_element_located((By.ID, "ext-142"))
            )

            print("Preenchendo credenciais e batendo ponto...")
            usuario.send_keys(self.username)
            senha.send_keys(self.password)
            bater.send_keys(Keys.RETURN)

            print("Ponto enviado, aguardando confirmação...")
            resultado = wait.until(
                ec.presence_of_element_located((By.ID, "ext-144"))
            )

            from time import sleep as tsleep
            tsleep(2)

            texto_resultado = resultado.text
            print("Resultado da batida de ponto:")
            print(texto_resultado)

            periodo_label = periodo or "Ponto"
            msg = (
                f"{periodo_label} batido com sucesso em "
                f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}.\n\n"
                f"Mensagem do sistema:\n{texto_resultado}"
            )
            return "Sucesso", msg

        except Exception as e:
            # loga erro bonitinho pra debug (incluindo nos Actions)
            print(f"ERRO AO BATER PONTO: {e}")
            msg = f"Erro ao bater ponto em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}"
            return "Erro", msg

        finally:
            driver.quit()
            print("Fechando navegador...")
