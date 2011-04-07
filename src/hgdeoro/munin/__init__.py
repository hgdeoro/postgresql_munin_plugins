"""
PostgreSql plugins for Munin
Copyright Horacio G. de Oro <hgdeoro@gmail.com> 2011
Licenced under GPL v2.
"""

import os

def format_multiline(multi_line_string):
    """Returns a new string, with NO emtpy lines, and with each line trim()'ed"""
    multi_line_string = multi_line_string.strip()
    multi_line_string = [line.strip() for line in multi_line_string.splitlines() if line.strip()]
    return '\n'.join(multi_line_string)

def connect():
    """Connects to the DB and returns the conection object"""
    pg_host = os.environ.get('pg_host', 'localhost')
    pg_port = os.environ.get('pg_port', '5432')
    pg_db_connect = os.environ.get('pg_db_connect', 'template1')
    pg_user = os.environ.get('pg_user', 'postgres')
    pg_passwd = os.environ.get('pg_passwd')
    
    conn_string = "host='%s' dbname='%s' user='%s' port='%s' password='%s'" % (
        pg_host, pg_db_connect, pg_user, pg_port, pg_passwd, )
    
    try:
        import psycopg2
        return psycopg2.connect(conn_string)
    except ImportError:
        import psycopg # pylint: disable=F0401
        return psycopg.connect(conn_string)
