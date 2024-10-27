import socket
import sys
import os

MIME = {
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.pdf': 'application/pdf',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '': 'application/octet-stream'
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


addr = ('', 33490) if len(sys.argv) == 1 else ('', int(sys.argv[1]))
s.bind(addr)
s.listen()
print(f'Listening on port {addr[1]}')
# http://localhost:33490/file.txt
# http://localhost:33490/file1.txt
# http://localhost:33490/file2.html

try:
    while True:
        client_socket, client_address = s.accept()
        # client_socket.settimeout(5)

        print(f'Got connection from {client_address}')

        d = ''
        dat = b''
        while dat.find(b'\r\n\r\n') == -1:
            dat = client_socket.recv(4096)
            d += dat.decode("ISO-8859-1")

        d = d.split('\r\n')
        path = d[0].split(' ')[1]
        file_name = os.path.split(path)[-1]
        ext = os.path.splitext(file_name)[-1]

        try:
            with open(file_name, 'rb') as f:
                data = f.read()
            code = '200 OK'
            con_type = MIME[ext]
        except:
            data = b'404 not found'
            code = '404 Not Found'
            con_type = 'text/plain'

        response = (
            f'HTTP/1.1 {code}\r\n'
            f'Content-Type: {con_type}\r\n'
            f'Content-Length: {len(data)}\r\n'
            'Connection: close\r\n'
            '\r\n\r\n'
        )
        response = response.encode("ISO-8859-1") + data

        client_socket.sendall(response)

        client_socket.close()
except KeyboardInterrupt:
    print('quit')
    s.close()
