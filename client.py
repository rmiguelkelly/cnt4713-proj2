
import sys
import socket
import updpacket

ERROR_EXIT_CODE = 0

#Creates a UDP socket that is bound to an endpoint
def create_udp_socket():
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    client.settimeout(10.0)
    return client

def get_file(filename:str):
    try:
        file = open(filename, 'rb')
        return file
    except Exception:
        sys.stderr.write("ERROR: unable to open file")
        sys.exit(ERROR_EXIT_CODE)

def perform_handshake_client(sock:socket.socket, dest):

    pass

def send_file_to_socket(path:str, socket: socket.socket, address):
    file = get_file(path)

    sequence_number = 0

    print("sending file")
    udp_header = updpacket.create_udp_packet_header(sequence_number, 0x00,  0, False, False, False)
    buffer = file.read(updpacket.MAX_UDP_PACKET_SIZE)
    socket.sendto(udp_header + buffer, address)
    sequence_number += 1

    while len(buffer) > 0:
        udp_header = updpacket.create_udp_packet_header(sequence_number, 0x00,  0, False, False, False)
        buffer = file.read(updpacket.MAX_UDP_PACKET_SIZE)
        socket.sendto(udp_header + buffer, address)
        print("sending file")
        sequence_number += 1
    
    final_packet = updpacket.create_udp_packet_header(sequence_number + 1, 0x00,  0, False, False, True)
    socket.sendto(final_packet, address)

    socket.close()
    file.close()

if __name__ == "__main__":
    socket = create_udp_socket()

    if (len(sys.argv) != 4):
        sys.stderr.write("ERROR: Invalid argument list\n")
        sys.exit(ERROR_EXIT_CODE)

    port = int(sys.argv[2])
    if (port <= 0 or port >= 65535):
        sys.stderr.write("ERROR: Port should be between 0 and 65535\n")
        exit(-1)
    
    endpoint = (sys.argv[1], port)

    #perform_handshake_client(socket, endpoint)
    
    try:
        send_file_to_socket(sys.argv[3], socket, endpoint)
    except:
        sys.stderr.write("ERROR: unable to send file to remote host\n")

    socket.close()


 