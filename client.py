import socket

s = socket.socket()

remote = ("localhost", 33490)

s.connect(remote)

while (data := s.recv(100)) != b'':
    print(data.decode(), end='')
    
s.close()