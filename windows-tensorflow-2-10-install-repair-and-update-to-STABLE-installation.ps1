git stash
git pull

& $PSScriptRoot\scripts\repair_installation.ps1
& $PSScriptRoot\scripts\windows-update-ENDUSER-tf210-installation.ps1

./windows-start-octane.ps1
