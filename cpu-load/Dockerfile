FROM alpine:3.19

# Instala Python e Zabbix Agent
RUN apk add --no-cache \
    python3 \
    py3-pip \
    zabbix-agent \
    busybox-extras

# Diretório da aplicação
WORKDIR /app

# Copia o script de carga
COPY cpu_load.py .

# Configuração mínima do Zabbix Agent
RUN sed -i 's/^Server=.*/Server=zabbix-server/' /etc/zabbix/zabbix_agentd.conf && \
    sed -i 's/^ServerActive=.*/ServerActive=zabbix-server/' /etc/zabbix/zabbix_agentd.conf && \
    sed -i 's/^Hostname=.*/Hostname=cpu-load/' /etc/zabbix/zabbix_agentd.conf

# Porta do agent
EXPOSE 10050

# Inicia o agent e o script Python
CMD zabbix_agentd && python3 cpu_load.py


