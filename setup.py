#!/usr/bin/env python3
"""
Setup script for AI Resume Analyzer
This script will help you install dependencies and set up the environment.
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def main():
    print("🚀 AI Resume Analyzer Setup")
    print("=" * 40)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required!")
        print(f"Current version: {python_version.major}.{python_version.minor}")
        return
    
    print(f"✅ Python version: {python_version.major}.{python_version.minor}")
    
    # Install required packages
    print("\n📦 Installing required packages...")
    packages = ["openai"]
    
    for package in packages:
        install_package(package)
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Get your OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Open resume_analyzer.py in a text editor")
    print("3. Replace 'your-api-key-here' with your actual API key")
    print("4. Run: python resume_analyzer.py")
    
    print("\n💡 Tips:")
    print("- Keep your API key secure and never share it")
    print("- The first analysis will use the example resume")
    print("- You can then analyze your own resume interactively")
    print("- Each API call costs money (GPT-4 is more expensive than GPT-3.5)")

if __name__ == "__main__":
    main() 