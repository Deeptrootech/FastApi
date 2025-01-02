from email.message import EmailMessage
from aiosmtplib import send


# Background task to send the email
async def send_register_success_email(to_email: str, username: str):
    """Function to send a login success email."""
    message = EmailMessage()
    message["From"] = "deep.pathak@trootech.com"  # Replace with your email
    message["To"] = to_email
    message["Subject"] = "SignUp Successful"
    message.set_content(
        f"Hello {username},\n\nYou have successfully Registered your account.\n\nThank you!"
    )

    # Replace with your SMTP settings
    await send(
        message,
        hostname="smtp.gmail.com",  # e.g., smtp.gmail.com
        port=465,
        username="deep.pathak@trootech.com",
        password="Kmnj#@5by",
        use_tls=True,
    )
