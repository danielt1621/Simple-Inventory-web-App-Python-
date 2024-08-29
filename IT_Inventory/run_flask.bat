@echo off
cd /d C:\path\to\your_project_folder
:loop
python server.py
timeout /t 10
goto loop
