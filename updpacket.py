#/usr/bin/python3
from functools import reduce
import socket

MAX_UDP_PACKET_SIZE:int = 524

#Creates the udp packet header 
def create_udp_packet_header(seq:int, ack:int, connection_id:int, ACK:bool, SYN:bool, FIN:bool):

    options = 0x0

    options |= 0b001 if FIN else 0b000
    options |= 0b010 if SYN else 0b000
    options |= 0b100 if ACK else 0b000

    udp_header = [
        #=======================================================
        (seq >> 0x18) & 0xFF, # ack part 1 FIRST FIELD
        (seq >> 0x10) & 0xFF, # ack part 2
        (seq >> 0x08) & 0xFF, # ack part 3
        (seq >> 0x00) & 0xFF, # ack part 4
        #=======================================================
        (ack >> 0x18) & 0xFF, # syn part 1 SECOND FIELD
        (ack >> 0x10) & 0xFF, # syn part 2
        (ack >> 0x08) & 0xFF, # syn part 3
        (ack >> 0x00) & 0xFF, # syn part 4
        #=======================================================
        (connection_id >> 0x08) & 0xFF,
        (connection_id >> 0x00) & 0xFF,
        0, #not used
        options
        #=======================================================
    ]

    return bytes(udp_header)

#decodes a udp packet header and returns a tuple
def decode_udp_packet_header(raw:bytes):
    
    seq = raw[3] | raw[2] << 0x08 | raw[1] << 0x10 | raw[0] << 0x18

    ack = raw[7] | raw[6] << 0x08 | raw[5] << 0x10 | raw[4] << 0x18

    conn_id = raw[9] | raw[8] << 0x08

    return (seq, ack, conn_id, (raw[11] >> 0b10 & 0x1) == 1, (raw[11] >> 0b01 & 0x1) == True, (raw[11] >> 0b00 & 0x1) == True)

#prints the header, for debugging
def print_udp_header(raw:bytes):
    print(int_to_binary(header[0], 8), end='')
    print(int_to_binary(header[1], 8), end='')
    print(int_to_binary(header[2], 8), end='')
    print(int_to_binary(header[3], 8), end='\n')

    print(int_to_binary(header[4], 8), end='')
    print(int_to_binary(header[5], 8), end='')
    print(int_to_binary(header[6], 8), end='')
    print(int_to_binary(header[7], 8), end='\n')

    print(int_to_binary(header[8], 8), end='')
    print(int_to_binary(header[9], 8), end='')
    print(int_to_binary(header[10], 8), end='')
    print(int_to_binary(header[11], 8), end='\n')

#prints an unsigned value to binary with a default size of 32 bites
def int_to_binary(value:int, size=32):
    return reduce(lambda agg, elm: str((value >> elm) & 0x1) + agg, range(size), '')
