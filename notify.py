import os
import smtplib
from email.mime.text import MIMEText


def send_notification(subject: str, body: str) -> None:
    """
    Envía un correo de aviso a través de Gmail SMTP. Si no están
    configuradas las variables de entorno, o falla el envío, no
    interrumpe el flujo principal (guardar el lead o la reseña es lo
    importante; el aviso es un extra).
    """

    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    notify_email = os.getenv("NOTIFY_EMAIL", smtp_user)

    if not smtp_user or not smtp_password or not notify_email:
        return

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = smtp_user
    message["To"] = notify_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [notify_email], message.as_string())
    except Exception:
        # No dejamos que un fallo de correo tumbe el guardado del dato.
        pass
