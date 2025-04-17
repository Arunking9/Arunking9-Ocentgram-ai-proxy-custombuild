#!/usr/bin/env python3

import configparser
import os
from src import printcolors as pc

def setup_ai():
    config = configparser.ConfigParser(interpolation=None)
    
    # Check if config directory exists
    if not os.path.exists("config"):
        os.makedirs("config")
    
    # Check if AI config file exists
    if os.path.exists("config/ai_config.ini"):
        pc.printout("Existing AI configuration found. Do you want to overwrite it? (y/n): ", pc.YELLOW)
        if input().lower() != 'y':
            pc.printout("Setup cancelled.\n", pc.RED)
            return
    
    # Ask if user wants to enable AI features
    pc.printout("Do you want to enable AI features? (y/n): ", pc.YELLOW)
    enable_ai = input().lower() == 'y'
    
    if enable_ai:
        # Get OpenAI API key
        while True:
            pc.printout("Enter your OpenAI API key: ", pc.YELLOW)
            api_key = input().strip()
            if api_key:
                break
            pc.printout("API key cannot be empty.\n", pc.RED)
        
        # Choose model
        while True:
            pc.printout("Choose AI model (1: gpt-3.5-turbo, 2: gpt-4): ", pc.YELLOW)
            model_choice = input().strip()
            if model_choice in ['1', '2']:
                model = "gpt-3.5-turbo" if model_choice == '1' else "gpt-4"
                break
            pc.printout("Please enter 1 or 2.\n", pc.RED)
        
        # Set max tokens
        while True:
            try:
                pc.printout("Enter maximum tokens for AI responses (100-2000): ", pc.YELLOW)
                max_tokens = int(input())
                if 100 <= max_tokens <= 2000:
                    break
                pc.printout("Please enter a number between 100 and 2000.\n", pc.RED)
            except ValueError:
                pc.printout("Please enter a valid number.\n", pc.RED)
    else:
        api_key = "your_api_key_here"
        model = "gpt-3.5-turbo"
        max_tokens = 500
    
    # Create configuration
    config["OpenAI"] = {
        "enabled": str(enable_ai).lower(),
        "api_key": api_key,
        "model": model,
        "max_tokens": str(max_tokens)
    }
    
    # Write to file
    with open("config/ai_config.ini", "w") as f:
        config.write(f)
    
    pc.printout("\nAI setup completed successfully!\n", pc.GREEN)
    if enable_ai:
        pc.printout("AI features are enabled and ready to use.\n", pc.GREEN)
    else:
        pc.printout("AI features are disabled. You can enable them later by running this script again.\n", pc.YELLOW)

if __name__ == "__main__":
    setup_ai() 