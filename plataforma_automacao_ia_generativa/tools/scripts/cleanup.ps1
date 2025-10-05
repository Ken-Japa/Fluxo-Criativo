# tools/scripts/cleanup.ps1
# Script para limpeza de arquivos temporários ou de build

Write-Host "Executando script de limpeza..."

# Exemplo: Remover diretórios de módulos de nó
# Get-ChildItem -Path . -Include "node_modules" -Recurse -Directory | Remove-Item -Recurse -Force

# Exemplo: Remover diretórios de cache de Python
# Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force

Write-Host "Limpeza concluída."