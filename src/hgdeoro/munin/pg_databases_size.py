#!/usr/bin/env python

"""
PostgreSql plugins for Munin
Copyright Horacio G. de Oro <hgdeoro@gmail.com> 2011
Licenced under GPL v2.

Based on a plugin (pg__db_size) from  Dalibo <cedric.villemain@dalibo.com>
Based on a plugin (postgres_block_read_) from Bj.rn Ruberg <bjorn@linpro.no> 

To install (in default locations of Ubuntu 10.04):

    ln -s /dir/dir/dir/path/to/pg_databases_size.py /etc/munin/plugins/pg_databases_size

To setup host, port, username, password, to which db to connect,
in '/etc/munin/plugin-conf.d/munin-node' (default location in Ubuntu):

    [pg_databases_size]
    env.pg_host localhost
    env.pg_port 5432
    env.pg_db_connect template1
    env.pg_user postgres
    env.pg_passwd <NO DEFAULT>

The only needed line is 'env.pg_passwd'.

The list of databases to ignore could be specified with 'env.pg_ignore_db', separated by commas:

    env.pg_ignore_db db_to_ignore,postgresql,template0,db2,db3

"""

import os
import os.path
import sys

# Setup PYTHONPATH
BASE_DIR = os.path.split(os.path.realpath(__file__))[0] # BASE_DIR/hgdeoro/munin
BASE_DIR = os.path.split(BASE_DIR)[0] # BASE_DIR/hgdeoro
BASE_DIR = os.path.split(BASE_DIR)[0] # BASE_DIR
sys.path.append(os.path.abspath(BASE_DIR))

from hgdeoro.munin import format_multiline, connect, get_dbs_to_monitor

def main():
    """
    Main method.
    """
    conn = connect()
    cursor = conn.cursor()
    
    if "config" in sys.argv:

        print format_multiline("""
            graph_title PostgreSql Database Size (on disk)
            graph_args --base 1024 -l 0 --vertical-label Bytes --upper-limit 3719946240
            graph_category postgresql
        """)
    
    for db_name in get_dbs_to_monitor(cursor):
        cursor.execute("SELECT pg_database_size(%s)", [db_name])
        db_size = cursor.fetchall()[0][0]
        
        if "config" in sys.argv:
            print format_multiline("""
                %(db_name)s.label %(db_name)s
                %(db_name)s.type GAUGE
            """ % { 'db_name': db_name })
        else:
            print "%s.value %d" % (db_name, db_size, )

if __name__ == '__main__':
    main()
