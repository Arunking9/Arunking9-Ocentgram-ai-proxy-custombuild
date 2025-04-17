import configparser
import sys
from typing import Dict, List, Tuple

from src import printcolors as pc

try:
    config = configparser.ConfigParser(interpolation=None)
    config.read("config/credentials.ini")
except FileNotFoundError:
    pc.printout('Error: file "config/credentials.ini" not found!\n', pc.RED)
    sys.exit(0)
except Exception as e:
    pc.printout("Error: {}\n".format(e), pc.RED)
    sys.exit(0)

def get_accounts() -> List[Tuple[str, str]]:
    """Get all configured Instagram accounts."""
    try:
        accounts = []
        for account_name, credentials in config["Accounts"].items():
            username, password = credentials.split(":")
            accounts.append((username.strip(), password.strip()))
        
        if not accounts:
            pc.printout('Error: No accounts configured in "config/credentials.ini"\n', pc.RED)
            sys.exit(0)
            
        return accounts
    except KeyError:
        pc.printout('Error: Missing "Accounts" section in "config/credentials.ini"\n', pc.RED)
        sys.exit(0)
    except ValueError:
        pc.printout('Error: Invalid account format in "config/credentials.ini". Use username:password format\n', pc.RED)
        sys.exit(0)

def get_settings() -> Dict[str, int]:
    """Get settings from config file."""
    settings = {
        "max_accounts": 3,
        "switch_delay": 60
    }
    
    try:
        if "Settings" in config:
            if "max_accounts" in config["Settings"]:
                settings["max_accounts"] = int(config["Settings"]["max_accounts"])
            if "switch_delay" in config["Settings"]:
                settings["switch_delay"] = int(config["Settings"]["switch_delay"])
    except ValueError:
        pc.printout('Error: Invalid settings values in "config/credentials.ini"\n', pc.RED)
        sys.exit(0)
        
    return settings

# Legacy functions for backward compatibility
def getUsername():
    accounts = get_accounts()
    return accounts[0][0] if accounts else None

def getPassword():
    accounts = get_accounts()
    return accounts[0][1] if accounts else None
