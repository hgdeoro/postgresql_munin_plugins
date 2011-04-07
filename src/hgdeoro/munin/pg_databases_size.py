import os
import psycopg2

## Licenced under GPL v2.
## Copyright Horacio G. de Oro <hgdeoro@gmail.com> 2011
## Based on a plugin (pg__db_size) from  Dalibo <cedric.villemain@dalibo.com>
## Based on a plugin (postgres_block_read_) from Bj.rn Ruberg <bjorn@linpro.no> 

def main():
    pg_host = os.environ.get('pg_host', 'localhost')
    pg_port = os.environ.get('pg_port', '5432')
    pg_db_connect = os.environ.get('pg_db_connect', 'template1')
    pg_user = os.environ.get('pg_user', 'postgres')
    pg_passwd = os.environ.get('pg_passwd')
    
    conn_string = "host='%s' dbname='%s' user='%s' port='%s' password='%s'" % (
        pg_host, pg_db_connect, pg_user, pg_port, pg_passwd, )
    
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    
if __name__ == '__main__':
    main()
