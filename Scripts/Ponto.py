from datetime import datetime
import os
from typing import Tuple
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from Feriados import Feriados
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time


class PontoBot:
    def __init__(
        self,
        feriados: Feriados | None = None,
        headless: bool = True,
        timezone: str = "America/Sao_Paulo",
    ) -> None:
        self.timezone = timezone
        self.feriados = feriados or Feriados(timezone=self.timezone)
        self.headless = headless

        # Carrega .env localmente (no GitHub usa secrets)
        load_dotenv()

        self.username = os.getenv("APDATA_USERNAME", "Teste")
        self.password = os.getenv("APDATA_PASSWORD", "Teste")

        if not self.username or not self.password:
            print(
                "ATENÇÃO: APDATA_USERNAME e/ou APDATA_PASSWORD não configurados. "
                "Bater ponto irá falhar."
            )

    def bater_ponto(self, periodo: str | None = None) -> Tuple[str, str]:
        """
        Tenta bater ponto AGORA usando Playwright.
        Retorna (status, mensagem):

        status:
          - "Sucesso"
          - "Ignorado"
          - "Erro"
        """

        # Verificação de feriados / finais de semana
        pode_bater, msg_validacao = self.feriados.can_mark_today()
        if not pode_bater:
            # Não tenta nem abrir navegador
            return "Ignorado", msg_validacao

        if not self.username or not self.password:
            return "Erro", (
                "Usuário/senha APDATA não encontrados nas variáveis de ambiente. "
                "Configure APDATA_USERNAME e APDATA_PASSWORD."
            )

        try:
            with sync_playwright() as p:
                # Lança o navegador
                browser = p.chromium.launch(
                    headless=self.headless,
                    args=[
                        "--disable-gpu",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                    ],
                )
                print("Navegador aberto!")

                page = browser.new_page()
                page.set_default_timeout(30000)  # 30s

                # Acessa página de ponto
                page.goto("https://cliente.apdata.com.br/dicon/", wait_until="load")
                print("Página carregada!")

                # Tempo extra opcional (às vezes o servidor é lento)
                time.sleep(5)

                # 1) Aceitar aviso de cookies (botão com id=button-1021)
                try:
                    btn_cookie = page.wait_for_selector("#button-1021", timeout=15000)
                    print("Aviso de Cookies carregado...")
                    btn_cookie.click()
                    print("Aviso de Cookies aceito!")
                except TimeoutError as e:
                    # Se não aparecer o aviso, segue o fluxo
                    print(f"Aviso de cookies não apareceu ou já foi aceito: {e}")

                # 2) Campos de login
                usuario = page.wait_for_selector(
                    "input[name='userName_relogio_8001']", timeout=30000
                )
                print("Campo de usuário carregado...")
                senha = page.wait_for_selector(
                    "input[name='password_relogio_8001']", timeout=30000
                )
                print("Campo de senha carregado...")
                bater = page.wait_for_selector("#ext-142", timeout=30000)
                print("Botão de bater ponto carregado...")

                # 3) Preencher credenciais e enviar
                print("Preenchendo credenciais e batendo ponto...")
                usuario.fill(self.username)
                print("Usuário preenchido...")
                senha.fill(self.password)
                print("Senha preenchida...")
                bater.click()
                print("Clique no botão de ponto enviado...")

                # 4) Aguardar resultado
                print("Ponto enviado, aguardando confirmação...")
                resultado = page.wait_for_selector("#ext-144", timeout=30000)
                print("Confirmação de ponto carregada...")

                # Pequena pausa para garantir que o texto foi renderizado
                time.sleep(2)

                texto_resultado = resultado.inner_text()
                print("Resultado da batida de ponto:")
                print(texto_resultado)

                periodo_label = periodo or "Ponto"
                msg = (
                    f"{periodo_label} batido com sucesso em "
                    f"{datetime.now(tz=ZoneInfo(self.timezone)).strftime('%d/%m/%Y %H:%M:%S')}.\n\n"
                    f"Mensagem do sistema:\n{texto_resultado}"
                )

                browser.close()
                print("Fechando navegador...")

                return "Sucesso", msg

        except PlaywrightTimeoutError as e:
            print(f"ERRO AO BATER PONTO (timeout): {e}")
            msg = (
                "Timeout ao tentar bater ponto em "
                f"{datetime.now(tz=ZoneInfo(self.timezone)).strftime('%d/%m/%Y %H:%M:%S')}.\n"
                f"Detalhes: {e}"
            )
            return "Erro", msg

        except Exception as e:
            print(f"ERRO AO BATER PONTO: {e}")
            msg = (
                "Erro ao bater ponto em "
                f"{datetime.now(tz=ZoneInfo(self.timezone)).strftime('%d/%m/%Y %H:%M:%S')}.\n"
                f"Detalhes: {e}"
            )
            return "Erro", msg
