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

def main():
    """
    Main method.
    """
    
    if "config" in sys.argv:
        print format_multiline("""
            graph_title PostgreSql Database Running Queries
            graph_args -l 0
            graph_category postgresql
            running.label Number of running queries (including locked)
            running.type GAUGE
            granted_locks.label Number of granted locks
            granted_locks.type GAUGE
            non_granted_locks.label Number of tx waiting for locks
            non_granted_locks.type GAUGE
        """)
        return
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pg_stat_activity")
    running_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pg_locks WHERE granted IS TRUE")
    granted_locks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pg_locks WHERE granted IS FALSE")
    non_granted_locks = cursor.fetchone()[0]
    
    print "running.value %d" % running_count
    print "granted_locks.value %d" % granted_locks
    print "non_granted_locks.value %d" % non_granted_locks

if __name__ == '__main__':
    main()
