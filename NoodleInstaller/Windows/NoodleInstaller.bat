@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python...
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -NoNewWindow -Wait"
) else (
    echo Python is already installed.
)

:: Ensure pip is up-to-date
python -m ensurepip
python -m pip install --upgrade pip

:: Install PyInstaller
echo Installing PyInstaller...
python -m pip install pyinstaller

:: Download the NoodleScript script
echo Downloading NoodleScript script...
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/simplyYan/NoodleScript/main/src/main.py' -OutFile '%USERPROFILE%\main.py'"

:: Compile the script using PyInstaller
echo Compiling NoodleScript script...
cd %USERPROFILE%
pyinstaller --onefile --name NoodleScript main.py

:: Move the compiled executable to a convenient location
move dist\NoodleScript.exe %USERPROFILE%\NoodleScript.exe

:: Clean up
rd /s /q build
del main.spec
del main.py
del /s /q dist

echo NoodleScript installation is complete.
echo You can now run NoodleScript using %USERPROFILE%\NoodleScript.exe

endlocal
pause
