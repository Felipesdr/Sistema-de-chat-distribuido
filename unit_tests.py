import unittest
import socket
import threading
import time
import os
from multithread_server_socket import ChatServer
from deitel_comm import Message, MessageBuffer

class TestChatComponents(unittest.TestCase):
    def setUp(self):
        # Limpa o arquivo de log entre testes
        open("chat_log.txt", "w").close()

    def test_message_creation(self):
        msg = Message("user1", "hello", 1, "UNICAST", "user2")
        self.assertEqual(msg.sender, "user1")
        self.assertEqual(msg.timestamp, 1)
        self.assertEqual(msg.type, "UNICAST")

    def test_message_buffer(self):
        buffer = MessageBuffer("test_log.txt")
        msg = Message("user1", "hello", 1, "UNICAST", "user2")

        # Teste armazenamento
        buffer.store(msg)
        self.assertEqual(len(buffer.messages), 1)

        # Teste consumo
        buffer.consume(msg, "user2", 2)
        self.assertEqual(msg.consumed_by, "user2")
        self.assertEqual(msg.consumed_timestamp, 2)

        # Limpeza
        if os.path.exists("test_log.txt"):
            os.remove("test_log.txt")

