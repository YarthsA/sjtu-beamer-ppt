# compile_tex.ps1 - Compile .tex file to PDF
# Usage: powershell.exe -ExecutionPolicy Bypass -File compile_tex.ps1 -TexFile main.tex -WorkDir C:\path\to\project

param(
    [Parameter(Mandatory=$true)]
    [string]$TexFile,

    [Parameter(Mandatory=$false)]
    [string]$WorkDir = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir
$beamerDir = Join-Path $skillDir "assets\SJTUBeamer"

# Verify SJTUBeamer template exists
if (-not (Test-Path "$beamerDir\beamerthemesjtubeamer.sty")) {
    Write-Host "ERROR: SJTUBeamer template not found. Run setup_env.ps1 first." -ForegroundColor Red
    exit 1
}

# Verify .tex file exists
$texPath = Join-Path $WorkDir $TexFile
if (-not (Test-Path $texPath)) {
    Write-Host "ERROR: .tex file not found: $texPath" -ForegroundColor Red
    exit 1
}

Write-Host "=== Compiling Beamer Presentation ===" -ForegroundColor Cyan
Write-Host "  Source: $TexFile"
Write-Host "  WorkDir: $WorkDir"
Write-Host ""

# 1. Deploy SJTUBeamer resources
Write-Host "[1/3] Deploying SJTUBeamer resources ..." -ForegroundColor Gray

$styFiles = @(
    "beamerthemesjtubeamer.sty",
    "beamercolorthemesjtubeamer.sty",
    "beamerfontthemesjtubeamer.sty",
    "beamerinnerthemesjtubeamer.sty",
    "beamerouterthemesjtubeamer.sty",
    "sjtuvi.sty",
    "sjtucover.sty"
)

foreach ($f in $styFiles) {
    $src = Join-Path $beamerDir $f
    $dst = Join-Path $WorkDir $f
    if (Test-Path $src) {
        Copy-Item $src $dst -Force
    }
}

# Copy vi/ folder (logos)
$viSrc = Join-Path $beamerDir "vi"
$viDst = Join-Path $WorkDir "vi"
if (Test-Path $viSrc) {
    if (-not (Test-Path $viDst)) {
        Copy-Item $viSrc $viDst -Recurse -Force
    }
}

# Copy latexmkrc if not present
$latexmkrcSrc = Join-Path $beamerDir "latexmkrc"
$latexmkrcDst = Join-Path $WorkDir "latexmkrc"
if ((Test-Path $latexmkrcSrc) -and (-not (Test-Path $latexmkrcDst))) {
    Copy-Item $latexmkrcSrc $latexmkrcDst -Force
}

# 2. Compile
Write-Host "[2/3] Compiling (latexmk -xelatex) ..." -ForegroundColor Gray

Push-Location $WorkDir
try {
    & latexmk -xelatex -interaction=nonstopmode -file-line-error $TexFile 2>&1
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}

# 3. Check result
$pdfName = [System.IO.Path]::ChangeExtension($TexFile, ".pdf")
$pdfPath = Join-Path $WorkDir $pdfName

Write-Host "[3/3] Checking output ..." -ForegroundColor Gray

if ($exitCode -eq 0 -and (Test-Path $pdfPath)) {
    Write-Host ""
    Write-Host "=== Compilation SUCCEEDED ===" -ForegroundColor Green
    Write-Host "  Output: $pdfPath" -ForegroundColor Cyan

    # --- Overflow Check ---
    $logName = [System.IO.Path]::ChangeExtension($TexFile, ".log")
    $logPath = Join-Path $WorkDir $logName
    if (Test-Path $logPath) {
        $overfulls = Select-String -Path $logPath -Pattern "Overfull \\[hv]box"
        if ($overfulls) {
            Write-Host ""
            Write-Host "*** OVERFLOW WARNINGS ***" -ForegroundColor Yellow
            Write-Host "  Content may exceed slide boundaries:" -ForegroundColor Yellow
            $shown = @{}
            foreach ($o in $overfulls) {
                $line = $o.Line.Trim()
                # Extract Overfull type and amount
                if ($line -match "Overfull \\hbox") {
                    $type = "H-overflow (too wide)"
                    $fix = "shrink width, smaller font, or fewer columns"
                } else {
                    $type = "V-overflow (too tall)"
                    $fix = "reduce items, smaller font, or split frame"
                }
                $amt = ""
                if ($line -match "by (\d+\.?\d*pt)") {
                    $amt = "($($Matches[1]))"
                }
                # Deduplicate by type+amount
                $key = "$type$amt"
                if (-not $shown[$key]) {
                    Write-Host "  [$type] $amt" -ForegroundColor Yellow
                    Write-Host "    Fix: $fix" -ForegroundColor DarkGray
                    $shown[$key] = $true
                }
            }
            Write-Host "  Edit .tex and recompile to resolve." -ForegroundColor Yellow
        } else {
            Write-Host "  [OK] No overflow detected" -ForegroundColor DarkGray
        }
    }
} else {
    Write-Host ""
    Write-Host "=== Compilation FAILED (exit code: $exitCode) ===" -ForegroundColor Red

    $logName = [System.IO.Path]::ChangeExtension($TexFile, ".log")
    $logPath = Join-Path $WorkDir $logName
    if (Test-Path $logPath) {
        Write-Host ""
        Write-Host "Recent errors:" -ForegroundColor Yellow
        Select-String -Path $logPath -Pattern "^!" | Select-Object -Last 5 | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Yellow
        }
    }
    exit $exitCode
}
