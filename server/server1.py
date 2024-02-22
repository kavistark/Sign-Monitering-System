import socket
import msg
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 12346
server_socket.bind((host, port))

server_socket.listen(5)
print('waiting...')
while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024)
    print('Received from client: %s' % data.decode('ascii'))
    if (str(data.decode())=='help'):
        msg.aleram('help')  
    client_socket.close()