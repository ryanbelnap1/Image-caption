python3 -m venv venv

source ./venv/bin/activate

echo "Installing requirements"

pip install -r requirements.txt

# Show completion message
echo "Virtual environment made and installed properly"

# Keep the terminal open
read -p "Press Enter to continue..."
