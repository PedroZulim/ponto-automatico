from datetime import datetime
import os

from dotenv import load_dotenv
import Fetch_api
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def bater_ponto():
    fetch = Fetch_api.Feriados()
    # Segunda (0) até sexta (4)
    hoje = datetime.today().weekday()
    if not (0 <= hoje <= 4):
        print("Hoje não é dia útil, não vou bater ponto.")
        # send_report("Ignorado", "Hoje não é dia útil, não vou bater ponto.")
        return
    elif fetch.get_feriados().__contains__(datetime.today().strftime('%Y-%m-%d')):
        print("Hoje é feriado, não vou bater ponto.")
        # send_report("Ignorado", "Hoje é feriado, não vou bater ponto.")
        return

    # Carrega .env localmente (no GitHub usa secrets)
    load_dotenv()

    username = os.getenv("APDATA_USERNAME") or os.getenv("username")
    password = os.getenv("APDATA_PASSWORD") or os.getenv("password")

    if not username or not password:
        raise ValueError("Usuário/senha não encontrados nas variáveis de ambiente.")

    print(f'user: {username}, pass: {password}')

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    print("Navegador aberto!")

    wait = WebDriverWait(driver, 30)  # espera até 30s pros elementos aparecerem

    try:
        driver.get("https://cliente.apdata.com.br/dicon/")
        print("Página carregada!")

        # espera o botão inicial ficar clicável
        btn = wait.until(
            ec.element_to_be_clickable((By.ID, "button-1021"))
        )
        btn.send_keys(Keys.RETURN)

        # espera os campos de usuário e senha aparecerem
        usuario = wait.until(
            ec.presence_of_element_located((By.NAME, "userName_relogio_8001"))
        )
        senha = wait.until(
            ec.presence_of_element_located((By.NAME, "password_relogio_8001"))
        )
        bater = wait.until(
            ec.element_to_be_clickable((By.ID, "ext-142"))
        )

        usuario.send_keys(username)
        senha.send_keys(password)
        bater.send_keys(Keys.RETURN)

        print("Ponto batido com sucesso!")

        # send_report("Sucesso", "Ponto batido com sucesso.")
        wait.until(
            ec.presence_of_element_located((By.ID, "ext-144"))
        )

        print(driver.find_element(By.ID, "ext-144").text)
    except Exception as e:
        # loga erro bonitinho pra debug nos Actions
        print(f"ERRO AO BATER PONTO: {e}")
        # send_report("Erro", f"Erro ao bater ponto: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    bater_ponto()
