__author__ = 'Alec Nunn'

import sqlite3

from flask.ext.api import FlaskAPI
from flask import _app_ctx_stack, stream_with_context, Response

from common import *


app = FlaskAPI(__name__)


def get_db():
    """
    Opens a connection to the database and returns the database as an object

    Don't forget to close the connection when you are finished please and
    thank you
    """
    sqlite_db = sqlite3.connect('test.db')
    sqlite_db.row_factory = sqlite3.Row
    sqlite_db.create_function('inet_ntoa', 1, get_ip)
    return sqlite_db


def stream_query(q, args):
    """
    Queries the DB
    """
    cursor = get_db().execute(q, args)

    def generate():
        while True:
            rows = cursor.fetchmany(1000)
            if not rows:
                return
            for row in rows:
                yield str(row[0]) + '\n'
    return Response(stream_with_context(generate()))


def query(q, args, one=False):
    cursor = get_db().execute(q, args)
    r = cursor.fetchall()
    return (r if r else None) if one else r


@app.route('/api/org/<org>')
def route_org(org):
    orginfo = query('select id, shortname, fullname from orgs where shortname=?', [org], one=True)
    if orginfo is None:
        return {"error": "Invalid organization '{}'".format(org)}
    else:
        orginfo = orginfo[0]
    netblocks = []
    for block in query('select block from netblocks where owner=? limit 25', [orginfo[0]]):
        netblocks.append(block[0])
    ips = []
    for ip in query('select inet_ntoa(ip) as `ip` from ips where owner=? limit 25', [orginfo[0]]):
        ips.append(ip[0])
    return {"orginfo": {"id": orginfo[0], "shortname": orginfo[1], "fullname": orginfo[2]}, "netblocks": netblocks, "ips": ips}


@app.route('/api/org/<org>/<action>')
def stream_org(org, action):
    if action == 'ips':
        return stream_query('select inet_ntoa(ips.ip) as `ip` from ips join orgs on ips.owner=orgs.id where orgs.shortname=?', [org])
    elif action == 'netblocks':
        return stream_query('select netblocks.block from netblocks join orgs on netblocks.owner=orgs.id where orgs.shortname=?', [org])
    else:
        return {'error': 'Invalid action \'{}\''.format(action)}

@app.route('/api/ip/<ip>')
def route_ip(ip):
    ip_q = query('select ips.owner, netblocks.block from ips join netblocks on ips.netblock=netblocks.id where ip=?', [get_dec(ip)])
    try:
        owner = query('select shortname from orgs where id=?', [ip_q[0][0]])[0][0]
    except IndexError:
        return {'error': 'The IP you requested does not have any associated data'}
    return {'owner': owner, 'ip': ip, 'netblock': ip_q[0][1]}


@app.route('/api/list/<t>')
def route_list(t):
    if t == 'org':
        return stream_query('select shortname from orgs', [])
    elif t == 'ip':
        return stream_query('select inet_ntoa(ip) as ip from ips', [])
    else:
        return {'error': 'Invalid type request \'{}\''.format(t)}


if __name__ == '__main__':
    from sys import argv, exit
    from os import remove, path
    if len(argv) > 1:
        if argv[1] == '--init':
            if path.isfile('test.db'): remove('test.db')
            get_db().executescript(schema)
            print('[+] Initialized database')
            exit()
        else:
            print('[-] Unknown command \'{}\''.format(argv))
    if not path.isfile('test.db'):
        print('You must initialize the database by using the \'--init\' option')
        exit()
    app.run(port=8080, debug=True)