#!/usr/bin/env python3
"""
Modern setup script for Edu Mail Generator
Automatically installs dependencies and configures the environment
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors"""
    try:
        print(f"{'[INFO]':<8} {description}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"{'[OUTPUT]':<8} {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{'[ERROR]':<8} Command failed: {command}")
        print(f"{'[ERROR]':<8} {e.stderr}")
        return False

def install_requirements():
    """Install Python requirements"""
    print("=" * 60)
    print("INSTALLING PYTHON DEPENDENCIES")
    print("=" * 60)
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def check_browsers():
    """Check for available browsers"""
    print("\n" + "=" * 60)
    print("CHECKING AVAILABLE BROWSERS")
    print("=" * 60)
    
    browsers = []
    
    # Check Chrome
    chrome_paths = [
        "google-chrome",
        "chrome",
        "chromium",
        "chromium-browser",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        try:
            if os.path.exists(path) or subprocess.run(f"which {path}", shell=True, capture_output=True).returncode == 0:
                browsers.append(("chrome", "Google Chrome"))
                browsers.append(("chrome_undetected", "Chrome Undetected (Recommended)"))
                print(f"{'[FOUND]':<8} Google Chrome")
                break
        except:
            continue
    
    # Check Firefox
    firefox_paths = [
        "firefox",
        r"C:\Program Files\Mozilla Firefox\firefox.exe",
        r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        "/Applications/Firefox.app/Contents/MacOS/firefox"
    ]
    
    for path in firefox_paths:
        try:
            if os.path.exists(path) or subprocess.run(f"which {path}", shell=True, capture_output=True).returncode == 0:
                browsers.append(("firefox", "Mozilla Firefox"))
                print(f"{'[FOUND]':<8} Mozilla Firefox")
                break
        except:
            continue
    
    if not browsers:
        print(f"{'[ERROR]':<8} No supported browsers found!")
        print(f"{'[INFO]':<8} Please install Google Chrome or Mozilla Firefox")
        return None
    
    return browsers

def select_browser(browsers):
    """Let user select preferred browser"""
    print("\n" + "=" * 60)
    print("BROWSER SELECTION")
    print("=" * 60)
    
    print("Available browsers:")
    for i, (key, name) in enumerate(browsers, 1):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice = input(f"\nSelect browser (1-{len(browsers)}): ").strip()
            index = int(choice) - 1
            if 0 <= index < len(browsers):
                selected = browsers[index]
                print(f"{'[SELECTED]':<8} {selected[1]}")
                return selected[0]
            else:
                print(f"{'[ERROR]':<8} Please enter a number between 1 and {len(browsers)}")
        except ValueError:
            print(f"{'[ERROR]':<8} Please enter a valid number")

def create_config_files(browser_choice):
    """Create configuration files"""
    print("\n" + "=" * 60)
    print("CREATING CONFIGURATION FILES")
    print("=" * 60)
    
    # Create prefBrowser.txt for compatibility
    try:
        with open('prefBrowser.txt', 'w') as f:
            f.write(browser_choice)
        print(f"{'[CREATED]':<8} prefBrowser.txt")
    except Exception as e:
        print(f"{'[ERROR]':<8} Failed to create prefBrowser.txt: {e}")
        return False
    
    # Create config.json
    try:
        config = {
            "browser": browser_choice,
            "headless": False,
            "timeout": 60,
            "retry_attempts": 3,
            "delay_between_actions": 0.7,
            "captcha_timeout": 200,
            "output_file": "generated_accounts.txt",
            "log_level": "INFO"
        }
        
        import json
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        print(f"{'[CREATED]':<8} config.json")
    except Exception as e:
        print(f"{'[ERROR]':<8} Failed to create config.json: {e}")
        return False
    
    return True

def create_env_example():
    """Create .env.example file"""
    try:
        env_content = """# Environment Variables for Edu Mail Generator
# Copy this file to .env and fill in your values

# Your email address (will be used as contact email)
EDU_EMAIL=your-email@example.com

# Alternative: GitHub email (for GitHub Actions)
GITHUB_EMAIL=your-github-email@example.com

# Optional: Custom output file path
OUTPUT_FILE=generated_accounts.txt

# Optional: Log level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
"""
        with open('.env.example', 'w') as f:
            f.write(env_content)
        print(f"{'[CREATED]':<8} .env.example")
        return True
    except Exception as e:
        print(f"{'[ERROR]':<8} Failed to create .env.example: {e}")
        return False

def main():
    """Main setup function"""
    print("EDU MAIL GENERATOR - MODERN SETUP")
    print("=" * 60)
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    
    # Install requirements
    if not install_requirements():
        print(f"\n{'[FAILED]':<8} Setup failed during dependency installation")
        return False
    
    # Check browsers
    browsers = check_browsers()
    if not browsers:
        print(f"\n{'[FAILED]':<8} Setup failed - no browsers found")
        return False
    
    # Select browser
    browser_choice = select_browser(browsers)
    
    # Create config files
    if not create_config_files(browser_choice):
        print(f"\n{'[FAILED]':<8} Setup failed during configuration")
        return False
    
    # Create environment example
    create_env_example()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"{'[INFO]':<8} Selected browser: {browser_choice}")
    print(f"{'[INFO]':<8} Configuration saved to config.json")
    print(f"{'[INFO]':<8} Browser preference saved to prefBrowser.txt")
    print(f"{'[INFO]':<8} Environment template created: .env.example")
    print()
    print("NEXT STEPS:")
    print("1. Copy .env.example to .env and configure your email")
    print("2. Run: python edu_mail_generator.py")
    print("3. Or run the original: python bot.py")
    print()
    print("For GitHub Actions, set EDU_EMAIL in repository secrets")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{'[CANCELLED]':<8} Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{'[ERROR]':<8} Unexpected error: {e}")
        sys.exit(1)
