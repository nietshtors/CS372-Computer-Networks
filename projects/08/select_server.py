# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s = socket.socket()

    addr = ('localhost', port)
    s.bind(addr)
    s.listen()
    print('waiting for connections')
    read_set = [s]
    try:
        while True:
            ready_to_read, _, _ = select.select(read_set, {}, {})
            for s in ready_to_read:
                if s == read_set[0]:
                    client_socket, client_address = s.accept()
                    print(f'{client_address}: connected')
                    read_set.append(client_socket)
                elif s in read_set:
                    data = s.recv(4096)
                    if data: print(f'{s.getpeername()}: {len(data):2d} bytes {data}')
                    else: print(f'{s.getpeername()}: disconnected'); read_set.remove(s)
    except KeyboardInterrupt:
        read_set[0].close()

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
