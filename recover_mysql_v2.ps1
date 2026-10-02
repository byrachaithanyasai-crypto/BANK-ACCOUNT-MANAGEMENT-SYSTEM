Write-Host "============================================="
Write-Host "BANKX - MySQL Root Password Recovery Script v2"
Write-Host "============================================="

$ErrorActionPreference = 'Stop'

# 1. Stop MySQL80 if running
$svc = Get-Service -Name MySQL80 -ErrorAction SilentlyContinue
if ($svc -and $svc.Status -eq 'Running') {
    Write-Host "[1/9] Stopping MySQL80 service..."
    Stop-Service -Name MySQL80 -Force
} else {
    Write-Host "[1/9] MySQL80 is already stopped."
}

# 2. Check port 3306
$portInUse = netstat -ano | Select-String ":3306 "
if ($portInUse) {
    Write-Host "ERROR: Port 3306 is still in use! Please kill the process using it."
    exit 1
}

# 3. Start mysqld temporarily
Write-Host "[2/9] Starting MySQL temporarily without authentication..."
$mysqld = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqld.exe"
$myini = "C:\ProgramData\MySQL\MySQL Server 8.0\my.ini"
$logFile = "$PWD\mysqld_temp.log"

if (Test-Path $logFile) { Remove-Item $logFile -Force }

$args = @("--defaults-file=$myini", "--skip-grant-tables", "--shared-memory")
$process = Start-Process -FilePath $mysqld -ArgumentList $args -PassThru -WindowStyle Hidden -RedirectStandardOutput $logFile -RedirectStandardError $logFile

# 4. Wait for readiness
Write-Host "[3/9] Waiting for MySQL server to become ready (up to 30s)..."
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    if ($process.HasExited) {
        Write-Host "ERROR: mysqld exited unexpectedly!"
        Write-Host "--- LOG OUTPUT ---"
        Get-Content $logFile | Select-Object -Last 20
        exit 1
    }
    
    $check = netstat -ano | Select-String ":3306 "
    if ($check) {
        $ready = $true
        break
    }
    Start-Sleep -Seconds 1
}

if (-not $ready) {
    Write-Host "ERROR: MySQL did not open port 3306 within 30 seconds."
    Stop-Process -Id $process.Id -Force
    exit 1
}

Write-Host "[4/9] MySQL is ready on port 3306!"

# 5. Connect and reset
Write-Host "[5/9] Resetting root password..."
$mysql = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$newPassword = Read-Host -Prompt "Enter your NEW MySQL root password"

Write-Host "[6/9] Applying password update..."
try {
    $sql = "UPDATE mysql.user SET authentication_string=null WHERE User='root'; FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$newPassword'; FLUSH PRIVILEGES;"
    & $mysql -u root -e $sql
    Write-Host "[7/9] Password updated successfully."
} catch {
    Write-Host "ERROR running mysql command: $_"
}

# 6. Stop temporary server
Write-Host "[8/9] Stopping temporary MySQL server..."
Stop-Process -Id $process.Id -Force
Start-Sleep -Seconds 3

# 7. Start normal service
Write-Host "[9/9] Restarting normal MySQL80 service..."
Start-Service -Name MySQL80
Start-Sleep -Seconds 3

Write-Host "Recovery Complete!"
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
