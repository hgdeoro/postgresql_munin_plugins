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
    conn = connect()
    cursor = conn.cursor()
    
    if "config" in sys.argv:

        print format_multiline("""
            graph_title PostgreSql Block IO
            graph_args --base 1000 -l 0
            graph_category postgresql
        """)
    
    # Do this BEFORE cursor.execute(...)!!!
    dbs_to_monitor = get_dbs_to_monitor(cursor)
    
    cursor.execute("SELECT datid, datname, blks_read, blks_hit FROM pg_stat_database" + \
        " ORDER BY datname")
    
    first = True
    for datid, datname, blks_read, blks_hit in cursor.fetchall(): # pylint: disable=W0612
        
        if not datname in dbs_to_monitor:
            continue
        
        # AFTER the continue...
        if "config" in sys.argv:
            print format_multiline("""
                %(db_name)s_read.label %(db_name)s block reads
                %(db_name)s_read.type DERIVE
                %(db_name)s_read.min 0
                %(db_name)s_read.draw LINE
                
                %(db_name)s_hit.label %(db_name)s buffer hits
                %(db_name)s_hit.type DERIVE
                %(db_name)s_hit.min 0
                %(db_name)s_hit.draw LINE
            """ % { 'db_name': datname, })
        else:
            print format_multiline("""
                %(db_name)s_read.value %(read)d
                %(db_name)s_hit.value %(hit)d
            """ % { 'db_name': datname, 'read': blks_read, 'hit': blks_hit})

if __name__ == '__main__':
    main()
