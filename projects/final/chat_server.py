import json
import sys
import socket
import select


packet_buffer = {}


def get_next_packet(s):
    """
    Return the next packet from the stream.

    The packet consists of the encoded payload length followed by the
    UTF-8-encoded payload.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """

    global packet_buffer

    while True:
        if len(packet_buffer[s]) > 1:
            packet_len = int.from_bytes(packet_buffer[s][0:2])
            if len(packet_buffer[s]) >= packet_len + 2:
                packet = packet_buffer[s][:packet_len + 2]
                packet_buffer[s] = packet_buffer[s][packet_len + 2:]
                return packet

        try:
            data = s.recv(20)
        except Exception:
            return None

        if len(data) == 0:
            return None

        packet_buffer[s] += data


def build_packet(payload: dict):
    """Builds a packet from a given payload"""
    packet = b''
    
    data = json.dumps(payload)
    payload_bytes = data.encode()
    
    len_ = len(payload_bytes)
    len_bytes = len_.to_bytes(2, "big")
    
    packet += len_bytes + payload_bytes
    return packet


def broadcast(set, payload):
    for s in set: s.sendall(build_packet(payload))


def run_server(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    addr = ('localhost', port)
    s.bind(addr)
    s.listen()
    print('waiting for connections')
    read_set = [s]
    nicks = {}
    global packet_buffer
    try:
        while True:
            ready_to_read, _, _ = select.select(read_set, {}, {})
            for s in ready_to_read:
                if s == read_set[0]:
                    client_socket, client_address = s.accept()
                    print(f'{client_address}: connected')
                    read_set.append(client_socket)
                    packet_buffer[client_socket] = b''
                elif s in read_set:
                    packet = get_next_packet(s)
                    if packet:
                        data = json.loads(packet[2:].decode('UTF-8'))
                        match data['type']:
                            case 'chat':
                                print(f'{nicks[s]}: {data['message']}')
                                payload = {
                                    "type": "chat",
                                    "nick": nicks[s],
                                    "message": data['message']
                                }
                                broadcast(read_set[1:], payload)
                            case 'hello':
                                nicks[s] = data['nick']
                                print(f'{nicks[s]} joined')
                                payload = {
                                    "type": "join",
                                    "nick": data['nick']
                                }
                                broadcast(read_set[1:], payload)
                    else: 
                        print(f'{nicks[s]}: disconnected')
                        read_set.remove(s)
                        payload = {
                            "type": "leave",
                            "nick": nicks[s]
                        }
                        broadcast(read_set[1:], payload)
                        nicks.pop(s)
    except KeyboardInterrupt:
        read_set[0].close()


def usage():
    print("usage: chat_server.py port", file=sys.stderr)


def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))