@echo off
cd /d C:\Apache24\htdocs\IT_Inventory
:loop
python server.py
timeout /t 10
goto loop