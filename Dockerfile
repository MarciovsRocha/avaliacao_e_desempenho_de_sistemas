FROM zabbix/zabbix-server-mysql:alpine-latest

USER root

# Instala ODBC + driver MariaDB
RUN apk add --no-cache \
    unixodbc \
    mariadb-connector-odbc

# Registra o driver MariaDB
RUN cat << 'EOF' > /etc/odbcinst.ini
[MariaDB]
Description=MariaDB ODBC Driver
Driver=/usr/lib/mariadb/libmaodbc.so
UsageCount=1
EOF

# Cria um DSN padrão para o Zabbix
RUN cat << 'EOF' > /etc/odbc.ini
[MYSQL_ZABBIX]
Driver=MariaDB
Server=mariadb
Port=3306
Database=mysql
EOF

# Volta para o usuário do Zabbix
USER zabbix

