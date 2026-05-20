const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = function(event) {
    let message = JSON.parse(event.data);

    if (message.step === 2) {
        document.getElementById("output").innerText = "JS: Otrzymałem z Pythona! Odsyłam krok 3.";

        message.step = 3;
        message.js_added = "HTML też tu był!";

        ws.send(JSON.stringify(message));
    }

    if (message.akcja === "zaladowano_config") {
        document.getElementById("configEditor").value = JSON.stringify(message.dane, null, 4);
        document.getElementById("configStatus").innerText = "Wczytano pomyślnie z serwera!";
    }

    if (message.akcja === "info") {
        document.getElementById("configStatus").innerText = message.tekst;
    }
};

function startPingPong() {
    document.getElementById("output").innerText = "JS: Wysyłam do Pythona krok 1...";

    const data = {
        step: 1,
        info: "Kliknięto guzik"
    };

    ws.send(JSON.stringify(data));
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