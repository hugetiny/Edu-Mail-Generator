#!/usr/bin/env python3
"""
Test script to verify the setup is working correctly
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    required_modules = [
        'selenium',
        'seleniumwire',
        'webdriver_manager',
        'faker',
        'requests',
        'colorama'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_local_modules():
    """Test if local modules can be imported"""
    print("\nTesting local modules...")
    
    local_modules = [
        '__constants/const.py',
        '__banner/myBanner.py', 
        '__colors__/colors.py',
        'helper.py'
    ]
    
    failed_modules = []
    
    for module_path in local_modules:
        if os.path.exists(module_path):
            print(f"✓ {module_path} exists")
            
            # Try to import
            try:
                if module_path == '__constants/const.py':
                    from __constants.const import allColleges
                elif module_path == '__banner/myBanner.py':
                    from __banner.myBanner import bannerTop
                elif module_path == '__colors__/colors.py':
                    from __colors__.colors import fc, fg, fr
                elif module_path == 'helper.py':
                    from helper import EduHelper
                print(f"  ✓ Import successful")
            except Exception as e:
                print(f"  ✗ Import failed: {e}")
                failed_modules.append(module_path)
        else:
            print(f"✗ {module_path} missing")
            failed_modules.append(module_path)
    
    return len(failed_modules) == 0

def test_webdriver():
    """Test webdriver setup"""
    print("\nTesting webdriver setup...")
    
    try:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        # Test Chrome setup
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Test basic functionality
        driver.get('https://www.google.com')
        title = driver.title
        driver.quit()
        
        print(f"✓ Chrome webdriver working (tested with Google: {title})")
        return True
        
    except Exception as e:
        print(f"✗ Chrome webdriver failed: {e}")
        
        # Try Firefox as fallback
        try:
            from webdriver_manager.firefox import GeckoDriverManager
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            
            options = FirefoxOptions()
            options.add_argument('--headless')
            
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
            
            driver.get('https://www.google.com')
            title = driver.title
            driver.quit()
            
            print(f"✓ Firefox webdriver working (tested with Google: {title})")
            return True
            
        except Exception as e2:
            print(f"✗ Firefox webdriver also failed: {e2}")
            return False

def test_config():
    """Test configuration files"""
    print("\nTesting configuration...")
    
    config_files = ['config.json', 'prefBrowser.txt']
    missing_files = []
    
    for file in config_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            missing_files.append(file)
    
    # Test config loading
    try:
        from config import Config
        config = Config()
        print(f"✓ Config loading successful")
        print(f"  Browser: {config.get('browser')}")
        print(f"  Timeout: {config.get('timeout')}")
        return len(missing_files) == 0
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return False

def main():
    """Run all tests"""
    print("EDU MAIL GENERATOR - SETUP TEST")
    print("=" * 50)
    
    tests = [
        ("Python Modules", test_imports),
        ("Local Modules", test_local_modules),
        ("Configuration", test_config),
        ("WebDriver", test_webdriver)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name.upper()}")
        print("-" * len(test_name))
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n✓ All tests passed! Setup is working correctly.")
        print("You can now run: python edu_mail_generator.py")
        return True
    else:
        print(f"\n✗ {len(results) - passed} test(s) failed. Please check the setup.")
        print("Try running: python setup_modern.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
