import socket
import updpacket

server_seq = 4321
conn_id = 1

def perform_server_handshake(sock:socket.socket):
    (buff1, addr1) = sock.recvfrom(524)
    packbuff1 = updpacket.decode_udp_packet_header(buff1)
    print("one")

    pack1 = updpacket.create_udp_packet_header(server_seq, packbuff1[1], conn_id, True, True, False)
    sock.sendto(pack1, addr1)

    (buff2, addr2) = sock.recvfrom(524)
    packbuff2 = updpacket.decode_udp_packet_header(buff2)
    print("two")

    print(packbuff2)


server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 3030))

perform_server_handshake(server)
