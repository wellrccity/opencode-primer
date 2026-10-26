#requires -Version 5.1
<#
.SYNOPSIS
    Installs the opencode-primer configuration into an OpenCode config directory.

.DESCRIPTION
    Copies config, agents, commands, skills, and the meta-goal plugin into the
    target directory. The target is the value of the OPENCODE_CONFIG_DIR
    environment variable when set, otherwise "$HOME/.config/opencode".

    Existing files are never overwritten unless -Force is used. With -Force the
    whole target is first backed up to "<target>-backup-<yyyyMMdd-HHmmss>".

    -DryRun prints the planned actions and writes nothing.

.PARAMETER Force
    Back up the target and overwrite existing files.

.PARAMETER DryRun
    Print planned actions and exit without writing anything.

.PARAMETER Help
    Print usage information and exit without writing anything.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/install.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -Force
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$DryRun,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $PSScriptRoot

if ($Help) {
    Write-Host 'Usage: powershell -ExecutionPolicy Bypass -File scripts/install.ps1 [-Force] [-DryRun] [-Help]'
    Write-Host ''
    Write-Host 'Target: the OPENCODE_CONFIG_DIR environment variable when set,'
    Write-Host '        otherwise "$HOME/.config/opencode".'
    Write-Host ''
    Write-Host '  -Force   Back up the target and overwrite existing files.'
    Write-Host '  -DryRun  Print planned actions and write nothing.'
    Write-Host '  -Help    Print this usage and exit without writing anything.'
    exit 0
}

$Mappings = @(
    [pscustomobject]@{ Source = 'config/opencode.json'; Destination = 'opencode.json';     Kind = 'File' },
    [pscustomobject]@{ Source = 'config/cli.json';      Destination = 'cli.json';          Kind = 'File' },
    [pscustomobject]@{ Source = 'config/AGENTS.md';     Destination = 'AGENTS.md';         Kind = 'File' },
    [pscustomobject]@{ Source = 'agents';               Destination = 'agents';            Kind = 'Directory' },
    [pscustomobject]@{ Source = 'commands';             Destination = 'commands';          Kind = 'Directory' },
    [pscustomobject]@{ Source = 'skills';               Destination = 'skills';            Kind = 'Directory' },
    [pscustomobject]@{ Source = 'plugins/meta-goal';    Destination = 'plugins/meta-goal'; Kind = 'Directory' }
)

function Get-TargetDirectory {
    $configured = [Environment]::GetEnvironmentVariable('OPENCODE_CONFIG_DIR')
    if (-not [string]::IsNullOrWhiteSpace($configured)) {
        return [System.IO.Path]::GetFullPath($configured)
    }

    $homeDir = [Environment]::GetFolderPath('UserProfile')
    if ([string]::IsNullOrWhiteSpace($homeDir)) {
        $homeDir = $HOME
    }
    if ([string]::IsNullOrWhiteSpace($homeDir)) {
        throw 'Cannot resolve the home directory. Set OPENCODE_CONFIG_DIR.'
    }
    return [System.IO.Path]::Combine($homeDir, '.config', 'opencode')
}

function Get-InstallItems {
    param(
        [string]$Root,
        [string]$Target
    )

    $items = New-Object System.Collections.ArrayList
    foreach ($mapping in $Mappings) {
        $relativeSource = $mapping.Source.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
        $relativeDest = $mapping.Destination.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
        $sourcePath = [System.IO.Path]::Combine($Root, $relativeSource)
        $destPath = [System.IO.Path]::Combine($Target, $relativeDest)

        if (-not (Test-Path -LiteralPath $sourcePath)) {
            throw "Missing source: $($mapping.Source)"
        }

        if ($mapping.Kind -eq 'File') {
            [void]$items.Add([pscustomobject]@{ Source = $sourcePath; Destination = $destPath })
            continue
        }

        $files = @(Get-ChildItem -LiteralPath $sourcePath -Recurse -File | Sort-Object -Property FullName)
        foreach ($file in $files) {
            $relative = $file.FullName.Substring($sourcePath.Length).TrimStart([char[]]@('\', '/'))
            [void]$items.Add([pscustomobject]@{
                Source      = $file.FullName
                Destination = [System.IO.Path]::Combine($destPath, $relative)
            })
        }
    }
    return $items
}

function Invoke-Install {
    param(
        [string]$Root,
        [string]$Target,
        [bool]$ForceOverwrite,
        [bool]$PreviewOnly
    )

    Write-Host "Source: $Root"
    Write-Host "Target: $Target"
    if ($PreviewOnly) {
        Write-Host 'Mode:   dry run (nothing is written)'
    }
    elseif ($ForceOverwrite) {
        Write-Host 'Mode:   force (target is backed up, existing files overwritten)'
    }
    else {
        Write-Host 'Mode:   safe (existing files are skipped)'
    }
    Write-Host ''

    $items = @(Get-InstallItems -Root $Root -Target $Target)

    $copy = New-Object System.Collections.ArrayList
    $skipped = 0
    foreach ($item in $items) {
        if ((Test-Path -LiteralPath $item.Destination) -and -not $ForceOverwrite) {
            Write-Host ('SKIP   {0} (already exists)' -f $item.Destination)
            $skipped++
            continue
        }
        [void]$copy.Add($item)
    }

    $backupPath = $null
    if ($ForceOverwrite -and $copy.Count -gt 0 -and (Test-Path -LiteralPath $Target)) {
        $backupPath = '{0}-backup-{1}' -f $Target, (Get-Date -Format 'yyyyMMdd-HHmmss')
    }

    if ($PreviewOnly) {
        if ($backupPath) {
            Write-Host ('WOULD BACKUP {0} -> {1}' -f $Target, $backupPath)
        }
        foreach ($item in $copy) {
            Write-Host ('WOULD COPY   {0} -> {1}' -f $item.Source, $item.Destination)
        }
        Write-Host ''
        Write-Host ('Dry run complete: {0} file(s) would be installed, {1} skipped.' -f $copy.Count, $skipped)
        return 0
    }

    if ($backupPath) {
        if (Test-Path -LiteralPath $backupPath) {
            throw "Backup path already exists: $backupPath"
        }
        Write-Host ('BACKUP {0} -> {1}' -f $Target, $backupPath)
        Copy-Item -LiteralPath $Target -Destination $backupPath -Recurse
    }

    foreach ($item in $copy) {
        $parent = Split-Path -Parent $item.Destination
        if ($parent -and -not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        Copy-Item -LiteralPath $item.Source -Destination $item.Destination -Force
        Write-Host ('COPY   {0} -> {1}' -f $item.Source, $item.Destination)
    }

    Write-Host ''
    Write-Host ('Installed {0} file(s) into {1}, {2} skipped.' -f $copy.Count, $Target, $skipped)
    return 0
}

try {
    $targetPath = Get-TargetDirectory
    Invoke-Install -Root $RepoRoot -Target $targetPath -ForceOverwrite ([bool]$Force) -PreviewOnly ([bool]$DryRun) | Out-Null
}
catch {
    Write-Host ('ERROR: ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}

exit 0
