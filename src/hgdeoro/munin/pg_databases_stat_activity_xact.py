#!/usr/bin/env python

"""
PostgreSql plugins for Munin
Copyright Horacio G. de Oro <hgdeoro@gmail.com> 2011
Licenced under GPL v2.

Based on a plugin (pg__db_size) from  Dalibo <cedric.villemain@dalibo.com>
Based on a plugin (postgres_block_read_) from Bj.rn Ruberg <bjorn@linpro.no> 
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

# FIXME: check that fieldnames contains only valid values

def main():
    """
    Main method.
    """
    conn = connect()
    cursor = conn.cursor()
    
    if "config" in sys.argv:
        # graph_args -l 0 --vertical-label Tx --base 1000
        # graph_vlabel (+) commits / (-) rollbacks per seccond
        print format_multiline("""
            graph_title PostgreSql Commits and Rollbacks
            graph_category postgresql
        """)
    
    dbs_to_monitor = get_dbs_to_monitor(cursor)
    
    cursor.execute("SELECT datname, datid, xact_commit, xact_rollback FROM pg_stat_database " + \
        "ORDER BY datname")
    
    for datname, datid, xact_commit, xact_rollback in cursor.fetchall(): # pylint: disable=W0612
        
        if not datname in dbs_to_monitor:
            continue
        
        var_commit = "%s_ct" % datname
        var_rb = "%s_rb" % datname
        if "config" in sys.argv:
            print format_multiline("""
                %(var_commit)s.label %(db_name)s commits
                %(var_commit)s.draw LINE
                %(var_commit)s.type DERIVE
                %(var_commit)s.min 0
                
                %(var_rb)s.label %(db_name)s rollbacks
                %(var_rb)s.draw LINE
                %(var_rb)s.type DERIVE
                %(var_rb)s.min 0
            """ % { 'db_name': datname, 'var_commit': var_commit, 'var_rb': var_rb })
            
        else:
            print format_multiline("""
                %(var_commit)s.value %(xact_commit)d
                %(var_rb)s.value %(xact_rollback)d
            """ % { 'db_name': datname, 'xact_commit': xact_commit, 'xact_rollback': xact_rollback,
                'var_commit': var_commit, 'var_rb': var_rb})

if __name__ == '__main__':
    main()
