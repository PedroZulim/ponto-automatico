from datetime import datetime, time
from time import sleep

from Feriados import Feriados
from Ponto import PontoBot
from Send_email import EmailReporter


# Janela de entrada
ENTRADA_INICIO = time(7, 15)
ENTRADA_LIMITE = time(7, 23)

# Janela de saída
SAIDA_INICIO = time(17, 3)
SAIDA_LIMITE = time(17, 11)


def _identificar_periodo(agora: time) -> str | None:
    if ENTRADA_INICIO <= agora <= ENTRADA_LIMITE:
        return "Entrada"
    if SAIDA_INICIO <= agora <= SAIDA_LIMITE:
        return "Saída"
    return None


def main() -> None:
    feriados = Feriados()
    reporter = EmailReporter()
    ponto_bot = PontoBot(feriados=feriados, headless=True)

    # Validação inicial: dia útil / feriado
    pode_bater, msg_validacao = feriados.can_mark_today()
    if not pode_bater:
        # Só manda um relatório simples de "Ignorado" e encerra
        reporter.send_report("Ignorado", msg_validacao)
        return

    print("Iniciando loop de horário para bater ponto...")

    while True:
        agora = datetime.now().time()
        periodo = _identificar_periodo(agora)

        if periodo:
            print(f"Dentro da janela de {periodo}. Tentando bater ponto...")
            status, msg = ponto_bot.bater_ponto(periodo=periodo)
            reporter.send_report(status, msg)
            break

        # Se passou da janela de saída, não faz mais nada hoje
        if agora > SAIDA_LIMITE:
            msg = "Passou do horário esperado para bater ponto (entrada e saída)."
            print(msg)
            reporter.send_report("Erro", msg)
            break

        print("Fora da janela de marcação, aguardando 60 segundos...")
        sleep(60)


if __name__ == "__main__":
    main()