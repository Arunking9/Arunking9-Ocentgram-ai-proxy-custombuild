import configparser
import sys
import random
from typing import List, Dict, Tuple
from src import printcolors as pc
import os
import json
from pathlib import Path

class AccountManager:
    def __init__(self):
        self.accounts: List[Dict[str, str]] = []
        self.current_account_index = 0
        self.load_accounts()
    
    def load_accounts(self):
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read("config/credentials.ini")
            
            if "Accounts" not in config:
                pc.printout('Error: No "Accounts" section found in "config/credentials.ini"\n', pc.RED)
                sys.exit(0)
            
            # Debug: Print all sections
            pc.printout(f'Found sections: {config.sections()}\n', pc.YELLOW)
            
            # Get account count
            try:
                account_count = int(config["Accounts"]["count"])
                pc.printout(f'Found {account_count} accounts in config\n', pc.GREEN)
            except (ValueError, KeyError) as e:
                pc.printout(f'Error reading account count: {str(e)}\n', pc.RED)
                account_count = 0
            
            # Load all accounts up to count
            for i in range(1, account_count + 1):
                section = f"account{i}"
                pc.printout(f'Checking section: {section}\n', pc.YELLOW)
                
                if section in config:
                    try:
                        username = config[section]["username"]
                        password = config[section]["password"]
                        
                        if username and password:
                            self.accounts.append({
                                "name": section,
                                "username": username,
                                "password": password,
                                "is_blocked": False,
                                "last_used": None
                            })
                            pc.printout(f'Loaded account {i}: {username}\n', pc.GREEN)
                        else:
                            pc.printout(f'Error: Missing credentials for {section}\n', pc.YELLOW)
                    except KeyError as e:
                        pc.printout(f'Error loading account {section}: {str(e)}\n', pc.YELLOW)
                else:
                    pc.printout(f'Warning: Account section {section} not found\n', pc.YELLOW)
                    
            if not self.accounts:
                pc.printout('Error: No valid accounts found in "config/credentials.ini"\n', pc.RED)
                sys.exit(0)
                
            pc.printout(f'Successfully loaded {len(self.accounts)} accounts\n', pc.GREEN)
                
        except FileNotFoundError:
            pc.printout('Error: file "config/credentials.ini" not found!\n', pc.RED)
            sys.exit(0)
        except Exception as e:
            pc.printout(f"Error: {str(e)}\n", pc.RED)
            sys.exit(0)
    
    def get_next_account(self) -> Dict[str, str]:
        """Get the next available account, rotating through the list"""
        if not self.accounts:
            pc.printout('Error: No accounts available\n', pc.RED)
            sys.exit(0)
            
        # Try to find an unblocked account
        for _ in range(len(self.accounts)):
            account = self.accounts[self.current_account_index]
            self.current_account_index = (self.current_account_index + 1) % len(self.accounts)
            
            if not account["is_blocked"]:
                pc.printout(f'Using account: {account["username"]}\n', pc.CYAN)
                return account
                
        # If all accounts are blocked, reset them and try again
        self.reset_blocked_accounts()
        return self.get_next_account()
    
    def mark_account_blocked(self, username: str):
        """Mark an account as blocked"""
        for account in self.accounts:
            if account["username"] == username:
                account["is_blocked"] = True
                pc.printout(f'Account {username} marked as blocked\n', pc.YELLOW)
                break
    
    def reset_blocked_accounts(self):
        """Reset all blocked accounts"""
        for account in self.accounts:
            account["is_blocked"] = False
        pc.printout('All accounts have been reset\n', pc.YELLOW)

# Create a global account manager instance
account_manager = AccountManager()

def get_next_account():
    """Get the next available Instagram account credentials"""
    return account_manager.get_next_account()

def mark_account_blocked(username):
    """Mark an account as being rate limited"""
    account_manager.mark_account_blocked(username)

def reset_blocked_accounts():
    """Reset all blocked accounts"""
    account_manager.reset_blocked_accounts()
