from datetime import datetime, time
from time import sleep
from zoneinfo import ZoneInfo

from Feriados import Feriados
from Ponto import PontoBot
from Send_email import EmailReporter

# Janelas de segurança (para não tentar o dia todo)
ENTRADA_INICIO = time(7, 10)
ENTRADA_LIMITE = time(7, 23)

SAIDA_INICIO = time(16, 55)
SAIDA_LIMITE = time(17, 11)

# Horários exatos em que o ponto deve ser batido
TARGET_ENTRADA = "07:22"
TARGET_SAIDA = "17:10"


def _esta_na_janela(agora: time) -> bool:
    """Retorna True se estiver em qualquer janela (entrada ou saída)."""
    return (
        ENTRADA_INICIO <= agora <= ENTRADA_LIMITE
        or SAIDA_INICIO <= agora <= SAIDA_LIMITE
    )


def _identificar_periodo_por_horario_exato(hora_minuto: str) -> str | None:
    """
    Descobre se o horário exato é de Entrada ou Saída.
    """
    if hora_minuto == TARGET_ENTRADA:
        return "Entrada"
    if hora_minuto == TARGET_SAIDA:
        return "Saída"
    return None


def main() -> None:
    feriados = Feriados()
    reporter = EmailReporter()
    ponto_bot = PontoBot(feriados=feriados, headless=True)

    # Validação inicial: dia útil / feriado
    pode_bater, msg_validacao = feriados.can_mark_today()
    if not pode_bater:
        reporter.send_report("Ignorado", msg_validacao)
        return

    print("Iniciando loop para aguardar horário exato de batida de ponto...")

    while True:
        agora_dt = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
        agora = agora_dt.time()
        hora_minuto = agora_dt.strftime("%H:%M")

        print(f"Agora: {hora_minuto}")

        # 1) Se já passou da janela de SAÍDA → desiste do dia
        if agora > SAIDA_LIMITE:
            msg = (
                "Passou da janela de saída "
                f"({SAIDA_LIMITE.strftime('%H:%M')}). "
                "Nenhum ponto foi batido (entrada/saída)."
            )
            print(msg)
            reporter.send_report("Erro", msg)
            break

        # 2) Se já passou da janela de ENTRADA, mas ainda não entrou na janela de SAÍDA
        #    → perdeu a entrada, e esse script não vai tentar a saída
        if ENTRADA_LIMITE < agora < SAIDA_INICIO:
            msg = (
                "Passou da janela de entrada "
                f"({ENTRADA_LIMITE.strftime('%H:%M')}) "
                "e ainda não começou a janela de saída. "
                "Ponto de entrada não será batido."
            )
            print(msg)
            reporter.send_report("Erro", msg)
            break

        # 3) Se ainda não chegou na janela de entrada → só aguarda
        if agora < ENTRADA_INICIO:
            print("Ainda não chegou na janela. Aguardando 60 segundos...")
            sleep(60)
            continue

        # 4) Aqui sabemos que:
        #    - Estamos dentro da janela de entrada, OU
        #    - Já dentro da janela de saída
        if not _esta_na_janela(agora):
            # Só por segurança, deveria ser coberto pelos casos acima
            print("Fora das janelas de marcação, aguardando 60 segundos...")
            sleep(60)
            continue

        periodo = _identificar_periodo_por_horario_exato(hora_minuto)

        if periodo:
            # Só entra aqui se for exatamente 07:22 ou 17:10
            print(f"Horário EXATO de {periodo} atingido ({hora_minuto}). Tentando bater ponto...")
            status, msg = ponto_bot.bater_ponto(periodo=periodo)
            reporter.send_report(status, msg)
            break

        # Ainda dentro da janela, mas não é o horário exato ainda
        print(
            "Dentro da janela de marcação, mas ainda não é o horário exato "
            f"(alvos: {TARGET_ENTRADA} / {TARGET_SAIDA}). Aguardando 60 segundos..."
        )
        sleep(60)


if __name__ == "__main__":
    main()
