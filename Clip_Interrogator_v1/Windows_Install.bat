@echo off

REM Create virtual environment folder
echo composing venv
IF NOT EXIST venv (
    python -m venv venv
) ELSE (
    echo venv folder already exists, skipping making new venv...
)
call .\venv\Scripts\activate.bat

echo installing necessary libraries
echo models will be downloaded when first time run into cache folder
REM Install packages from requirements.txt

pip install -r requirements.txt

REM Show completion message
echo Virtual environment made and ready to use

REM Pause to keep the command prompt open
pause