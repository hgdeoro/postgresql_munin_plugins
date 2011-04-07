#!/usr/bin/env python

"""
PostgreSql plugins for Munin
Copyright Horacio G. de Oro <hgdeoro@gmail.com> 2011
Licenced under GPL v2.

Based on a plugin (pg__db_size) from  Dalibo <cedric.villemain@dalibo.com>
Based on a plugin (postgres_block_read_) from Bj.rn Ruberg <bjorn@linpro.no> 

To install (in default locations of Ubuntu 10.04):

    ln -s /dir/dir/dir/path/to/pg_databases_stat_activity_xact.py \
        /etc/munin/plugins/pg_databases_stat_activity_xact

To setup host, port, username, password, to which db to connect,
in '/etc/munin/plugin-conf.d/munin-node' (default location in Ubuntu):

    [pg_databases_stat_activity_xact]
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
            graph_title PostgreSql Commits and Rollbacks
            graph_args -l 0 --vertical-label Tx
            graph_category postgresql
        """)
    
    dbs_to_monitor = get_dbs_to_monitor(cursor)
    
    cursor.execute("SELECT datname, datid, xact_commit, xact_rollback FROM pg_stat_database " + \
        "ORDER BY datname")
    
    for datname, datid, xact_commit, xact_rollback in cursor.fetchall(): # pylint: disable=W0612
        
        if not datname in dbs_to_monitor:
            continue
        
        if "config" in sys.argv:
            print format_multiline("""
                %(db_name)s_xact_commit.label Tx commited in %(db_name)s
                %(db_name)s_xact_commit.type DERIVE
                %(db_name)s_xact_commit.min 0
                %(db_name)s_xact_rollback.label Tx rollbacked in %(db_name)s
                %(db_name)s_xact_rollback.type DERIVE
                %(db_name)s_xact_rollback.min 0
            """ % { 'db_name': datname })
        else:
            print format_multiline("""
                %(db_name)s_xact_commit %(xact_commit)d
                %(db_name)s_xact_rollback %(xact_rollback)d
            """ % { 'db_name': datname, 'xact_commit': xact_commit, 'xact_rollback': xact_rollback})

if __name__ == '__main__':
    main()
