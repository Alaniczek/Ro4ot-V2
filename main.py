import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {"predkosc": 100, "tryb": "auto"}
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config


def save_config(data):
    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)


async def moja_funkcja_w_tle():
    while True:
        print("Robię coś innego w tle!")
        await asyncio.sleep(5)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(moja_funkcja_w_tle())


@app.get("/")
async def get():
    return FileResponse("templates/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        message = json.loads(data)

        if message.get("step") == 1:
            message["step"] = 2
            message["python_added"] = "Odebrano z HTML, leci z powrotem do JS!"
            await websocket.send_text(json.dumps(message))

        elif message.get("step") == 3:
            print("--- LOGI Z PYTHONA ---")
            print("Ostateczny JSON:", message)
            print("----------------------")

        elif message.get("akcja") == "wczytaj":
            cfg = load_config()
            await websocket.send_text(json.dumps({"akcja": "zaladowano_config", "dane": cfg}))

        elif message.get("akcja") == "zapisz":
            save_config(message.get("dane", {}))
            await websocket.send_text(json.dumps({"akcja": "info", "tekst": "Plik config.json został zapisany!"}))