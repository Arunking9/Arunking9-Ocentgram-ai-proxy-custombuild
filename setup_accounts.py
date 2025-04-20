#!/usr/bin/env python3

import os
import sys
import argparse
import configparser
import getpass
from src.print_color import print_color
from pathlib import Path

def setup_accounts(num_accounts=1, replace_account=None):
    """Setup Instagram accounts for Osintgram"""
    try:
        config_dir = Path("config")
        config_dir.mkdir(exist_ok=True)
        
        config = configparser.ConfigParser()
        config_file = config_dir / "credentials.ini"
        
        if config_file.exists():
            config.read(config_file)
        
        if replace_account is not None:
            # Replace specific account
            account_section = f"account{replace_account}"
            if account_section in config:
                username = input(f"Enter username for account {replace_account}: ").strip()
                password = input(f"Enter password for account {replace_account}: ").strip()
                
                if not username or not password:
                    print("Error: Username and password cannot be empty!")
                    return
                
                config[account_section] = {
                    "username": username,
                    "password": password
                }
                
                with open(config_file, "w") as f:
                    config.write(f)
                
                print(f"Account {replace_account} replaced successfully!")
            else:
                print(f"Error: Account {replace_account} not found!")
        else:
            # Add new accounts
            current_accounts = [int(section.replace("account", "")) for section in config.sections() if section.startswith("account")]
            start_account = max(current_accounts) + 1 if current_accounts else 1
            
            for i in range(num_accounts):
                account_num = start_account + i
                username = input(f"Enter username for account {account_num}: ").strip()
                password = input(f"Enter password for account {account_num}: ").strip()
                
                if not username or not password:
                    print("Error: Username and password cannot be empty!")
                    continue
                
                config[f"account{account_num}"] = {
                    "username": username,
                    "password": password
                }
            
            with open(config_file, "w") as f:
                config.write(f)
            
            print(f"{num_accounts} account(s) added successfully!")
        
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
    parser = argparse.ArgumentParser(description="Setup Instagram accounts for Osintgram")
    parser.add_argument("--add", type=int, help="Number of accounts to add")
    parser.add_argument("--replace", type=int, help="Account number to replace")
    
    args = parser.parse_args()
    
    if args.replace is not None:
        setup_accounts(replace_account=args.replace)
    elif args.add is not None:
        if args.add < 1 or args.add > 10:
            print("Error: Number of accounts must be between 1 and 10!")
        else:
            setup_accounts(num_accounts=args.add)
    else:
        print("Error: Please specify either --add or --replace option!") 