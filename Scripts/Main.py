from datetime import datetime
import time

from Ponto import bater_ponto
from Send_email import send_report

ENTRADA_INICIO = time(7, 22)
ENTRADA_LIMITE = time(7, 27)

SAIDA_INICIO = time(17, 10)
SAIDA_LIMITE = time(17, 15)

tempo = True
while tempo:
    agora = datetime.now().time()

    # Dentro da janela de entrada
    if ENTRADA_INICIO <= agora <= ENTRADA_LIMITE:
        bater_ponto()
        break

    # Dentro da janela de saída
    elif SAIDA_INICIO <= agora <= SAIDA_LIMITE:
        bater_ponto()
        break

    # PASSOU da janela de entrada e AINDA é cedo (antes da janela da saída)
    elif agora > ENTRADA_LIMITE and agora < SAIDA_INICIO:
        # Perdeu a entrada → para imediatamente
        tempo = False

    # PASSOU da janela de saída
    elif agora > SAIDA_LIMITE:
        # Perdeu até a saída → para imediatamente
        tempo = False

    time.sleep(60)

else:
    send_report("Erro", "Passou do horário esperado para bater ponto.")
