# Sobe o Zabbix e restaura o dump AD01 (execute nesta pasta, no PowerShell)
# Uso:  powershell -ExecutionPolicy Bypass -File .\subir_zabbix.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== Atualizando repositorio =="
git fetch
git pull

Write-Host "== Resetando containers e redes =="
docker compose down --remove-orphans
docker network prune -f

Write-Host "== Subindo containers (build do zabbix-server com ODBC) =="
docker compose up -d --build

Write-Host "== Aguardando o MariaDB aceitar conexoes =="
$ok = $false
for ($i = 0; $i -lt 40; $i++) {
    docker exec zabbix-mariadb mysqladmin -u zabbix -pzabbixpass ping 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $ok = $true; break }
    Start-Sleep -Seconds 3
}
if (-not $ok) { throw "MariaDB nao respondeu" }

Write-Host "== Restaurando AD01-16.sql (dump mais recente, inclui TDE02, F12, F14 e F16) (pode levar 1-2 minutos) =="
docker compose stop zabbix-server zabbix-web
docker cp .\AD01-16.sql zabbix-mariadb:/tmp/AD01.sql
docker exec zabbix-mariadb sh -c "mysql -u zabbix -pzabbixpass zabbix < /tmp/AD01.sql"
docker compose start zabbix-server zabbix-web

Write-Host "== Conferindo EnableGlobalScripts =="
docker exec zabbix-server sh -c "grep -R EnableGlobalScripts /etc/zabbix"

docker ps
Write-Host "Pronto: abra http://localhost:8080"
