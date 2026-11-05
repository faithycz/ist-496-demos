import requests
from dotenv import load_dotenv
import os

def pushover_setup():
    """
    This loads the environment variables for pushover and verifies they exist and are correct.
    """
    pushover_user = os.getenv("PUSHOVER_USER")
    pushover_token = os.getenv("PUSHOVER_TOKEN")

    if pushover_user:
        if pushover_user.startswith("u"):
            print("Pushover user found and looks good")
        else:
            print("Pushover user found but doesn't start with u")
    else:
        print("Pushover user not found")

    if pushover_token:
        if pushover_token.startswith("a"):
            print("Pushover token found and looks good")
        else:
            print("Pushover token found but doesn't start with a")
    else:
        print("Pushover token not found")

def push(message):
    pushover_user = os.getenv("PUSHOVER_USER")
    pushover_token = os.getenv("PUSHOVER_TOKEN")
    pushover_url = "https://api.pushover.net/1/messages.json"

    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)