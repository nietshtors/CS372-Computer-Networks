NUMFILES = 10


def ip_to_bytes(ip):
    return b''.join([int(n).to_bytes(1) for n in ip.split('.')])


def checksum(pseudo_header, tcp_data):
    data = pseudo_header + tcp_data

    total = 0
    offset = 0   # byte offset into data

    while offset < len(data):
        # Slice 2 bytes out and get their value:
        word = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2   # Go to the next 2-byte value

        total += word
        total = (total & 0xffff) + (total >> 16)  # carry around

    return (~total) & 0xffff  # one's complement


for i in range(NUMFILES):
    # 1: Read in the tcp_addrs_0.txt file.
    with open(f'tcp_data/tcp_addrs_{i}.txt', 'r') as f:
        # 2: Split the line in two, the source and destination addresses.
        source, dest = f.read().split()

    # 3: Write a function that converts the dots-and-numbers IP addresses into
    #    bytestrings.
    source = ip_to_bytes(source)
    dest = ip_to_bytes(dest)

    # 4: Read in the tcp_data_0.dat file.
    with open(f'tcp_data/tcp_data_{i}.dat', 'rb') as f:
        tcp_data = f.read()
        tcp_len = len(tcp_data)

    # 5: Write a function that generates the IP pseudo header bytes from the
    #    IP addresses from tcp_addrs_0.txt and the TCP length from the
    #    tcp_data_0.dat file.
    pseudoheader = source + dest + b'\x00\x06' + tcp_len.to_bytes(2)
    # print(pseudoheader.hex(' '))

    # 6: Build a new version of the TCP data that has the checksum set to zero.
    tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]

    # 7: Concatenate the pseudo header and the TCP data with zero checksum.
    if len(tcp_zero_cksum) % 2 == 1:
        tcp_zero_cksum += b'\x00'

    # 8: Compute the checksum of that concatenation
    cksum = checksum(pseudoheader, tcp_zero_cksum).to_bytes(2)

    # 9: Extract the checksum from the original data in tcp_data_0.dat.
    og_cksum = tcp_data[16:18]
    # 10: Compare the two checksums. If they’re identical, it works!
    print('PASS' if cksum == og_cksum else 'FAIL')
