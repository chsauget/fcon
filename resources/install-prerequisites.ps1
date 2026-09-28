[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSVersion.Major -lt 5) {
    throw 'This script requires Windows PowerShell 5.1 or PowerShell 7.'
}

if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
    throw 'WinGet was not found. Install or update App Installer from the Microsoft Store, then run this script again.'
}

$packages = @(
    'Microsoft.PowerBI'
    'Microsoft.VisualStudioCode'
    'OpenJS.NodeJS.LTS'
    'Microsoft.AzureCLI'
    'Git.Git'
)

$failedCount = 0

foreach ($package in $packages) {

    $arguments = @(
        'install'
        '--exact'
        '--id', $package
        '--source', 'winget'
        '--silent'
        '--disable-interactivity'
        '--accept-source-agreements'
        '--accept-package-agreements'
    )

    $output = & winget.exe @arguments 2>&1 | ForEach-Object { $_.ToString() }
    $exitCode = $LASTEXITCODE

    if (($exitCode -eq 0) -or ($exitCode -eq -1978335189)) {
        Write-Host "${package}: OK" -ForegroundColor Green
    }
    else {
        $failedCount++
        $errorMessage = $output |
            Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
            Select-Object -Last 1

        if ([string]::IsNullOrWhiteSpace($errorMessage)) {
            $errorMessage = "WinGet exited with code $exitCode"
        }

        $errorMessage = ($errorMessage -replace '\s+', ' ').Trim()
        Write-Host "${package}: ERROR - $errorMessage" -ForegroundColor Red
    }
}

# Claude Code (native installer)
try {
    Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression
    Write-Host "Claude Code: OK" -ForegroundColor Green
}
catch {
    $failedCount++
    Write-Host "Claude Code: ERROR - $($_.Exception.Message)" -ForegroundColor Red
}

if ($failedCount -gt 0) {
    exit 1
}

exit 0
