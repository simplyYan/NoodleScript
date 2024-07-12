#!/bin/bash

set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Python if not installed
if ! command_exists python3; then
    echo "Python3 is not installed. Installing Python3..."
    if command_exists brew; then
        brew install python
    else
        echo "Homebrew is not installed. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        brew install python
    fi
else
    echo "Python3 is already installed."
fi

# Ensure pip is up-to-date
python3 -m ensurepip --upgrade

# Install PyInstaller
echo "Installing PyInstaller..."
python3 -m pip install --upgrade pip
python3 -m pip install pyinstaller

# Download the NoodleScript script
echo "Downloading NoodleScript script..."
curl -o ~/main.py https://raw.githubusercontent.com/simplyYan/NoodleScript/main/src/main.py

# Compile the script using PyInstaller
echo "Compiling NoodleScript script..."
cd ~
pyinstaller --onefile --name NoodleScript main.py

# Move the compiled executable to a convenient location
mv dist/NoodleScript ~/NoodleScript

# Clean up
rm -rf build dist main.spec main.py

echo "NoodleScript installation is complete."
echo "You can now run NoodleScript using ~/NoodleScript"

# Prompt the user to add the executable to their PATH
echo "Would you like to add NoodleScript to your PATH? (y/n)"
read -r add_to_path
if [ "$add_to_path" = "y" ]; then
    echo 'export PATH=$PATH:~' >> ~/.bash_profile
    source ~/.bash_profile
    echo "NoodleScript has been added to your PATH. You can now run it using the command 'NoodleScript'."
else
    echo "You chose not to add NoodleScript to your PATH. You can run it using '~/NoodleScript'."
fi

