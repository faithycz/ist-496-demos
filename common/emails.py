from agents import function_tool, Agent, output_guardrail, GuardrailFunctionOutput, Runner
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
from pydantic import BaseModel, Field

from common.model import openai_gpt_mini

load_dotenv(override=True)

def email_setup():
    """
        This verifies that an email address, SMTP server, and app password exist and are set up properly.
    """

    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

    if EMAIL_ADDRESS:
        print("Email address is set")
    else:
        print("Email address is not set")

    if EMAIL_SMTP_SERVER:
        print("SMTP server is set")
    else:
        print("SMTP server is not set")

    if EMAIL_APP_PASSWORD:
        print("App password is set")
    else:
        print("App password is not set")

    USE_EMAIL = EMAIL_ADDRESS and EMAIL_SMTP_SERVER and EMAIL_APP_PASSWORD

    if USE_EMAIL:
        print("Email is set up and ready to use!")
    else:
        print("Email is not set up and requires troubleshooting.")

def send_email(subject: str, text_body: str, html_body: str):
    """
        This is a regular Python function that sends an email to a user.

        Args:
            subject (str): subject of the email
            text_body (str): body of the email
            html_body (str): body of the email
    """

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

@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    This is a function that sends an email to a user.

    Args:
        subject (str): subject of the email
        text_body (str): body of the email
        html_body (str): body of the email
    """
    send_email(subject, text_body, html_body)

    return "Email sent successfully"

class EmailReview(BaseModel):
    is_professional: bool = Field(description="Whether the email is professional and appropriate")
    number_of_sentences: int = Field(description="The number of sentences in the body of the email, not including the greeting and signature")
    contains_placeholders: bool = Field(description="Whether the email contains placeholders for personalization")

checker = Agent(name="Checker", instructions="You review potential sales emails", model=openai_gpt_mini, output_type=EmailReview)

@output_guardrail
async def email_guardrail(ctx, agent, message):
    result = await Runner.run(checker, message, context=ctx.context)
    review = result.final_output
    is_problem = review.contains_placeholders or not review.is_professional
    return GuardrailFunctionOutput(output_info={"review": review},tripwire_triggered=is_problem)