git stash
git pull

& $PSScriptRoot\scripts\repair_installation.ps1
& $PSScriptRoot\scripts\windows-update-ENDUSER-installation.ps1

./windows-start-octobot.ps1
