import socket

def start_client():
    host = socket.gethostname()  # Get the host name
    port = 12345  # The same port as used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            print('Connected to server on {}:{}'.format(host, port))
            
            while True:
                message = input("Enter message to send (Type 'quit' to exit): ")
                if message.lower() == 'quit':
                    break
                client_socket.sendall(message.encode('utf-8'))
                data = client_socket.recv(1024)
                print('Received from server:', data.decode('utf-8'))

    except ConnectionRefusedError:
        print("Connection refused. Is the server running?")
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    start_client()
