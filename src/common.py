__author__ = 'Alec Nunn'

import socket
import struct

def get_ip(i):
    return socket.inet_ntoa(struct.pack('!I', int(i)))

def get_dec(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]

schema = """CREATE TABLE "orgs" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "shortname" TEXT,
    "fullname" TEXT
);
CREATE TABLE "ips" (
    "ip" INTEGER,
    "owner" INTEGER,
    "netblock" INTEGER
);
CREATE TABLE "netblocks" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "block" TEXT,
    "owner" INTEGER
);"""