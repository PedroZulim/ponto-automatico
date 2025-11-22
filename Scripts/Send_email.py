from email.mime.text import MIMEText
import os
import smtplib
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

StatusType = Literal["Sucesso", "Erro", "Ignorado"]


class EmailReporter:
    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 465,
    ) -> None:
        self.sender = os.getenv("EMAIL_SENDER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

        if not self.sender or not self.password:
            print(
                "ATENÇÃO: EMAIL_SENDER ou EMAIL_PASSWORD não configurados. "
                "O envio de e-mails será ignorado."
            )
            self._enabled = False
        else:
            self._enabled = True

    def send_report(self, status: StatusType, message: str) -> None:
        """
        Envia um e-mail simples com o status e a mensagem.
        Não levanta exceção se falhar, apenas loga o erro.
        """
        if not self._enabled:
            print("Reporter de e-mail desabilitado. Não foi enviado e-mail.")
            print(f"[{status}] {message}")
            return

        body = f"Status: {status}\n\n{message}"
        msg = MIMEText(body)
        msg["Subject"] = f"Relatório ponto automático - {status}"
        msg["From"] = self.sender
        msg["To"] = self.sender

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.sender, self.password)
                smtp.send_message(msg)
            print(f"Email enviado com sucesso para {self.sender}")
        except smtplib.SMTPAuthenticationError as e:
            print(f"Erro de autenticação ao enviar email: {e}")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")