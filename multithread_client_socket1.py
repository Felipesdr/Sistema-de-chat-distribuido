import socket
import threading
import sys
import time

class ChatClient:
    def __init__(self, host="127.0.0.1", port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logical_clock = 0
        self.lock = threading.Lock()

        try:
            self.client.connect((host, port))

            # Iniciando conexão
            self.client.send("CONNECT".encode())

            # Resposta de aceitação da conexão
            response = self.client.recv(1024).decode()
            parts = response.split(":", 2)

            if parts[0] == "ACCEPT":
                server_timestamp = int(parts[1])
                self.update_clock(server_timestamp)
                print(f"Conexão estabelecida: {parts[2]}")
                print("-" * 40)  # Linha separadora
            else:
                print(f"Conexão recusada: {parts[1]}")
                self.client.close()
                sys.exit()

            # Pequena pausa para garantir separação das mensagens
            time.sleep(1)

            # Receber solicitação de nome em uma nova chamada
            self.client.setblocking(True)
            prompt_data = self.client.recv(1024).decode()
            prompt_parts = prompt_data.split(":", 1)
            server_timestamp = int(prompt_parts[0])
            prompt = prompt_parts[1]

            self.update_clock(server_timestamp)
            print(prompt, end="")
            self.user_name = input()

            # Enviar nome com timestamp
            timestamp = self.increment_clock()
            self.client.send(f"{timestamp}:{self.user_name}".encode())

            threading.Thread(target=self.receive_messages, daemon=True).start()
            self.send_messages()
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            sys.exit()

    def increment_clock(self):
        with self.lock:
            self.logical_clock += 1
            return self.logical_clock

    def update_clock(self, received_timestamp):
        with self.lock:
            self.logical_clock = max(self.logical_clock, received_timestamp) + 1
            return self.logical_clock

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    parts = message.split(":", 2)
                    if len(parts) >= 2:
                        server_timestamp = int(parts[0])
                        self.update_clock(server_timestamp)
                        sender = parts[1]
                        content = parts[2] if len(parts) > 2 else ""
                        print(f"\n[{server_timestamp}] {sender}: {content}")
                    else:
                        print("\n" + message)
            except:
                print("Conexão com o servidor encerrada!")
                self.client.close()
                break

    def send_messages(self):
        while True:
            print("\nOpções:")
            print("1. Enviar mensagem para um usuário (MSG:nome_usuario:mensagem)")
            print("2. Enviar mensagem para múltiplos usuários (MULTICAST:usuario1,usuario2,usuario3:mensagem)")
            print("3. Enviar mensagem para todos (BROADCAST:ALL:mensagem)")
            print("4. Sair")

            user_input = input()

            if user_input.lower() == "sair":
                self.client.close()
                break

            if ":" in user_input:
                parts = user_input.split(":", 2)
                command = parts[0]
                target = parts[1]
                content = parts[2] if len(parts) > 2 else ""

                timestamp = self.increment_clock()
                message = f"{timestamp}:{command}:{target}:{content}"
                self.client.send(message.encode())
            else:
                print("Formato inválido. Use COMANDO:ALVO:MENSAGEM")


if __name__ == "__main__":
    ChatClient()