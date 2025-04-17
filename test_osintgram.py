#!/usr/bin/env python3

import os
import sys
import subprocess
from src import printcolors as pc

def test_setup():
    """Test the setup process for accounts and AI"""
    print("\n=== Testing Setup Process ===")
    
    # Test account setup
    print("\n1. Testing Account Setup...")
    try:
        subprocess.run([sys.executable, "setup_accounts.py"], check=True)
        if os.path.exists("config/credentials.ini"):
            print("✓ Account setup successful")
        else:
            print("✗ Account setup failed")
            return False
    except Exception as e:
        print(f"✗ Account setup failed: {str(e)}")
        return False
    
    # Test AI setup
    print("\n2. Testing AI Setup...")
    try:
        subprocess.run([sys.executable, "setup_ai.py"], check=True)
        if os.path.exists("config/ai_config.ini"):
            print("✓ AI setup successful")
        else:
            print("✗ AI setup failed")
            return False
    except Exception as e:
        print(f"✗ AI setup failed: {str(e)}")
        return False
    
    return True

def test_osintgram():
    """Test the main Osintgram functionality"""
    print("\n=== Testing Osintgram Functionality ===")
    
    # Test basic commands
    test_commands = [
        "info",
        "followers",
        "followings",
        "hashtags",
        "posts_analysis"
    ]
    
    for cmd in test_commands:
        print(f"\nTesting command: {cmd}")
        try:
            result = subprocess.run(
                [sys.executable, "main.py", "instagram", "-c", cmd],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"✓ Command '{cmd}' successful")
            else:
                print(f"✗ Command '{cmd}' failed")
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"✗ Command '{cmd}' failed: {str(e)}")
            return False
    
    return True

def test_multi_account():
    """Test multi-account functionality"""
    print("\n=== Testing Multi-Account Functionality ===")
    
    try:
        # Test with rate limiting simulation
        print("\n1. Testing account switching...")
        result = subprocess.run(
            [sys.executable, "main.py", "instagram", "-c", "followers"],
            capture_output=True,
            text=True
        )
        
        if "rate limited" in result.stderr.lower() or "switching to next account" in result.stderr.lower():
            print("✓ Account switching working")
        else:
            print("✗ Account switching not triggered")
            return False
        
        # Test account management
        print("\n2. Testing account management...")
        if os.path.exists("config/credentials.ini"):
            with open("config/credentials.ini", "r") as f:
                content = f.read()
                if "account1" in content and "account2" in content:
                    print("✓ Multiple accounts configured")
                else:
                    print("✗ Multiple accounts not found")
                    return False
        else:
            print("✗ Credentials file not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Multi-account test failed: {str(e)}")
        return False

def test_ai_features():
    """Test AI features"""
    print("\n=== Testing AI Features ===")
    
    try:
        # Check if AI is enabled
        if os.path.exists("config/ai_config.ini"):
            with open("config/ai_config.ini", "r") as f:
                content = f.read()
                if "enabled = true" in content.lower():
                    print("✓ AI features enabled")
                else:
                    print("✗ AI features not enabled")
                    return False
        else:
            print("✗ AI config file not found")
            return False
        
        # Test AI analysis
        print("\nTesting AI analysis...")
        result = subprocess.run(
            [sys.executable, "main.py", "instagram", "-c", "posts_analysis"],
            capture_output=True,
            text=True
        )
        
        if "AI Analysis" in result.stdout:
            print("✓ AI analysis working")
        else:
            print("✗ AI analysis not working")
            return False
        
        return True
    except Exception as e:
        print(f"✗ AI features test failed: {str(e)}")
        return False

def main():
    print("Starting Osintgram Test Suite...")
    
    # Run all tests
    setup_result = test_setup()
    if not setup_result:
        print("\n✗ Setup tests failed. Please fix setup issues before continuing.")
        return
    
    osintgram_result = test_osintgram()
    if not osintgram_result:
        print("\n✗ Osintgram functionality tests failed.")
        return
    
    multi_account_result = test_multi_account()
    if not multi_account_result:
        print("\n✗ Multi-account tests failed.")
        return
    
    ai_result = test_ai_features()
    if not ai_result:
        print("\n✗ AI features tests failed.")
        return
    
    print("\n=== All Tests Completed ===")
    print("✓ Setup Tests: Passed")
    print("✓ Osintgram Tests: Passed")
    print("✓ Multi-Account Tests: Passed")
    print("✓ AI Features Tests: Passed")
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main() 