import socket
import updpacket

class udpclient:
    def __init__(self, addr = '127.0.0.1', port):
        self.address = addr
        self.port = port
        self.seq_num = 42
        
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
        self.client.settimeout(10.0)

        self.packet_state = updpacket.create_udp_packet_header(self.seq_num, 0, 0, False, True, False)
    
    def perform_handshake(self):
        


seq_initial = 42

def perform_client_handshake(sock: socket.socket, addr, seq):
    
    pack1 = updpacket.create_udp_packet_header(seq, 0, 0, False, True, False)
    sock.sendto(pack1, addr)

    (buff1, addr1) = sock.recvfrom(524)
    resp1 = updpacket.decode_udp_packet_header(buff1)

    seq += 1

    pack2 = updpacket.create_udp_packet_header(resp1[0], seq, resp1[2], True, True, False)
    sock.sendto(pack2, addr1)


client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
client.settimeout(10.0)

endpoint = ('localhost', 3030)

perform_client_handshake(client, endpoint, seq_initial)