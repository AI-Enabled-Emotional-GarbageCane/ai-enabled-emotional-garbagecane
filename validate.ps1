param(
    [string]$Python = $env:PYTHON
)

$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if ([string]::IsNullOrWhiteSpace($Python)) {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $Python = "python"
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        $Python = "py"
    } else {
        Write-Error "Python was not found. Install Python 3 or set the PYTHON environment variable."
        exit 1
    }
}

if ($Python -eq "py") {
    & py -3 scripts/validate-contract.py
} else {
    & $Python scripts/validate-contract.py
}

exit $LASTEXITCODE
