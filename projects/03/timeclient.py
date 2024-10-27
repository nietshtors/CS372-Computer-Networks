import socket
import time

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch


HOST = 'time.nist.gov'
PORT = 37
with socket.socket() as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(4096)
        if data:
            break
nist = int.from_bytes(data)
syst = system_seconds_since_1900()

print(f'NIST time  : {nist}')
print(f'System time: {syst}')
