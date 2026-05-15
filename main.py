from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import socket

app = FastAPI()

UDP_IP = "192.168.1.100"
UDP_PORT = 4210


@app.get("/", response_class=HTMLResponse)
async def form_page():
    return """
    <html>
        <body>
            <h2>Panel sterowania Ro4ot</h2>
            <form action="/send" method="post">
                <input type="text" name="command" autofocus>
                <button type="submit">Wyslij UDP</button>
            </form>
        </body>
    </html>
    """


@app.post("/send")
async def send_to_robot(command: str = Form(...)):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (UDP_IP, UDP_PORT))

    return {"wyslano": command, "cel": UDP_IP}