@echo off
setlocal

REM --- Check if virtual environment exists ---
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Please run: python -m venv .venv
    echo Then run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM --- Activate and run in the SAME shell ---
call ".venv\Scripts\activate.bat"

echo Starting Django dev server on http://127.0.0.1:8080/ ...
echo Using stat reloader for Windows file watching...

REM --- Run server with stat reloader ---
python manage.py runserver_plus 8080 --reloader-type stat

REM --- Keep window open on crash so you can read the error ---
if errorlevel 1 (
    echo.
    echo [ERROR] Server exited with an error. Check the traceback above.
    pause
)

endlocal