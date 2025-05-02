

# Create virtual environment folder
echo "composing venv"

if [ ! -d "venv" ]; then
    python -m venv venv
else
    echo "venv folder already exists, skipping making new venv..."
fi

# Activate virtual environment
source venv/bin/activate

echo "installing necessary libraries"
echo "models will be downloaded when first time run into cache folder"

# Install packages
pip install open_clip_torch

pip3 install torch==2.2.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 --upgrade

pip install transformers

pip install bitsandbytes --upgrade

pip install accelerate --upgrade

pip install clip-interrogator==0.6.0

pip install gradio

pip install xformers==0.0.24 --upgrade

pip install triton --upgrade

pip install deepspeed --upgrade

# Show completion message
echo "Virtual environment made and ready to use"
