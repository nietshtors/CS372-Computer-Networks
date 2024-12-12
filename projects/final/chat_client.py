# python chat_client.py alice localhost 3490

from chatui import init_windows, read_command, print_message, end_windows
import sys
import socket
import json
import threading


def usage():
    print("usage: chat_client.py prefix host port", file=sys.stderr)


packet_buffer = b''


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
        if len(packet_buffer) > 1:
            packet_len = int.from_bytes(packet_buffer[0:2])
            if len(packet_buffer) >= packet_len + 2:
                packet = packet_buffer[:packet_len + 2]
                packet_buffer = packet_buffer[packet_len + 2:]
                return packet

        data = s.recv(20)

        if len(data) == 0:
            return None

        packet_buffer += data


def runner(s):
    """Receives packets from server and displays them"""
    while True:
        packet = get_next_packet(s)
        if packet:
            data = json.loads(packet[2:].decode('UTF-8'))
            match data['type']:
                case 'chat':
                    print_message(f'{data['nick']}: {data['message']}')
                case 'join':
                    print_message(f'*** {data['nick']} has joined the chat')
                case 'leave':
                    print_message(f'*** {data['nick']} has left the chat')


def build_packet(payload: dict):
    """Builds a packet from a given payload"""
    packet = b''
    
    data = json.dumps(payload)
    payload_bytes = data.encode()
    
    len_ = len(payload_bytes)
    len_bytes = len_.to_bytes(2, "big")
    
    packet += len_bytes + payload_bytes
    return packet


def main(argv):
    try:
        prefix = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1

    init_windows()
    
    # Make the client socket and connect
    s = socket.socket()
    s.connect((host, port))
    
    payload = {
        "type": "hello",
        "nick": prefix
    }
    s.sendall(build_packet(payload))
    
    # launch thread
    t = threading.Thread(target=runner, args=(s,), daemon=True)
    t.start()
    
    while True:
        command = read_command(f'{prefix}> ')
        if command == '/q': break
        
        chat_payload = {
            "type": "chat",
            "message": command
        }
        s.sendall(build_packet(chat_payload))

    end_windows()


if __name__ == "__main__":
    sys.exit(main(sys.argv))