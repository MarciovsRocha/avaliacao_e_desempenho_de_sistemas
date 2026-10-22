FROM zabbix/zabbix-server-mysql:alpine-7.0-latest

USER root

# Instala ODBC + driver MariaDB
# (repositorios via http: a rede local intercepta o certificado TLS)
RUN sed -i 's|https://|http://|g' /etc/apk/repositories \
 && apk add --no-cache unixodbc mariadb-connector-odbc

# Registra o driver MariaDB
RUN printf '%s\n' \
    '[MariaDB]' \
    'Description=MariaDB ODBC Driver' \
    'Driver=/usr/lib/mariadb/libmaodbc.so' \
    'UsageCount=1' \
    > /etc/odbcinst.ini

# Cria um DSN padrao para o Zabbix
RUN printf '%s\n' \
    '[MYSQL_ZABBIX]' \
    'Driver=MariaDB' \
    'Server=mariadb' \
    'Port=3306' \
    'Database=mysql' \
    > /etc/odbc.ini

# Volta para o usuario do Zabbix
USER zabbix
