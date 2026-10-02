Write-Host "============================================="
Write-Host "BANKX - MySQL Root Password Recovery Script"
Write-Host "============================================="
Write-Host "Please ensure this is running as Administrator."
Write-Host ""

$ErrorActionPreference = 'Stop'

Write-Host "[1/6] Stopping MySQL80 service..."
Stop-Service -Name MySQL80 -Force

Write-Host "[2/6] Starting MySQL temporarily without authentication..."
$mysqld = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe"
$process = Start-Process -FilePath $mysqld -ArgumentList "--skip-grant-tables", "--shared-memory" -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 5

Write-Host "[3/6] Resetting root password..."
$mysql = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$newPassword = Read-Host -Prompt "Enter your NEW MySQL root password"

# We must flush privileges before ALTER USER works when started with skip-grant-tables
$sql = "UPDATE mysql.user SET authentication_string=null WHERE User='root'; FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$newPassword'; FLUSH PRIVILEGES;"

& $mysql -u root -e $sql

Write-Host "[4/6] Stopping temporary MySQL server..."
Stop-Process -Id $process.Id -Force
Start-Sleep -Seconds 3

Write-Host "[5/6] Restarting normal MySQL80 service..."
Start-Service -Name MySQL80
Start-Sleep -Seconds 3

Write-Host "[6/6] Recovery Complete!"
Write-Host "You can now connect using the new password."
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
