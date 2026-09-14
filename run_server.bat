@echo off
title Tanglish IDE Server
echo ==================================================
echo Starting Tanglish Programming IDE Server...
echo ==================================================
echo Opening web browser at http://127.0.0.1:5000 ...
start http://127.0.0.1:5000

if exist "server.py" (
    python server.py
) else (
    python "server_file (1).txt"
)

pause
