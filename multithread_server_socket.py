import socket
import threading
from typing import Dict, List
from deitel_comm import Message, User, MessageBuffer


class ChatServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.users: Dict[str, User] = {}
        self.logical_clock = 0
        self.message_buffer = MessageBuffer()
        self.lock = threading.Lock()

    def increment_clock(self):
        with self.lock:
            self.logical_clock += 1
            return self.logical_clock

    def update_clock(self, received_timestamp):
        with self.lock:
            self.logical_clock = max(self.logical_clock, received_timestamp) + 1
            return self.logical_clock

    def handle_client(self, conn, addr):
        try:
            # Protocolo de conexão
            connect_request = conn.recv(1024).decode().strip()

            if not connect_request.startswith("CONNECT"):
                conn.send("REJECT:Protocolo inválido".encode())
                return

            conn.send(f"ACCEPT:{self.increment_clock()}:Bem-vindo ao servidor".encode())

            # Obter nome do usuário
            conn.send(f"{self.increment_clock()}:Digite seu nome: ".encode())
            name_data = conn.recv(1024).decode().strip()
            name_parts = name_data.split(":", 1)
            client_timestamp = int(name_parts[0])
            name = name_parts[1]

            # Atualiza relógio
            timestamp = self.update_clock(client_timestamp)

            user = User(name, conn)
            self.users[name] = user
            print(f"{name} entrou no chat. Timestamp: {timestamp}")

            # Envia lista de usuários conectados
            users_list = ", ".join(self.users.keys())
            user.send_message(f"{self.increment_clock()}:Sistema:Usuários conectados: {users_list}")

            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                parts = data.split(":", 3)
                if len(parts) < 3:
                    continue

                client_timestamp = int(parts[0])
                command = parts[1]
                target = parts[2]
                content = parts[3] if len(parts) > 3 else ""

                timestamp = self.update_clock(client_timestamp)

                if command == "MSG":  # Unicast
                    if target in self.users:
                        receiver = self.users[target]
                        msg = Message(name, content, timestamp, "UNICAST", target)
                        self.message_buffer.store(msg)

                        consume_timestamp = self.increment_clock()
                        receiver.send_message(f"{consume_timestamp}:{name}:{content}")
                        self.message_buffer.consume(msg, target, consume_timestamp)
                    else:
                        user.send_message(f"{self.increment_clock()}:Sistema:Usuário não encontrado.")

                elif command == "MULTICAST":  # Multicast para usuários específicos
                    targets = target.split(",")
                    valid_targets = [t for t in targets if t in self.users]

                    if valid_targets:
                        msg = Message(name, content, timestamp, "MULTICAST", target)
                        self.message_buffer.store(msg)

                        for target_name in valid_targets:
                            if target_name != name:  # Não enviar para o próprio remetente
                                receiver = self.users[target_name]
                                consume_timestamp = self.increment_clock()
                                receiver.send_message(f"{consume_timestamp}:{name} (multicast):{content}")
                                self.message_buffer.consume(msg, target_name, consume_timestamp)

                        # Avisa quantos receberam
                        user.send_message(
                            f"{self.increment_clock()}:Sistema:Mensagem enviada para {len(valid_targets)} usuário(s)")
                    else:
                        user.send_message(f"{self.increment_clock()}:Sistema:Nenhum destinatário válido encontrado.")

                elif command == "BROADCAST":  # Broadcast para todos
                    msg = Message(name, content, timestamp, "BROADCAST", "ALL")
                    self.message_buffer.store(msg)

                    for receiver_name, receiver in self.users.items():
                        if receiver_name != name:  # Não enviar para o próprio remetente
                            consume_timestamp = self.increment_clock()
                            receiver.send_message(f"{consume_timestamp}:{name} (broadcast):{content}")
                            self.message_buffer.consume(msg, receiver_name, consume_timestamp)

                    # Confirma o broadcast
                    user.send_message(
                        f"{self.increment_clock()}:Sistema:Mensagem enviada para todos ({len(self.users) - 1} usuário(s))")

        except Exception as e:
            print(f"Erro na conexão: {e}")
        finally:
            if 'name' in locals() and name in self.users:
                print(f"{name} desconectado.")
                del self.users[name]
            conn.close()

    def run(self):
        print("Servidor distribuído rodando com relógio lógico...")
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    server = ChatServer()
    server.run()