
import sys
import socket

ERROR_EXIT_CODE = 0

#Creates a UDP socket that is bound to an endpoint
def create_udp_socket():
    
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)

    return client

if __name__ == "__main__":
    socket = create_udp_socket()
    
    endpoint = ('localhost', 3333)
    
    socket.sendto("hello".encode('utf-8'), endpoint)

    socket.close()