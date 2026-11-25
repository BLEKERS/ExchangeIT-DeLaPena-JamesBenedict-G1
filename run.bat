@echo off
setlocal
REM --- Activate and run in the SAME shell ---
call ".venv\Scripts\activate.bat"

echo Starting Django dev server on http://127.0.0.1:8080/ ...
python manage.py runserver_plus 8080

REM --- Keep window open on crash so you can read the error ---
if errorlevel 1 (
    echo.
    echo [ERROR] Server exited with an error.
    pause
)

endlocal