import socket
import sys

s = socket.socket()

port = 80
if len(sys.argv) > 1:
    addr = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
else:
    addr = 'localhost'

remote = (addr, port)

s.connect(remote)

req = (
    'GET / HTTP/1.1\r\n'
    f'Host: {addr}\r\n'
    'Connection: close\r\n\r\n'
)

s.sendall(req.encode())

while True:
    data = s.recv(4096)
    print(data.decode())
    if len(data) == 0:
        break

s.close()
