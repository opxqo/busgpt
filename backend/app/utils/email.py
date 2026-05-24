import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import settings


def send_activation_email(email: str, token: str) -> None:
    """Send an activation email with a verification link."""
    activation_url = f"{settings.BACKEND_URL}{settings.API_V1_STR}/auth/activate?token={token}&redirect=1"

    subject = "BusGPT - 请激活您的邮箱"
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f7f4ee; padding: 40px 20px; color: #191f24;">
      <div style="max-width: 480px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 40px 32px; border: 1px solid #ded8cd;">
        <div style="text-align: center; margin-bottom: 24px;">
          <div style="display: inline-flex; width: 48px; height: 48px; align-items: center; justify-content: center; border-radius: 10px; background: #191f24; color: #f7f4ee; font-size: 20px; font-weight: 900;">B</div>
        </div>
        <h1 style="margin: 0 0 8px; font-size: 22px; font-weight: 800; text-align: center;">激活您的 BusGPT 账户</h1>
        <p style="margin: 0 0 24px; font-size: 14px; color: #6b7280; text-align: center; line-height: 1.6;">
          您好！请点击下方按钮完成邮箱验证。<br>此链接 24 小时内有效。
        </p>
        <div style="text-align: center; margin-bottom: 24px;">
          <a href="{activation_url}" style="display: inline-block; padding: 12px 32px; background: #10b981; color: #ffffff; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 14px;">点击激活邮箱</a>
        </div>
        <p style="margin: 0; font-size: 12px; color: #9ca3af; text-align: center; line-height: 1.6;">
          如果您没有注册 BusGPT 账户，请忽略此邮件。<br>
          如按钮无法点击，请复制以下链接到浏览器：<br>
          <span style="word-break: break-all; color: #6b7280;">{activation_url}</span>
        </p>
      </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_USERNAME}>"
    msg["To"] = email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        print(f"\n{'=' * 60}")
        print(f"[DEV MODE] SMTP not configured. Activation link:")
        print(f"  To: {email}")
        print(f"  URL: {activation_url}")
        print(f"{'=' * 60}\n")
        return

    try:
        if settings.SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()

        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USERNAME, email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send activation email to {email}: {e}")
        print(f"[DEV FALLBACK] Activation URL: {activation_url}")
        raise
