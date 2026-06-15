# setup_env.ps1 - First-time SJTUBeamer environment setup
# Usage: powershell.exe -ExecutionPolicy Bypass -File setup_env.ps1

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir
$beamerDir = Join-Path $skillDir "assets\SJTUBeamer"

Write-Host "=== SJTUBeamer Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# 1. Check/install MiKTeX
Write-Host "[1/5] Checking MiKTeX ... " -NoNewline
$miktexFound = $false
try {
    $null = & xelatex --version 2>&1
    $miktexFound = $true
    Write-Host "Installed" -ForegroundColor Green
} catch {
    Write-Host "Not installed" -ForegroundColor Yellow
}

if (-not $miktexFound) {
    Write-Host "  Installing MiKTeX (may take a few minutes) ..." -ForegroundColor Yellow
    try {
        winget install MiKTeX.MiKTeX --accept-package-agreements --accept-source-agreements
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        Write-Host "  MiKTeX installed" -ForegroundColor Green
    } catch {
        Write-Host "  winget install failed. Please install MiKTeX manually: https://miktex.org/download" -ForegroundColor Red
        exit 1
    }
}

# 2. Enable auto-installer
Write-Host "[2/5] Enabling MiKTeX auto-installer ... " -NoNewline
try {
    & initexmf --enable-installer 2>&1 | Out-Null
    Write-Host "OK" -ForegroundColor Green
} catch {
    Write-Host "Failed (run manually: initexmf --enable-installer)" -ForegroundColor Yellow
}

# 3. Install latexmk
Write-Host "[3/5] Checking latexmk ... " -NoNewline
try {
    $null = & latexmk --version 2>&1
    Write-Host "Installed" -ForegroundColor Green
} catch {
    Write-Host "Not found, installing ..." -ForegroundColor Yellow
    try {
        & mpm --install latexmk 2>&1 | Out-Null
        & initexmf --update-config 2>&1 | Out-Null
        Write-Host "OK" -ForegroundColor Green
    } catch {
        Write-Host "Install failed (run manually: mpm --install latexmk)" -ForegroundColor Yellow
    }
}

# 4. Clone SJTUBeamer template
Write-Host "[4/5] Cloning SJTUBeamer template ... " -NoNewline
if (Test-Path "$beamerDir\beamerthemesjtubeamer.sty") {
    Write-Host "Already exists" -ForegroundColor Green
} else {
    Write-Host "Cloning ..." -ForegroundColor Yellow
    try {
        git clone https://github.com/sjtug/SJTUBeamer.git $beamerDir
        Write-Host "OK" -ForegroundColor Green
    } catch {
        Write-Host "GitHub clone failed, trying mirror ..." -ForegroundColor Yellow
        try {
            git clone https://mirror.sjtu.edu.cn/git/SJTUBeamer.git $beamerDir
            Write-Host "OK (via mirror)" -ForegroundColor Green
        } catch {
            Write-Host "Clone failed. Please run manually: git clone https://github.com/sjtug/SJTUBeamer.git `"$beamerDir`"" -ForegroundColor Red
        }
    }
}

# 5. Verify
Write-Host "[5/5] Verifying environment ..."
& "$scriptDir\check_env.ps1"

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host "You can now generate Beamer presentations with the sjtu-beamer-ppt skill." -ForegroundColor Cyan
