if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -notmatch '^\s*#' -and $_ -match '=') {
            $parts = $_ -split '=',2
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            $Env:$key = $value
        }
    }
}
.venv\Scripts\Activate.ps1
Octane