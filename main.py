

import os
from typing import Optional
import asyncio
from fastapi import FastAPI, Form, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
import config
import uvicorn

app = FastAPI()
settings = config.Settings()


@app.get('/')
async def index():
    return FileResponse('index.html')

@app.post('/')
async def handle_form(phone: str = Form(...)):
    await asyncio.get_event_loop().run_in_executor(
        None, send_sms, phone, 'Hola!, el codigo solicitado es: ')
    return RedirectResponse('/success', status_code=status.HTTP_303_SEE_OTHER)


def send_sms(to_number, body):
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    return client.messages.create(from_=settings.twilio_phone_number,
                                  to=to_number, body=body)

@app.get('/success')
async def success():
    return FileResponse('success.html')





if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=5000)), log_level="info")
