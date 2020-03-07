#/usr/bin/python3

import sys
import socket
import updpacket

ERROR_EXIT_CODE = 0

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

def run_udp_server(socket: socket.socket):

    is_running = True

    file_index = 0
    
    while is_running:

        file = open("/Users/ronankelly/Desktop/data/{}.txt".format(file_index), 'wb')

        (buffer, _) = socket.recvfrom(updpacket.MAX_UDP_PACKET_SIZE)
        print(len(buffer))
        file.write(buffer[12:])
        
        while (len(buffer) > 12):
            (next, _) = socket.recvfrom(updpacket.MAX_UDP_PACKET_SIZE)
            buffer = next
            file.write(buffer[12:])
            print(len(buffer))
        
        print("Created File")
        file.close()
        
        file_index += 1

if __name__ == "__main__":
    socket = create_udp_socket(host="localhost", port=3333)

    print("Starting server...")
    run_udp_server(socket)
