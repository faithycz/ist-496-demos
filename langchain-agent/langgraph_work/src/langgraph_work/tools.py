from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv(override=True)

search = GoogleSerperRun(api_wrapper=GoogleSerperAPIWrapper())

@tool
def send_email(subject: str, text_body: str, html_body: str) -> str:
    """Send an email to the user's email address."""
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL(EMAIL_SMTP_SERVER, 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)

    return "Email sent"

tools = [search, send_email]