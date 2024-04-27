import socket
import threading

# Lista para armazenar os sockets dos clientes conectados
clientes_conectados = []
historico_mensagens = []

# Função para enviar mensagens para todos os clientes conectados
def enviarParaTodos(mensagem):
    for cliente in clientes_conectados:
        try:
            cliente.sendall(mensagem.encode())
        except:
            print(f"Ocorreu um erro no envio de mensagem para {cliente}")
            cliente.close()
            clientes_conectados.remove(cliente)

# Função para lidar com o novo cliente conectado
def novoCliente(conn, ender):
    try:
        # aqui eu recebo o nome
        nome = conn.recv(50).decode()
    except:
        print("erro ao receber o nome... fechando conexão")
        return

    print(f"{nome} entrou no chat, IP: {ender[0]}, PORTA: {ender[1]} \n \n")
    enviarParaTodos(f"{nome} entrou no chat")

    # Enviar histórico de mensagens para o novo cliente
    for mensagem in historico_mensagens:
        conn.sendall(mensagem.encode())

    # Loop de recebimento de mensagens que ficará rodando na thread
    while True:
        try:
            mensagem = conn.recv(1024).decode()
        except:
            print("Ocorreu algum erro na recepção dos dados, encerrando conexão.")
            clientes_conectados.remove(conn)
            break

        if mensagem == 's':
            print(f"{nome} saiu do chat")
            enviarParaTodos(f"{nome} saiu do chat")
            conn.close()
            clientes_conectados.remove(conn)
            break

        msgNome = nome + " >> " + mensagem
        print(msgNome)
        enviarParaTodos(msgNome)
        historico_mensagens.append(msgNome)

# Configurações do servidor
HOST = "26.198.146.42"
PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
print(f"O Servidor {HOST}:{PORT} está aguardando conexões")

# Loop principal para aceitar novas conexões
while True:
    try:
        conn, ender = sock.accept()
    except:
        print('Ocorreu um erro durante o ACCEPT() na conexão com um novo usuário')
        continue

    # Adicionar o novo cliente conectado à lista
    clientes_conectados.append(conn)
    # Iniciar uma thread para lidar com o novo cliente
    threadNovoCliente = threading.Thread(target=novoCliente, args=(conn, ender))
    threadNovoCliente.start()