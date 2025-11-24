from socket import *
import sys

# Importa o módulo socket
# Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
serverSocket.bind(('', 6789))
serverSocket.listen(1)

while True:
    # Estabelece a conexão
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    
    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:], encoding="utf-8")
        outputdata = f.read()
        
        # Envia a linha de status do cabeçalho HTTP
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        
        # Envia o conteúdo do arquivo ao cliente linha por linha
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        
        connectionSocket.send("\r\n".encode())
        
        # Fecha a conexão com o cliente
        connectionSocket.close()
        f.close()
        
    except IOError:
        # Envia mensagem de erro 404 se o arquivo não for encontrado
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<h1>404 Not Found</h1>".encode())
        
        # Fecha o socket do cliente
        connectionSocket.close()

# Fecha o socket do servidor
serverSocket.close()
sys.exit()
