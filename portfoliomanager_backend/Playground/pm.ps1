Clear-Host
Write-Host "Starting MongoDB"
Start-Process -FilePath "C:\Program Files\MongoDB\Server\4.4\bin\mongod.exe" -ArgumentList "--auth --dbpath=c:\MongoDBDaten --bind_ip 127.0.0.1" -WindowStyle Minimized 
Write-Host "Starting PM Backend API"
Start-Process -FilePath "py" -WorkingDirectory "C:\_Development_\PortfolioManager\portfoliomanager_backend" -ArgumentList "-m API.api" -WindowStyle Minimized
Write-Host "Starting Fronend"
Start-Process -FilePath "npm" -WorkingDirectory "C:\_Development_\PortfolioManager\portfoliomanager_frontend" -ArgumentList "run serve"
