# tools/utils/helper_functions.ps1
# Funções utilitárias comuns para scripts PowerShell

function Write-Log {
    param (
        [string]$Message,
        [string]$Level = "INFO"
    )
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$Timestamp] [$Level] $Message"
}

function Test-PathExists {
    param (
        [string]$Path
    )
    return (Test-Path $Path)
}