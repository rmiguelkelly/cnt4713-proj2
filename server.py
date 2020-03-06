
import sys
import socket
import updpacket

ERROR_EXIT_CODE = 0
RECV_BUFFER_SIZE = 4096

#Creates a UDP socket that is bound to an endpoint
def create_udp_socket(host = '127.0.0.1', port = 3333):
    
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if port < 0 and port > 65536:
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
        (buffer, _) = socket.recvfrom(RECV_BUFFER_SIZE)
        print(str(buffer, 'utf-8'))

        file_index += 1

if __name__ == "__main__":
    socket = create_udp_socket(host="localhost", port=3333)

    print("Starting server...")
    run_udp_server(socket)
