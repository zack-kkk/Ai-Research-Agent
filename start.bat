@echo off

cd /d %~dp0

echo Starting AI Research Agent...

start cmd /k "uvicorn main:app --reload"

timeout /t 5

start index.html

echo System started successfully.
pause