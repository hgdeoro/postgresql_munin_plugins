#!/usr/bin/env python

"""
PostgreSql Database Size plugin for Munin
Copyright Horacio G. de Oro <hgdeoro@gmail.com> 2011
Licenced under GPL v2.

Based on a plugin (pg__db_size) from  Dalibo <cedric.villemain@dalibo.com>
Based on a plugin (postgres_block_read_) from Bj.rn Ruberg <bjorn@linpro.no> 
"""

import os
import pprint
import psycopg2
import sys

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
    
    conn = psycopg2.connect(conn_string)
    return conn

def main():
    """
    Main method.
    """
    debug = bool("--debug" in sys.argv)
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select datname from pg_database")
    records = cursor.fetchall()
    
    if debug:
        pprint.pprint(records)

    if "config" in sys.argv:

        print format_multiline("""
            graph_title PostgreSql Database Size (in MiB)
            graph_args -l 0 
            graph_vlabel Size in MiB
            graph_category postgresql
            graph_period second
        """)
        
        #print format_multiline("""
        #    graph_title PostgreSql Database Size (in MiB)
        #    graph_args --upper-limit 100 -l 0
        #    graph_vlabel %
        #    graph_scale no
        #    graph_category disk
        #""")

    for db_name in [row[0] for row in records]:
        cursor.execute("SELECT pg_database_size(%s)", [db_name])
        db_size = cursor.fetchall()[0][0]
        if debug:
            print "%s: %d KiB" % (db_name, int(db_size/1024))
        
        if "config" in sys.argv:
            print format_multiline("""
                %(db_name)s.label %(db_name)s
                %(db_name)s.type GAUGE
                %(db_name)s.max 20480
            """ % { 'db_name': db_name })
        else:
            print "%s.value %d" % (db_name, int(db_size/(1024*1024)), )

if __name__ == '__main__':
    main()
