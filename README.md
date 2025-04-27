# Sistema de Chat Distribuído

Este projeto foi desenvolvido como requisito para conclusão da disciplina de Computação Paralela e Distribuída. Trata-se de um sistema de chat distribuído que implementa conceitos fundamentais de sistemas paralelos e distribuídos, como comunicação via sockets, multithreading, sincronização e relógios lógicos.

## Descrição do Projeto

O sistema permite que múltiplos clientes se conectem a um servidor central e troquem mensagens em tempo real. O sistema suporta três tipos de comunicação:

- **Unicast**: Envio de mensagens para um usuário específico
- **Multicast**: Envio de mensagens para um grupo selecionado de usuários
- **Broadcast**: Envio de mensagens para todos os usuários conectados

## Características Técnicas

- **Arquitetura Cliente-Servidor**: Implementação com sockets TCP/IP
- **Multithreading**: Cada cliente conectado é gerenciado por uma thread independente no servidor
- **Relógios Lógicos**: Implementação do algoritmo de Lamport para ordenação de eventos
- **Buffer de Mensagens**: Armazenamento e rastreamento de mensagens trocadas
- **Log Persistente**: Registro de todas as operações (produção e consumo de mensagens)
- **Sincronização**: Uso de locks para acessar recursos compartilhados

## Componentes do Sistema

- `multithread_server_socket.py`: Implementação do servidor multithreaded
- `multithread_client_socket.py`: Implementação do cliente com threads para envio e recebimento simultâneos
- `deitel_comm.py`: Classes auxiliares (Message, User, MessageBuffer)
- `chat_log.txt`: Arquivo de log que registra todas as operações do sistema

## Como Executar

1. Inicie o servidor:
```bash
python multithread_server_socket.py
```

2. Inicie um ou mais clientes (em terminais separados):
```bash
python multithread_client_socket.py
```

3. No cliente, siga as instruções para se conectar e enviar mensagens:
   - Para enviar mensagem privada: `MSG:nome_usuario:conteudo`
   - Para enviar para múltiplos usuários: `MULTICAST:usuario1,usuario2:conteudo`
   - Para enviar para todos: `BROADCAST:ALL:conteudo`

## Protocolo de Testes

O projeto inclui um conjunto de testes para verificar sua funcionalidade:
- Testes unitários para componentes individuais
- Testes de integração simulando múltiplos clientes
- Verificação de log para garantir consistência nas mensagens
- Testes de carga para avaliar o desempenho sob estresse

## Conceitos Aplicados de Computação Distribuída

- **Comunicação Assíncrona**: Clientes podem enviar e receber mensagens independentemente
- **Relógios Lógicos**: Garantem ordenação causal das mensagens
- **Consistência**: As mensagens são entregues na ordem correta para todos os destinatários
- **Tolerância a Falhas**: O sistema gerencia desconexões de clientes
- **Concorrência**: Múltiplos clientes são atendidos simultaneamente

## Requisitos

- Python 3.6 ou superior
- Bibliotecas padrão do Python (socket, threading, time, sys)

## Conclusão

Este projeto demonstra a aplicação prática de conceitos fundamentais de computação paralela e distribuída, como comunicação entre processos, sincronização, ordenação de eventos distribuídos e gerenciamento de concorrência.

A implementação de um sistema de chat distribuído com múltiplas funcionalidades permite visualizar os desafios e soluções típicos de sistemas distribuídos reais, como garantia de ordem, consistência e tolerância a falhas.
