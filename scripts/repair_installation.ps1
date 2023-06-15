if (!(Get-Command pip -ErrorAction SilentlyContinue)) {
  # Install Python 3.10 for all users
  # windows_dependencies/python-3.10.9-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
  windows_dependencies/python-3.10.9-amd64.exe InstallAllUsers=1 PrependPath=1 Include_test=0
  Write-Host -NoNewLine 'Once the Python installation is completed, press any key to continue...';
  $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');
  $Env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")  
  # start powershell {.\windows-install-repair-or-update-DEVELOPER-installation.ps1}
}



Remove-Item .venv\ -Force  -Recurse -ErrorAction SilentlyContinue

cd octobot-packages
Get-ChildItem *.c -Recurse | foreach { Remove-Item -Path $_.FullName }
Get-ChildItem *.pyd -Recurse | foreach { Remove-Item -Path $_.FullName }

cd ..


python -m venv .venv

New-Item -Path "./" -Name "user" -ItemType "directory"  -ErrorAction SilentlyContinue


$sourceFile = 'octobot-packages/OctoBot/octobot/config/default_config.json'
$destinationFile = 'user/config.json'
if (-not (test-path $destinationFile))
{
  $opts = @{'path' = $sourceFile; 'destination' = $destinationFile; 'confirm' = $false}
  copy-item @opts
}

$sourceFile = 'scripts/.env-example-windows'
$destinationFile = '.env'
if (-not (test-path $destinationFile))
{
  $opts = @{'path' = $sourceFile; 'destination' = $destinationFile; 'confirm' = $false}
  copy-item @opts
}
