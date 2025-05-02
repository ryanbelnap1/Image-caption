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

pip install open_clip_torch

pip3 install torch==2.2.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade

pip install transformers

pip install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.2.post2-py3-none-win_amd64.whl --upgrade

pip install accelerate

pip install clip-interrogator==0.6.0

pip install gradio


pip install xformers==0.0.24 --upgrade

echo installing triton-2.1.0

pip install https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/triton-2.1.0-cp310-cp310-win_amd64.whl --upgrade

echo installing requirements

pip install https://huggingface.co/MonsterMMORPG/SECourses/resolve/main/deepspeed-0.11.2_cuda121-cp310-cp310-win_amd64.whl --upgrade

REM Show completion message
echo Virtual environment made and ready to use

REM Pause to keep the command prompt open
pause