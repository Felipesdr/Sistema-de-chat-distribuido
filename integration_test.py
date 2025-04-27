import socket
import threading
import time

class TestClient:
    def __init__(self, username, host="127.0.0.1", port=12345):
        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messages_received = []
        self.connected = False
        self.logical_clock = 0

    def connect(self):
        try:
            self.client.connect(("127.0.0.1", 12345))
            self.client.send("CONNECT".encode())

            # Processamento da conexão
            response = self.client.recv(1024).decode()
            if not response.startswith("ACCEPT"):
                raise Exception(f"Falha na conexão: {response}")

            # Receber prompt de nome
            prompt = self.client.recv(1024).decode()

            # Enviar nome
            self.logical_clock += 1
            self.client.send(f"{self.logical_clock}:{self.username}".encode())

            # Iniciar thread para receber mensagens
            self.receiver_thread = threading.Thread(target=self.receive_messages)
            self.receiver_thread.daemon = True
            self.receiver_thread.start()

            # Aguardar mensagem de boas-vindas
            time.sleep(0.5)
            self.connected = True
            return True
        except Exception as e:
            print(f"Erro ao conectar {self.username}: {e}")
            return False

    def send_message(self, command, target, content):
        if not self.connected:
            return False

        self.logical_clock += 1
        message = f"{self.logical_clock}:{command}:{target}:{content}"
        try:
            self.client.send(message.encode())
            return True
        except:
            print(f"Erro ao enviar mensagem de {self.username}")
            return False

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message:
                    self.messages_received.append(message)
            except:
                break

    def disconnect(self):
        if self.connected:
            self.client.close()
            self.connected = False


def run_integration_test():
    print("Iniciando testes de integração...")

    # Iniciar servidor em uma thread separada (se não estiver rodando)
    # Aqui você pode optar por iniciar o servidor manualmente antes do teste

    # Criar e conectar clientes de teste
    client1 = TestClient("TestUser1")
    client2 = TestClient("TestUser2")
    client3 = TestClient("TestUser3")

    clients = [client1, client2, client3]

    # Conectar clientes
    print("Conectando clientes...")
    for client in clients:
        if client.connect():
            print(f"{client.username} conectado")
        else:
            print(f"Falha ao conectar {client.username}")
            return

    time.sleep(1)  # Aguardar conexões estabilizarem

    # Teste 1: Unicast
    print("\nTestando UNICAST...")
    client1.send_message("MSG", "TestUser2", "Mensagem unicast de teste")
    time.sleep(0.5)

    # Teste 2: Multicast
    print("\nTestando MULTICAST...")
    client2.send_message("MULTICAST", "TestUser1,TestUser3", "Mensagem multicast de teste")
    time.sleep(0.5)

    # Teste 3: Broadcast
    print("\nTestando BROADCAST...")
    client3.send_message("BROADCAST", "ALL", "Mensagem broadcast de teste")
    time.sleep(0.5)

    # Verificar mensagens recebidas
    for client in clients:
        print(f"\nMensagens recebidas por {client.username}:")
        for msg in client.messages_received:
            print(f"  - {msg}")

    # Desconectar clientes
    for client in clients:
        client.disconnect()

    print("\nTestes de integração concluídos.")


if __name__ == "__main__":
    run_integration_test()