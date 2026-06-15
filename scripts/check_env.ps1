# check_env.ps1 - SJTUBeamer environment check
# Usage: powershell.exe -ExecutionPolicy Bypass -File check_env.ps1

$ok = $true

Write-Host "=== SJTUBeamer Environment Check ===" -ForegroundColor Cyan
Write-Host ""

# 1. XeLaTeX
Write-Host "[1/4] XeLaTeX ... " -NoNewline
try {
    $ver = & xelatex --version 2>&1 | Select-Object -First 1
    Write-Host "OK" -ForegroundColor Green
    Write-Host "       $ver" -ForegroundColor Gray
} catch {
    Write-Host "NOT FOUND" -ForegroundColor Red
    $ok = $false
}

# 2. latexmk
Write-Host "[2/4] latexmk ... " -NoNewline
try {
    $ver = & latexmk --version 2>&1 | Select-Object -First 1
    Write-Host "OK" -ForegroundColor Green
} catch {
    Write-Host "NOT FOUND" -ForegroundColor Red
    $ok = $false
}

# 3. MiKTeX auto-installer
Write-Host "[3/4] MiKTeX auto-installer ... " -NoNewline
try {
    $null = & initexmf --enable-installer 2>&1
    Write-Host "OK" -ForegroundColor Green
} catch {
    Write-Host "MiKTeX NOT FOUND" -ForegroundColor Red
    $ok = $false
}

# 4. SJTUBeamer template
Write-Host "[4/4] SJTUBeamer template ... " -NoNewline
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$beamerDir = Join-Path (Split-Path -Parent $scriptDir) "assets\SJTUBeamer"
if (Test-Path "$beamerDir\beamerthemesjtubeamer.sty") {
    Write-Host "OK" -ForegroundColor Green
    Write-Host "       Path: $beamerDir" -ForegroundColor Gray
} else {
    Write-Host "NOT FOUND" -ForegroundColor Red
    Write-Host "       Run setup_env.ps1 to clone the template" -ForegroundColor Gray
    $ok = $false
}

Write-Host ""
if ($ok) {
    Write-Host "=== Environment READY ===" -ForegroundColor Green
} else {
    Write-Host "=== Environment NOT READY ===" -ForegroundColor Yellow
}
