#/usr/bin/python3

import sys
import socket
import updpacket
import signal
import os

ERROR_EXIT_CODE = 0

def perform_handshake_server(socket:socket.socket):
    ip = updpacket.decode_udp_packet_header(socket.recvfrom(12))
    initial_res = updpacket.create_udp_packet_header(42, 0, 0, False, True, False)


#Creates a UDP socket that is bound to an endpoint
def create_udp_socket(host = '127.0.0.1', port = 3333):
    
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if port < 0 and port > 65535:
        sys.stderr.write("ERROR: port is out of range")
        sys.exit(ERROR_EXIT_CODE)

    try:
        server.bind((host, port))
    except Exception:
        sys.stderr.write("ERROR: Invalid hostname")
        sys.exit(ERROR_EXIT_CODE)

    return server

def run_udp_server(sock: socket.socket, path:str):

    if (os.path.exists(path) == False):
        print("fuck")
        os.mkdir(path)

    file_index = 0
    while True:

        (buffer, _) = sock.recvfrom(524)

        write_path = os.path.join(path, '{}.file'.format(file_index))
        file = open(write_path, 'wb')
        file.write(buffer[12:])

        while (len(buffer) > 12):
            (next, _) = sock.recvfrom(524)
            buffer = next
            file.write(buffer[12:])

        file.close()
        print("file created")

        file_index += 1

if __name__ == "__main__":

    if (len(sys.argv) != 3):
        sys.stderr.write("ERROR: Invalid argument list\n")
        sys.exit(ERROR_EXIT_CODE)

    socket = create_udp_socket(host='', port=int(sys.argv[1]))

    run_udp_server(socket, sys.argv[2])
