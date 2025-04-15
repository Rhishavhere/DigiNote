@echo off
set FULL_IMAGE_PATH=%~f1
cd /d "E:\CodeRepo\DigiNotes"
call venv\Scripts\activate
python "E:\CodeRepo\DigiNotes\main.py" "%FULL_IMAGE_PATH%"
pause