import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


addr = ('', 28333) if len(sys.argv) == 1 else ('', int(sys.argv[1]))
s.bind(addr)
s.listen()
print(f'Listening on port {addr[1]}')

try:
    while True:
        client_socket, client_address = s.accept()

        print(f'Got connection from {client_address}')

        data = ''
        while data != '\r\n\r\n':
            data = client_socket.recv(4096)
            print(data.decode())

        response = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/plain\r\n'
            'Content-Length: 6\r\n'
            'Connection: close\r\n'
            '\r\n\r\n'
            'Hello!\r\n'
        )

        client_socket.sendall(response.encode())

        client_socket.close()
except KeyboardInterrupt:
    print('quit')
    s.close()
