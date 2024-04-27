
import socket
import threading
import tkinter as tk

def receberMensagens(sock, chat_text):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if not mensagem:
                # Se a mensagem estiver vazia, o servidor indica que o cliente se desconectou
                chat_text.insert(tk.END, "Usuário desconectado\n")
                break
            chat_text.insert(tk.END, mensagem + '\n')
        except:
            print("Ocorreu um erro na recepção das mensagens do servidor")
            break

def enviarMensagem(sock, mensagem_entry):
    mensagem = mensagem_entry.get()
    sock.sendall(str.encode(mensagem))
    if mensagem == 'sair':
        sock.close()
        root.quit()
    mensagem_entry.delete(0, tk.END)

def fecharConexao(sock):
    sock.close()
    root.quit()

# Configurações do servidor
HOST = "26.198.146.42"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectar ao servidor
sock.connect((HOST, PORT))
# Enviar nome para o servidor
nome = input("Informe o seu nome: ")
sock.sendall(str.encode(nome))

# Interface gráfica
root = tk.Tk()
root.title("Chat Cliente")

# Área de exibição das mensagens
chat_text = tk.Text(root)
chat_text.pack(padx=10, pady=10)

# Campo de entrada de mensagem
mensagem_entry = tk.Entry(root, width=50)
mensagem_entry.pack(padx=10, pady=10)

# Botão para enviar mensagem
enviar_button = tk.Button(root, text="Enviar", command=lambda: enviarMensagem(sock, mensagem_entry))
enviar_button.pack(pady=10)

# Botão para fechar conexão
fechar_button = tk.Button(root, text="Fechar Conexão", command=lambda: fecharConexao(sock))
fechar_button.pack(pady=10)

# Iniciar uma thread para receber mensagens do servidor
threadReceber = threading.Thread(target=receberMensagens, args=(sock, chat_text))
threadReceber.start()

# Função para fechar a interface gráfica quando o usuário fechar a janela
def fecharJanela():
    fecharConexao(sock)

#quando o usuário clicar no botão de fechar a janela a função fecharJanela será chamada
root.protocol("WM_DELETE_WINDOW", fecharJanela)

# Iniciar a interface gráfica
root.mainloop()