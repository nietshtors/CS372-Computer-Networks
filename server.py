import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


addr = ('localhost', 33490)
s.bind(addr)
s.listen()
print(f'Listening on port {addr[1]}')

try:
    while True:
        client_socket, client_address = s.accept()
        
        print(f'Got connection from {client_address}')
        
        client_socket.sendall('Hi there!\n'.encode())
        client_socket.close()
except KeyboardInterrupt:
    print('quit')
    s.close()