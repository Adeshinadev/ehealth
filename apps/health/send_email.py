"""
This call sends a message to the given recipient with vars and custom vars.
"""
from mailjet_rest import Client
import os

api_key = "681f0ff1ce057f32e0cbe2b617c8cc71"
api_secret = "bae164dd8f28e32614626d1829c2f964"
"""i intentionally left this open here for testing purposes"""
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_mail(email, message):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "adeshinex4u@gmail.com",
                    "Name": "eHealth4everyone"
                },
                "To": [
                    {
                        "Email": f"{email}",
                        "Name": "passenger 1"
                    }
                ],
                "TemplateID": 4454095,
                "TemplateLanguage": True,
                "Subject": "Appointment notification",
                "Variables": {
                    "message": f"{message}"
                }
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code,'lloiu')
