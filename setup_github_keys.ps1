# Script para configurar chaves SSH e GPG para GitHub
param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubEmail,
    
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername
)

# Função para verificar se um comando existe
function Test-CommandExists {
    param($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try {
        if(Get-Command $command) { return $true }
    } catch {
        return $false
    } finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Verificar se o Git está instalado
if (-not (Test-CommandExists "git")) {
    Write-Host "Git não está instalado. Por favor, instale o Git primeiro."
    exit 1
}

# Verificar se o OpenSSH está instalado
if (-not (Test-CommandExists "ssh-keygen")) {
    Write-Host "OpenSSH não está instalado. Por favor, instale o OpenSSH primeiro."
    exit 1
}

# Verificar se o GPG está instalado
if (-not (Test-CommandExists "gpg")) {
    Write-Host "GPG não está instalado. Por favor, instale o GPG primeiro."
    exit 1
}

# Configurar SSH
Write-Host "`nConfigurando chave SSH..."
$sshDir = "$env:USERPROFILE\.ssh"
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir | Out-Null
}

# Gerar chave SSH
$sshKeyPath = "$sshDir\id_ed25519"
if (-not (Test-Path $sshKeyPath)) {
    ssh-keygen -t ed25519 -C $GitHubEmail -f $sshKeyPath -N '""'
    Write-Host "Chave SSH gerada com sucesso!"
} else {
    Write-Host "Chave SSH já existe."
}

# Iniciar o ssh-agent
Start-Service ssh-agent
ssh-add $sshKeyPath

# Mostrar a chave SSH pública
Write-Host "`nSua chave SSH pública:"
Get-Content "$sshKeyPath.pub"

# Configurar GPG
Write-Host "`nConfigurando chave GPG..."
$gpgConfigDir = "$env:APPDATA\gnupg"
if (-not (Test-Path $gpgConfigDir)) {
    New-Item -ItemType Directory -Path $gpgConfigDir | Out-Null
}

# Gerar chave GPG
$gpgKey = gpg --full-generate-key --batch --pinentry-mode loopback << @
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: $GitHubUsername
Name-Email: $GitHubEmail
Expire-Date: 0
@

# Obter o ID da chave GPG
$gpgKeyId = gpg --list-secret-keys --keyid-format LONG $GitHubEmail | 
    Select-String -Pattern "sec\s+rsa4096/([A-F0-9]+)" | 
    ForEach-Object { $_.Matches.Groups[1].Value }

# Exportar a chave GPG pública
$gpgPublicKey = gpg --armor --export $gpgKeyId
Write-Host "`nSua chave GPG pública:"
$gpgPublicKey

# Configurar Git para usar GPG
git config --global user.signingkey $gpgKeyId
git config --global commit.gpgsign true

Write-Host "`nConfiguração concluída!"
Write-Host "`nPara completar a configuração:"
Write-Host "1. Acesse https://github.com/settings/keys"
Write-Host "2. Adicione sua chave SSH pública"
Write-Host "3. Adicione sua chave GPG pública"
Write-Host "`nPara testar a conexão SSH:"
Write-Host "ssh -T git@github.com" 