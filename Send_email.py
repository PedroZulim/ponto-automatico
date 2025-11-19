from email.mime.text import MIMEText
import os
import smtplib

from dotenv import load_dotenv

load_dotenv()


def send_report(status, message):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = sender

    body = f"Status: {status}\n\n{message}"
    msg = MIMEText(body)
    msg["Subject"] = f"Relatório ponto automático - {status}"
    msg["From"] = sender
    msg["To"] = ", ".join(receiver)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print(f"Email enviado com sucesso para {', '.join(receiver)}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erro de autenticação: {e}")
        raise
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        raise