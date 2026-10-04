@echo off
REM Doppio clic per avviare il sito in locale e il pannello di gestione.
REM Sito:     http://localhost:8080
REM Pannello: http://localhost:8080/admin
REM Per fermare tutto chiudi le due finestre nere.
cd /d "%~dp0"
start "Sito followthesandro" cmd /k python -m http.server 8080
start "Pannello - salvataggio locale" cmd /k npx --yes decap-server
timeout /t 4 >nul
start "" http://localhost:8080/admin
