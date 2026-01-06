import requests
import os
from schemas.mensajes_schema import MensajesSchema
from fastapi.responses import JSONResponse
from fastapi import Depends
from services.contactos_service import save_mensaje
from database import get_db
from sqlalchemy.orm import Session
class Whatsapp():
    def whats_text(self,telefono,message):
        url = "https://apiwsp.factiliza.com/v1/message/sendtext/NTE5MTc0MTQ2ODQ="
        payload = {
            "number": '51' + str(telefono),
            "text": str(message)
        }
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzODU3MyIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.dKmKFEJ438eSF6gx4L52asNttTiVEbBd9RMxYj3GyE0",
            "Content-Type": "application/json"
        }
        response=requests.post(url, json=payload, headers=headers)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
    
    def waba_text(self,db:Session,telefono,time_wpp,message):
        telefono_str=str(telefono)
        data={
            "wa_id":telefono_str,
            "nombre":"def",
            "id_usuario":1,
            "direction":"outgoing",
            "waba_message_id":"def",
            "message_type":"text",
            "text_content":message,
            "raw_json":"",
            "timestamp":int(time_wpp)
        }
        version=os.getenv("VERSION_WPP_API")
        phone_number_id=os.getenv("ID_PHONE_NUMER_WPP")
        token=os.getenv("TOKEN_WPP")
        url = f"https://graph.facebook.com/{version}/{phone_number_id}/messages"

        body = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": data['wa_id'],
            "type": "text",
            "text": {
                "preview_url": False,
                "body": data['text_content']
            }
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response=requests.post(url, json=body, headers=headers)

        if not response.ok:
            return JSONResponse(content={"error":response.text},status_code=500)
        obj = response.json()
        message_id = obj["messages"][0]["id"]
        data["waba_message_id"]=message_id
        data["raw_json"]=obj
        mensaje_schema=MensajesSchema(**data)
        mensaje=save_mensaje(db,mensaje_schema)
        return {
            "status": "sent",
            "id": mensaje.id,
            "waba_message_id": data["waba_message_id"]
        }
