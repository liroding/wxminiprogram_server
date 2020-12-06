usermod -d /var/lib/mysql/ mysql
chown -R mysql:mysql /var/lib/mysql /var/run/mysqld
#mysqld --initialize --user=mysql --basedir=/usr --datadir=/var/lib/mysql
