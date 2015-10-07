__author__ = 'Alec Nunn'

import socket
import struct

def get_ip(i):
    return socket.inet_ntoa(struct.pack('!I', int(i)))

def get_dec(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]
