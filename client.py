
import sys
import socket

ERROR_EXIT_CODE = 0
SEND_BUFFER_SIZE = 4096

FILEPATH = "C:/Users/rkelly/Desktop/quotes/Quotation #0221944508 - DEPT OF TRANSPORTATION.PDF"

#Creates a UDP socket that is bound to an endpoint
def create_udp_socket():
    
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    return client

def get_file(filename:str):
    try:
        file = open(filename, 'rb')
        return file
    except Exception:
        sys.stderr.write("ERROR: unable to open file")
        sys.exit(ERROR_EXIT_CODE)

def send_file_to_socket(path:str, socket: socket.socket, address):
    file = get_file(path)

    buffer = file.read(SEND_BUFFER_SIZE)

    socket.sendto(buffer, address)

    while (len(buffer) > 0):
        buffer = file.read(SEND_BUFFER_SIZE)
        socket.sendto(buffer, address)


if __name__ == "__main__":
    socket = create_udp_socket()
    
    endpoint = ('localhost', 3333)
    
    send_file_to_socket(FILEPATH, socket, endpoint)

    socket.close()

 