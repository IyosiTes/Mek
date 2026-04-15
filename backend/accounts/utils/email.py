import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY

def send_reset_email(email, reset_link):
    try:
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [email],
            "subject": "Password Reset",
            "html": f"""
                <h2>Password Reset</h2>
                <p>Click below to reset your password:</p>
                <a href="{reset_link}">Reset Password</a>
                <p>This link expires in 15 minutes.</p>
            """
        })
        print("EMAIL SENT SUCCESS")
    except Exception as e:
        print("EMAIL ERROR:", str(e))