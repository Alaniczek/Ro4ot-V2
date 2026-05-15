import socket

ESP_IP = "192.168.243.34" # SPRAWDŹ CZY TO NA PEWNO TEN ADRES!
ESP_PORT = 4210
KOMENDA = "A\n"

print(f"Próba wysłania '{KOMENDA.strip()}' do {ESP_IP}:{ESP_PORT}...")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Wysyłamy i liczymy ile bajtów fizycznie opuściło kartę sieciową
    wyslane_bajty = sock.sendto(KOMENDA.encode('utf-8'), (ESP_IP, ESP_PORT))
    print(f"Sukces! Wysłano {wyslane_bajty} bajtów do karty sieciowej.")
    sock.close()
except Exception as e:
    print(f"Błąd wysyłania: {e}")