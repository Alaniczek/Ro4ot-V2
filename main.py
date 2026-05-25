import asyncio
import json
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.RobotManager import RobotManager
from core.RobotKit import RobotKit
from core.CommandManager import CommandManager

# CONFIGS ☆*: .｡. o(≧▽≦)o .｡.:*☆
CONFIG_PATH = "jsons/config.json"
COMMANDS_PATH = "jsons/commands.json"

robot_manager = RobotManager()

def load_config() -> Dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {"predkosc": 100, "tryb": "auto"}
        save_config(default_config)
        return default_config

def save_config(data: Dict[str, Any]):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

# Background workers *^____^*
async def background_worker():
    while True:
        #LOGIC IN THE BACKGROUND PLACE
        await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(background_worker())
    yield
    task.cancel()

# Main part (●'◡'●)
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("templates/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[WS] Połączono klienta.")
    
    try:
        while True:
            raw_data = await websocket.receive_text()
            message = json.loads(raw_data)
            action = message.get("akcja")

            if action == "ping":
                await websocket.send_json({
                    "akcja": "pong",
                    "python_added": "Odebrano z HTML, leci z powrotem do JS!"
                })

            elif action == "wczytaj":
                cfg = load_config()
                await websocket.send_json({"akcja": "zaladowano_config", "dane": cfg})

            elif action == "zapisz":
                save_config(message.get("dane", {}))
                await websocket.send_json({"akcja": "info", "tekst": "Konfiguracja zapisana!"})

            elif action == "ping_robot":
                ip = message.get("ip")
                port = int(message.get("port"))
                
                robot_kit = RobotKit(ip, port, "Unknown", "Manual")
                robot_manager.selectRobotByKit(robot_kit)
                robot_manager.command_manager = CommandManager(ip, port, COMMANDS_PATH)
                
                print(f"[UDP] Wysyłam PING do robota {ip}:{port}")
                robot_manager.command_manager.send_command("ping")
                
                await websocket.send_json({
                    "akcja": "info",
                    "tekst": f"Wysłano UDP 'ping' do {ip}:{port}"
                })

            elif action == "log":
                print(f"[LOG] {message}")

            else:
                print(f"[WS] Nieznana akcja: {action}")

    except WebSocketDisconnect:
        print("[WS] Rozłączono klienta.")
    except Exception as e:
        print(f"[ERR] Błąd WebSocketa: {e}")
