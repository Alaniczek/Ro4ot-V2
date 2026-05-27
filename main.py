import asyncio
import json
from contextlib import asynccontextmanager
from typing import Dict, Any, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from core.RobotManager import RobotManager
from core.RobotKit import RobotKit
from core.CommandManager import CommandManager
from core.ResponseHandler import ResponseHandler

# CONFIGS ☆*: .｡. o(≧▽≦)o .｡.:*☆
CONFIG_PATH = "jsons/config.json"
COMMANDS_PATH = "jsons/commands.json"

robot_manager = RobotManager()
response_handler = ResponseHandler(robot_manager)
active_websockets: Set[WebSocket] = set()

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


async def on_robot_response(ip: str, message: str):
    print(f"[STATUS] Robot {ip} sent: {message}")

    async def send_to_ws(ws):
        try:
            await ws.send_json({
                "akcja": "robot_status",
                "ip": ip,
                "status": message
            })
        except Exception:
            active_websockets.discard(ws)

    if active_websockets:
        await asyncio.gather(*(send_to_ws(ws) for ws in list(active_websockets)))

# Background workers *^____^*
async def background_worker():
    while True:
        await asyncio.sleep(5)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*50)
    print("RO4OT-V2: STARTING UDP LISTENER")
    try:
        # Start the UDP Response Handler on port 17145
        await response_handler.start(port=17145)
        response_handler.set_callback(on_robot_response)
        print("RO4OT-V2: SUCCESS - Listening on 17145")
    except Exception as e:
        print(f"RO4OT-V2: ERROR - Could not start UDP listener: {e}")
    print("="*50 + "\n")
    
    task = asyncio.create_task(background_worker())
    yield
    task.cancel()
    response_handler.stop()

# Main part (●'◡'●)
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("templates/index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    print("[WS] Połączono klienta.")

    try:
        while True:
            try:
                message = await websocket.receive_json()
            except ValueError:
                print("[WS] Otrzymano nieprawidłowy JSON.")
                continue

            action = message.get("akcja")

            match action:
                case "ping":
                    await websocket.send_json({
                        "akcja": "pong",
                        "python_added": "Odebrano z HTML, leci z powrotem do JS!"
                    })

                case "wczytaj":
                    await websocket.send_json({
                        "akcja": "zaladowano_config",
                        "dane": load_config()
                    })

                case "zapisz":
                    save_config(message.get("dane", {}))
                    await websocket.send_json({
                        "akcja": "info",
                        "tekst": "Konfiguracja zapisana!"
                    })

                case "ping_robot":
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

                case "log":
                    print(f"[LOG] {message}")

                case _:
                    print(f"[WS] Nieznana akcja: {action}")

    except WebSocketDisconnect:
        print("[WS] Rozłączono klienta.")
    except Exception as e:
        print(f"[ERR] Błąd WebSocketa: {e}")
    finally:
        active_websockets.discard(websocket)