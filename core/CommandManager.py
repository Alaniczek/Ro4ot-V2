import json
import socket

class CommandManager:
    def __init__(self, device_ip : str, device_port : int, command_list_path : str):
        self.device_ip = device_ip
        self.device_port = device_port
        self.command_list_path = command_list_path
        self.command_list : dict = []

    def change_device_settings(self, new_ip : str, new_port : int):
        self.device_ip = new_ip
        self.device_port = new_port
    def change_command_list_path(self, new_path : str):
        self.command_list_path = new_path

    def load_command_list(self):
        with open(self.command_list_path, 'r') as file:
            self.command_list = json.load(file)
        return self.command_list

    def get_command_list(self):
        return self.command_list

    def send_command(self, cmd : str):
        print(f"snd : {cmd}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(cmd.encode(), (self.device_ip, self.device_port))
        # sock.sendto((cmd + "\n").encode('utf-8'), (self.device_ip, self.device_port))
        sock.close()


Tester = CommandManager("192.168.243.34", 4210, "komendy.json")

while True:
    cmd = input("GiveCommand: ")
    if cmd == 'exit':
        break
    Tester.send_command(cmd)