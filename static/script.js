const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = function(event) {
    let message = JSON.parse(event.data);
    const akcja = message.akcja;

    if (akcja === "pong") {
        document.getElementById("output").innerText = "JS: Otrzymałem z Pythona! Odsyłam log.";
        message.akcja = "log";
        message.js_added = "HTML też tu był!";
        ws.send(JSON.stringify(message));
    }
    else if (akcja === "zaladowano_config") {
        document.getElementById("configEditor").value = JSON.stringify(message.dane, null, 4);
        document.getElementById("configStatus").innerText = "Wczytano pomyślnie z serwera!";
    }
    else if (akcja === "info") {
        document.getElementById("configStatus").innerText = message.tekst;
    }
};

function selectAndPingRobot()
{
    robot_ip = document.querySelector('#ROBOT_IP').value;
    robot_port = document.querySelector('#ROBOT_PORT').value;

    if (robot_ip && robot_port) {
        ws.send(JSON.stringify({ akcja: "ping_robot", ip: robot_ip, port: robot_port }));
        document.getElementById("output").innerText = `JS: Wysyłam ping do robota ${robot_ip}:${robot_port}...`;
    } else {
        document.getElementById("output").innerText = "JS: Proszę podać IP i port robota!";
    }
}


function startPingPong() {
    document.getElementById("output").innerText = "JS: Wysyłam do Pythona ping...";
    ws.send(JSON.stringify({ akcja: "ping", info: "Kliknięto guzik" }));
}

function loadConfig() {
    ws.send(JSON.stringify({ akcja: "wczytaj" }));
}

function saveConfig() {
    try {
        const textData = document.getElementById("configEditor").value;
        const parsedData = JSON.parse(textData);
        ws.send(JSON.stringify({ akcja: "zapisz", dane: parsedData }));
        document.getElementById("configStatus").innerText = "Wysyłam do zapisu...";
    } catch (e) {
        document.getElementById("configStatus").innerText = "BŁĄD: Nieprawidłowy format JSON!";
    }
}