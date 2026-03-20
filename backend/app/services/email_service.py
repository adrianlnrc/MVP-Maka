import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import settings


def send_password_reset_email(to_email: str, reset_token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/recuperar-senha/{reset_token}"

    subject = "Maka — Redefinição de senha"
    body_html = f"""
    <html>
    <body style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6366f1;">Maka — Redefinição de Senha</h2>
        <p>Recebemos uma solicitação para redefinir sua senha.</p>
        <p>Clique no link abaixo para criar uma nova senha. O link expira em 1 hora.</p>
        <a href="{reset_url}" style="
            display: inline-block;
            background: #6366f1;
            color: white;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            margin: 16px 0;
        ">Redefinir senha</a>
        <p style="color: #888; font-size: 14px;">
            Se você não solicitou isso, ignore este e-mail.
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
        <p style="color: #888; font-size: 12px;">Maka — Bíblia Cronológica</p>
    </body>
    </html>
    """

    if not settings.SMTP_HOST:
        # Development: just print the link
        print(f"[EMAIL] Reset link for {to_email}: {reset_url}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.FROM_EMAIL
    msg["To"] = to_email
    msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.FROM_EMAIL, to_email, msg.as_string())
