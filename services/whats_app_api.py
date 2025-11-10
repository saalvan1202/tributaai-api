import requests
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
