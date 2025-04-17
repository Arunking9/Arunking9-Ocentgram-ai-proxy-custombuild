#!/usr/bin/env python3

import os
import sys
import argparse
import configparser
import getpass
from src.print_color import print_color

def setup_accounts(num_accounts, replace=False, replace_account=None):
    """Setup Instagram accounts for Osintgram"""
    try:
        # Create config directory if it doesn't exist
        os.makedirs('config', exist_ok=True)
        
        config = configparser.ConfigParser()
        config_path = os.path.join('config', 'credentials.ini')
        
        # Check if config file exists
        if os.path.exists(config_path):
            config.read(config_path)
            current_count = int(config.get("Accounts", "count", fallback="0"))
        else:
            config["Accounts"] = {"count": "0"}
            current_count = 0
        
        if replace and replace_account:
            # Replace specific account
            account_section = f"account{replace_account}"
            if account_section not in config:
                print_color(f"Error: Account {replace_account} does not exist.", "red")
                sys.exit(1)
                
            print_color(f"\nReplacing account {replace_account}:", "yellow")
            
            while True:
                username = input("Enter Instagram username: ").strip()
                if username:
                    break
                print_color("Username cannot be empty", "red")
            
            while True:
                password = getpass.getpass("Enter Instagram password: ").strip()
                if password:
                    break
                print_color("Password cannot be empty", "red")
            
            # Only update the specific account section
            config[account_section] = {
                "username": username,
                "password": password
            }
            
            # Don't update the account count when replacing
        else:
            # Add new accounts
            start_index = current_count + 1
            for i in range(start_index, start_index + num_accounts):
                print_color(f"\nAccount {i}:", "yellow")
                
                while True:
                    username = input("Enter Instagram username: ").strip()
                    if username:
                        break
                    print_color("Username cannot be empty", "red")
                
                while True:
                    password = getpass.getpass("Enter Instagram password: ").strip()
                    if password:
                        break
                    print_color("Password cannot be empty", "red")
                
                # Add account to config
                account_section = f"account{i}"
                config[account_section] = {
                    "username": username,
                    "password": password
                }
            
            # Update account count only when adding new accounts
            config["Accounts"]["count"] = str(current_count + num_accounts)
        
        # Save configuration
        with open(config_path, 'w') as f:
            config.write(f)
        
        if replace and replace_account:
            print_color(f"\nSuccessfully replaced account {replace_account}", "green")
        else:
            print_color(f"\nSuccessfully added {num_accounts} account(s)", "green")
        print_color(f"Total accounts: {config['Accounts']['count']}", "green")
        print_color(f"Configuration saved to {config_path}", "green")
        
        # Print current accounts
        print_color("\nCurrent accounts:", "yellow")
        accounts = [s for s in config.sections() if s.startswith("account")]
        accounts.sort(key=lambda x: int(x.replace("account", "")))
        for section in accounts:
            print_color(f"Account {section.replace('account', '')}: {config[section]['username']}", "white")
        
    except Exception as e:
        print_color(f"Error setting up accounts: {str(e)}", "red")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup Instagram accounts for Osintgram')
    parser.add_argument('--add', type=int, help='Number of accounts to add')
    parser.add_argument('--replace', type=int, help='Account number to replace')
    
    args = parser.parse_args()
    
    if args.add:
        setup_accounts(args.add, replace=False)
    elif args.replace:
        setup_accounts(1, replace=True, replace_account=args.replace)
    else:
        print_color("Please specify either --add or --replace with the account number", "red")
        sys.exit(1) 