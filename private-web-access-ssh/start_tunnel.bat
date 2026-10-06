@echo off
set /p SERVER=Server IP: 
set /p USER=SSH username: 
ssh -N -L 8080:127.0.0.1:8000 %USER%@%SERVER%
pause
