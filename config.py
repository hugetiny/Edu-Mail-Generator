import os
import json
from typing import Dict, Any

class Config:
    """Configuration management for Edu Mail Generator"""
    
    def __init__(self):
        self.config_file = 'config.json'
        self.default_config = {
            'browser': 'chrome_undetected',
            'headless': False,
            'timeout': 60,
            'retry_attempts': 3,
            'delay_between_actions': 0.7,
            'captcha_timeout': 200,
            'output_file': 'generated_accounts.txt',
            'log_level': 'INFO'
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config
        else:
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file"""
        if config is None:
            config = self.config
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
    
    def get_email_from_env(self) -> str:
        """Get email from environment variable or GitHub secrets"""
        email = os.getenv('EDU_EMAIL')
        if not email:
            # Try to get from GitHub Actions secrets
            email = os.getenv('GITHUB_EMAIL')
        if not email:
            # Fallback to asking user
            email = input("Enter your email address: ")
        return email
    
    def get_browser_preference(self) -> str:
        """Get browser preference from config or ask user"""
        browser = self.get('browser')
        if not browser or browser == '':
            print("\nAvailable browsers:")
            print("1. chrome - Regular Chrome")
            print("2. firefox - Firefox")
            print("3. chrome_undetected - Undetected Chrome (Recommended)")
            
            while True:
                choice = input("Select browser (1-3): ").strip()
                if choice == '1':
                    browser = 'chrome'
                    break
                elif choice == '2':
                    browser = 'firefox'
                    break
                elif choice == '3':
                    browser = 'chrome_undetected'
                    break
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            
            self.set('browser', browser)
            
            # Save to prefBrowser.txt for compatibility
            with open('prefBrowser.txt', 'w') as f:
                f.write(browser)
        
        return browser
