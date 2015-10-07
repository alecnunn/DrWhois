__author__ = 'Alec Nunn'
__version__ = '0.0.4'

import requests

import json
import sqlite3
import socket
import struct
import sys

import argparse
parser = argparse.ArgumentParser(description='NetChop is built on top of NetCut and is used to scan the entire IP range of a given network (in CIDR notation).')
parser.add_argument('-i', '--input', help='Input file, each line being a net-block in CIDR notation')
parser.add_argument('--init', action='store_true', help='Initialize the database')
parser.add_argument('-key', '--apikey', help='API Key for ARIN API access')
args = parser.parse_args()


init = args.init
inputfile = args.input
apikey = args.apikey

def ipToDec(ip):
    return struct.unpack('!I', socket.inet_aton(str(ip)))[0]

def get_db():
    return sqlite3.connect('arin.db', isolation_level=None)

def init_db():
    db = get_db()
    db.executescript("create table 'arin' ('ip' integer, 'org' text);")
    db.close()

def query(q, args=(), one=False):
    cur = get_db().execute(q, args)
    r = cur.fetchall()
    return (r[0] if r else None) if one else r

def insert(ip, org):
    return query('insert into arin values (?, ?)', [ipToDec(ip), org])

def ArinLookup(ip):
    r = requests.get('http://whois.arin.net/rest/ip/{0}.json?apikey={1}'.format(ip, apikey))
    j = json.loads(unicode(r.text))
    if 'orgRef' in r.text:
        orgName = j['net']['orgRef']['@handle']
    elif 'customerRef' in r.text:
        orgName = j['net']['customerRef']['@handle']
    else:
        print('{} is broken'.format(ip))
    return insert(ip, orgName)


class Printer():
    def __init__(self, data):
        sys.stdout.write('\r\x1b[K' + data.__str__())
        sys.stdout.flush()

def netchop():
    with open(inputfile) as f:
        for i, line in enumerate(f):
            ArinLookup(line.rstrip('\r\n'))
            Printer('{} IPs processed!'.format(str(i)))

if __name__ == '__main__':
    if len(sys.argv) < 1:
        parser.print_help()
        sys.exit()
    else:
        if init:
            init_db()
            sys.exit()
        if inputfile:
            netchop()