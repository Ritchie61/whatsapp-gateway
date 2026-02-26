from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/webhook")
def verify(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    if hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return "Verification failed"

@app.post("/webhook")
async def receive_message(request: Request):
    payload = await request.json()

    message_text = extract_text(payload)
    if not message_text:
        return {"status": "ignored"}

    command = parse_command(message_text)
    response_text = route_command_to_picoclaw(command)

    send_whatsapp_message(
        text=response_text,
        to=extract_sender(payload)
    )

    return {"status": "ok"}
