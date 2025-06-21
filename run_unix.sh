#!/bin/bash

echo "EDU MAIL GENERATOR - Unix Launcher"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "Python found: $(python3 --version)"

# Check if setup has been run
if [ ! -f "config.json" ]; then
    echo ""
    echo "Configuration not found. Running setup..."
    python3 setup_modern.py
    if [ $? -ne 0 ]; then
        echo "Setup failed!"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found"
    echo "Please copy .env.example to .env and configure your email"
    echo ""
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]; then
        echo "Cancelled by user"
        exit 0
    fi
fi

# Run the generator
echo ""
echo "Starting Edu Mail Generator..."
echo ""
python3 edu_mail_generator.py

echo ""
echo "Generator finished. Check generated_accounts.txt for results."
