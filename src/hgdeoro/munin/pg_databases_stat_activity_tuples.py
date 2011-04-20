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
            graph_title PostgreSql Number of tuples managed
            graph_category postgresql
        """)
    
    dbs_to_monitor = get_dbs_to_monitor(cursor)
    
    cursor.execute("SELECT datname, datid, tup_returned, tup_fetched, tup_inserted, " + \
        "tup_updated, tup_deleted FROM pg_stat_database ORDER BY datname")
    
    for datname, datid, tup_returned, tup_fetched, tup_inserted, tup_updated, tup_deleted in \
            cursor.fetchall(): # pylint: disable=W0612
        
        if not datname in dbs_to_monitor:
            continue
        
        if "config" in sys.argv:
            for report_type in [ 'tup_returned', 'tup_fetched', 'tup_inserted', 'tup_updated',
                    'tup_deleted']:
                print format_multiline("""
                    %(db_name)s_%(report_type)s.label %(db_name)s %(report_type)s
                    %(db_name)s_%(report_type)s.draw LINE
                    %(db_name)s_%(report_type)s.type DERIVE
                    %(db_name)s_%(report_type)s.min 0
                """ % { 'db_name': datname, 'report_type': report_type, })
        else:
            print format_multiline("""
                %(db_name)s_tup_returned.value %(tup_returned)d
                %(db_name)s_tup_fetched.value %(tup_fetched)d
                %(db_name)s_tup_inserted.value %(tup_inserted)d
                %(db_name)s_tup_updated.value %(tup_updated)d
                %(db_name)s_tup_deleted.value %(tup_deleted)d
            """ % { 'db_name': datname, 'tup_returned': tup_returned, 'tup_fetched': tup_fetched,
                'tup_inserted': tup_inserted, 'tup_updated': tup_updated,
                'tup_deleted': tup_deleted })

if __name__ == '__main__':
    main()
