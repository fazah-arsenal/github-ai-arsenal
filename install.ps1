# DeepSeek Harness / Universal Agents Skill Installer (Windows PowerShell)
# Supports both local execution (.\install.ps1) and 1-liner remote execution via `irm ... | iex`
$ErrorActionPreference = "Stop"

$SkillName = "github-ai-arsenal"
$LocalScript = $MyInvocation.MyCommand.Path
$SourceDir = if ($LocalScript) { Split-Path -Parent $LocalScript } else { "" }
$TempExtract = ""

if (-not $SourceDir -or -not (Test-Path (Join-Path $SourceDir "SKILL.md"))) {
    $Repo = if ($env:GH_ARSENAL_REPO) { $env:GH_ARSENAL_REPO } else { "fazah-arsenal/github-ai-arsenal" }
    $Branch = if ($env:GH_ARSENAL_BRANCH) { $env:GH_ARSENAL_BRANCH } else { "main" }
    $ZipUrl = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"
    $TempZip = Join-Path $env:TEMP "$SkillName-install.zip"
    $TempExtract = Join-Path $env:TEMP "$SkillName-extract"
    if (Test-Path $TempExtract) { Remove-Item $TempExtract -Recurse -Force }
    Write-Host "Downloading $SkillName from $ZipUrl ..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $ZipUrl -OutFile $TempZip -UseBasicParsing
    Expand-Archive -Path $TempZip -DestinationPath $TempExtract -Force
    Remove-Item $TempZip -Force -ErrorAction SilentlyContinue
    $Sub = Get-ChildItem $TempExtract -Directory | Select-Object -First 1
    $SourceDir = $Sub.FullName
}

$Targets = @(
    (Join-Path $env:USERPROFILE ".agents\skills\$SkillName"),
    (Join-Path $env:USERPROFILE ".gemini\config\skills\$SkillName")
)
foreach ($extra in @(".claude\skills", ".codex\skills", ".cursor\skills")) {
    $root = Join-Path $env:USERPROFILE $extra
    if (Test-Path $root) { $Targets += (Join-Path $root $SkillName) }
}

foreach ($dest in $Targets) {
    Write-Host "Installing $SkillName -> $dest" -ForegroundColor Cyan
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Copy-Item (Join-Path $SourceDir "SKILL.md") -Destination $dest -Force
    Copy-Item (Join-Path $SourceDir "README.md") -Destination $dest -Force
    Copy-Item (Join-Path $SourceDir "scripts") -Destination (Join-Path $dest "scripts") -Recurse -Force
    Copy-Item (Join-Path $SourceDir "references") -Destination (Join-Path $dest "references") -Recurse -Force
    if (Test-Path (Join-Path $SourceDir "examples")) {
        Copy-Item (Join-Path $SourceDir "examples") -Destination (Join-Path $dest "examples") -Recurse -Force
    }
}

if ($TempExtract -and (Test-Path $TempExtract)) {
    Remove-Item $TempExtract -Recurse -Force -ErrorAction SilentlyContinue
}

# Install short global CLI command: `fazah`
$BinDir = Join-Path $env:USERPROFILE ".local\bin"
New-Item -ItemType Directory -Path $BinDir -Force | Out-Null
$FazahCmd = Join-Path $BinDir "fazah.cmd"
$MainScript = Join-Path $env:USERPROFILE ".agents\skills\$SkillName\scripts\gh_arsenal.py"
"@echo off`r`npython `"$MainScript`" %*" | Set-Content -Path $FazahCmd -Encoding ASCII

# Auto-add Python Scripts directory and .local\bin to User PATH permanently
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$PathsToAdd = @($BinDir)
try {
    $pyExe = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($pyExe) {
        $pyScripts = Join-Path (Split-Path -Parent $pyExe) "Scripts"
        if (Test-Path $pyScripts) { $PathsToAdd += $pyScripts }
    }
} catch {}

foreach ($p in $PathsToAdd) {
    if (-not $UserPath -or ($UserPath -notlike "*$p*")) {
        $UserPath = if ($UserPath) { "$UserPath;$p" } else { $p }
        [Environment]::SetEnvironmentVariable("Path", $UserPath, "User")
        $env:Path = "$env:Path;$p"
    }
}

# Auto-link all MCP clients (Antigravity, Cursor, Claude, Windsurf, VS Code) on install
Write-Host "Auto-linking all local MCP environments..." -ForegroundColor Cyan
try {
    python "$MainScript" link
} catch {
    Write-Host "Notice: Run 'fazah link' once Python is added to PATH." -ForegroundColor Yellow
}

Write-Host "Installed $SkillName (20,078+ GitHub tools, Native MCP Server & short 'fazah' CLI) successfully!" -ForegroundColor Green
Write-Host "Try now: fazah doc | fazah r `"telegram bot`" | fazah m -q `"postgres`"" -ForegroundColor Yellow
