import socket


class Message:
    def __init__(self, sender: str, content: str, timestamp: int,
                 msg_type: str = "UNICAST", target: str = "",
                 consumed_by: str = None, consumed_timestamp: int = None):
        self.sender = sender  # produtor
        self.content = content
        self.type = msg_type  # UNICAST, MULTICAST ou BROADCAST
        self.payload = target  # alvo da mensagem
        self.timestamp = timestamp  # carimbo lógico do produtor
        self.consumed_by = consumed_by  # consumidor
        self.consumed_timestamp = consumed_timestamp  # carimbo de consumo

    def __str__(self):
        return f"[{self.timestamp}] {self.type} de {self.sender} para {self.payload}: {self.content}"


class User:
    def __init__(self, name: str, conn: socket.socket):
        self.name = name
        self.conn = conn

    def send_message(self, message: str):
        try:
            self.conn.send(message.encode())
        except:
            self.conn.close()

class MessageBuffer:
    def __init__(self, log_file="chat_log.txt"):
        self.messages = []
        self.log_file = log_file
        # Inicializa o arquivo de log
        with open(self.log_file, 'w') as f:
            f.write("=== CHAT SERVER LOG ===\n")

    def store(self, message: Message):
        """Armazena uma mensagem no buffer e registra no log"""
        self.messages.append(message)
        self._log_store(message)

    def consume(self, message: Message, consumer: str, timestamp: int):
        """Marca uma mensagem como consumida e registra no log"""
        message.consumed_by = consumer
        message.consumed_timestamp = timestamp
        self._log_consume(message)

    def _log_store(self, message: Message):
        """Registra produção da mensagem no log"""
        with open(self.log_file, 'a') as f:
            f.write(
                f"STORE [{message.timestamp}] {message.type} FROM {message.sender} TO {message.payload}: {message.content}\n")

    def _log_consume(self, message: Message):
        """Registra consumo da mensagem no log"""
        with open(self.log_file, 'a') as f:
            f.write(
                f"CONSUME [{message.consumed_timestamp}] {message.type} BY {message.consumed_by} FROM {message.sender}: {message.content}\n")