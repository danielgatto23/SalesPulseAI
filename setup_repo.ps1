# Script para configurar repositório Git e enviar para GitHub
param(
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername,
    
    [Parameter(Mandatory=$true)]
    [string]$GitHubToken
)

# Verificar se o Git está instalado
try {
    git --version | Out-Null
} catch {
    Write-Host "Git não está instalado. Por favor, instale o Git primeiro."
    exit 1
}

# Criar arquivo .gitignore
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment variables
.env

# Logs
logs/
*.log

# Database
*.db
*.sqlite3

# Jupyter Notebook
.ipynb_checkpoints

# System Files
.DS_Store
Thumbs.db
"@

$gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit inicial
git commit -m "Initial commit: Sales Insights System"

# Configurar repositório remoto
$remoteUrl = "https://$GitHubUsername`:$GitHubToken@github.com/$GitHubUsername/$RepoName.git"
git remote add origin $remoteUrl

# Criar repositório no GitHub usando a API
$headers = @{
    "Authorization" = "token $GitHubToken"
    "Accept" = "application/vnd.github.v3+json"
}

$body = @{
    "name" = $RepoName
    "description" = "Sistema de Insights de Vendas com previsão e recomendações"
    "private" = $false
    "auto_init" = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body
    Write-Host "Repositório criado com sucesso no GitHub: $($response.html_url)"
} catch {
    Write-Host "Erro ao criar repositório no GitHub: $_"
    exit 1
}

# Enviar código para o GitHub
try {
    git push -u origin main
    Write-Host "Código enviado com sucesso para o GitHub!"
} catch {
    Write-Host "Erro ao enviar código para o GitHub: $_"
    exit 1
}

Write-Host "`nConfiguração concluída! Seu repositório está disponível em:"
Write-Host "https://github.com/$GitHubUsername/$RepoName" 