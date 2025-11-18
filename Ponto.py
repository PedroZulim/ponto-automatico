from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
from datetime import datetime


def bater_ponto():
    # Segunda (0) até sexta (4)
    hoje = datetime.today().weekday()
    if not (0 <= hoje <= 4):
        print("Hoje não é dia útil, não vou bater ponto.")
        return

    # Carrega .env localmente (no GitHub será ignorado, mas tudo vem de secrets)
    load_dotenv()

    username = os.getenv("APDATA_USERNAME") or os.getenv("username")
    password = os.getenv("APDATA_PASSWORD") or os.getenv("password")

    if not username or not password:
        raise ValueError("Usuário/senha não encontrados nas variáveis de ambiente.")

    chrome_options = Options()
    # Headless pro GitHub Actions
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get("https://cliente.apdata.com.br/dicon/")
        time.sleep(3)

        btn = driver.find_element(By.ID, "button-1021")
        btn.send_keys(Keys.RETURN)
        time.sleep(3)

        usuario = driver.find_element(By.NAME, "userName_relogio_8001")
        senha = driver.find_element(By.NAME, "password_relogio_8001")
        bater = driver.find_element(By.ID, "ext-142")

        usuario.send_keys(username)
        senha.send_keys(password)

        bater.send_keys(Keys.RETURN)
        time.sleep(3)

        print("Ponto batido com sucesso.")
    finally:
        driver.quit()


if __name__ == "__main__":
    bater_ponto()
