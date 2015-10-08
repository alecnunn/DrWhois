__author__ = 'Alec Nunn'

from sqlite3 import dbapi2 as sqlite3

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
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect('arin.db')
        top.sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db.create_function('inet_ntoa', 1, get_ip)
    return top.sqlite_db


@app.teardown_appcontext
def close_db(exception):
    """
    Close DB at end of request
    """
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def query(q, args):
    """
    Queries the DB
    """
    cursor = get_db().execute(q, args)

    def generate():
        import itertools
        field_names = [d[0].lower() for d in cursor.description]
        yield '['
        while True:
            rows = cursor.fetchmany(1000)
            if not rows:
                yield ']'
                return
            for row in rows:
                yield str(dict(itertools.izip(field_names, row))).replace('u\'', '\'') + ","
    return Response(stream_with_context(generate()))


@app.route('/org/<org>')
def route_org(org):
    return query('select inet_ntoa(ip) as ip from arin where org=?', [org])


@app.route('/ip/<ip>')
def route_ip(ip):
    return query('select inet_ntoa(ip) as ip, org from arin where ip=?', [get_dec(ip)])


@app.route('/list/<t>')
def route_list(t):
    if t == 'org':
        return query('select distinct(org) from arin', [])
    elif t == 'ip':
        return query('select inet_ntoa(ip) as ip from arin', [])
    else:
        return {'error': 'Invalid type request \'{}\''.format(t)}


if __name__ == '__main__':
    app.run(port=8080, debug=True)