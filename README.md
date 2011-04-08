PostgreSql plugins for Munin
============================

Each of these plugins for Munin generates graphs for *all* the databases
in the PostgreSql instance. So, if you use pg_databases_size.py,
the graph will contain the size of every database (including
template0 and template1). You may *exclude* databases (see below).

Install
-------

A simple  and **INSECURE** way to install (based on default locations of Munin on Ubuntu 10.10):

    ~$ cd ~
    ~$ git clone git://github.com/hgdeoro/postgresql_munin_plugins.git
    ~$ ln -s ~/postgresql_munin_plugins/src/hgdeoro/munin/pg_databases_size.py \
                /etc/munin/plugins/pg_databases_size

Configure
---------

To setup host, port, username, password, to which db to connect,
add the folowing lines to in '/etc/munin/plugin-conf.d/munin-node':

    [pg_databases_size]
    env.pg_host localhost
    env.pg_port 5432
    env.pg_db_connect template1
    env.pg_user postgres
    env.pg_passwd <NO DEFAULT>

The only required parameter is **env.pg_passwd**

The list of databases to ignore could be specified with 'env.pg_ignore_db', separated by commas:

    env.pg_ignore_db db_to_ignore,postgresql,template0,db2,db3

License
-------

Copyright &copy; Horacio G. de Oro - <hgdeoro@gmail.com> - 2011

Licenced under GPL v2.
