from datetime import datetime, time
from time import sleep
from zoneinfo import ZoneInfo

from Config import Config
from Feriados import Feriados
from Ponto import PontoBot
from Send_email import EmailReporter


def _esta_na_janela(agora: time, config: Config) -> bool:
    """Retorna True se estiver em qualquer janela (entrada ou saída)."""
    return (
        config.entrada_janela_inicio <= agora <= config.entrada_janela_limite
        or config.saida_janela_inicio <= agora <= config.saida_janela_limite
    )


def _identificar_periodo_por_horario_exato(hora_minuto: str, config: Config) -> str | None:
    """
    Descobre se o horário exato é de Entrada ou Saída.
    """
    if hora_minuto == config.entrada_horario_exato:
        return "Entrada"
    if hora_minuto == config.saida_horario_exato:
        return "Saída"
    return None


def main() -> None:
    # Carrega configurações
    config = Config()
    
    feriados = Feriados(timezone=config.timezone)
    reporter = EmailReporter()
    ponto_bot = PontoBot(
        feriados=feriados,
        headless=config.modo_headless,
        timezone=config.timezone
    )

    # Validação inicial: dia útil / feriado
    pode_bater, msg_validacao = feriados.can_mark_today()
    if not pode_bater:
        reporter.send_report("Ignorado", msg_validacao)
        return

    print("Iniciando loop para aguardar horário exato de batida de ponto...")

    while True:
        agora_dt = datetime.now(tz=ZoneInfo(config.timezone))
        agora = agora_dt.time()
        hora_minuto = agora_dt.strftime("%H:%M")

        print(f"Agora: {hora_minuto}")

        # 1) Se já passou da janela de SAÍDA → desiste do dia
        if agora > config.saida_janela_limite:
            msg = (
                "Passou da janela de saída "
                f"({config.saida_janela_limite.strftime('%H:%M')}). "
                "Nenhum ponto foi batido (entrada/saída)."
            )
            print(msg)
            reporter.send_report("Erro", msg)
            break

        # 2) Se já passou da janela de ENTRADA, mas ainda não entrou na janela de SAÍDA
        #    → perdeu a entrada, e esse script não vai tentar a saída
        if config.entrada_janela_limite < agora < config.saida_janela_inicio:
            msg = (
                "Passou da janela de entrada "
                f"({config.entrada_janela_limite.strftime('%H:%M')}) "
                "e ainda não começou a janela de saída. "
                "Ponto de entrada não será batido."
            )
            print(msg)
            reporter.send_report("Erro", msg)
            break

        # 3) Se ainda não chegou na janela de entrada → só aguarda
        if agora < config.entrada_janela_inicio:
            print("Ainda não chegou na janela. Aguardando...")
            sleep(config.intervalo_verificacao)
            continue

        # 4) Aqui sabemos que:
        #    - Estamos dentro da janela de entrada, OU
        #    - Já dentro da janela de saída
        if not _esta_na_janela(agora, config):
            # Só por segurança, deveria ser coberto pelos casos acima
            print("Fora das janelas de marcação, aguardando...")
            sleep(config.intervalo_verificacao)
            continue

        periodo = _identificar_periodo_por_horario_exato(hora_minuto, config)

        if periodo:
            # Só entra aqui se for exatamente o horário configurado
            print(f"Horário EXATO de {periodo} atingido ({hora_minuto}). Tentando bater ponto...")
            status, msg = ponto_bot.bater_ponto(periodo=periodo)
            reporter.send_report(status, msg)
            break

        # Ainda dentro da janela, mas não é o horário exato ainda
        print(
            "Dentro da janela de marcação, mas ainda não é o horário exato "
            f"(alvos: {config.entrada_horario_exato} / {config.saida_horario_exato}). Aguardando..."
        )
        sleep(config.intervalo_verificacao)


if __name__ == "__main__":
    main()
