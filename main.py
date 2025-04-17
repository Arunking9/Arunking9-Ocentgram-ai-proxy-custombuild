#!/usr/bin/env python3

from src.Osintgram import Osintgram
import argparse
<<<<<<< HEAD
from src import printcolors as pc
from src import artwork
import sys
import signal

is_windows = False

try:
    import gnureadline  
except: 
    is_windows = True
    import pyreadline


def printlogo():
    pc.printout(artwork.ascii_art, pc.YELLOW)
    pc.printout("\nVersion 1.1 - Developed by Giuseppe Criscione\n\n", pc.YELLOW)
    pc.printout("Type 'list' to show all allowed commands\n")
    pc.printout("Type 'FILE=y' to save results to files like '<target username>_<command>.txt (default is disabled)'\n")
    pc.printout("Type 'FILE=n' to disable saving to files'\n")
    pc.printout("Type 'JSON=y' to export results to a JSON files like '<target username>_<command>.json (default is "
                "disabled)'\n")
    pc.printout("Type 'JSON=n' to disable exporting to files'\n")


def cmdlist():
    pc.printout("FILE=y/n\t")
    print("Enable/disable output in a '<target username>_<command>.txt' file'")
    pc.printout("JSON=y/n\t")
    print("Enable/disable export in a '<target username>_<command>.json' file'")
    pc.printout("setup\t\t")
    print("Setup Instagram accounts and switch delay")
    pc.printout("accounts\t")
    print("Show current account status and switch accounts")
    pc.printout("addrs\t\t")
    print("Get all registered addressed by target photos")
    pc.printout("cache\t\t")
    print("Clear cache of the tool")
    pc.printout("captions\t")
    print("Get target's photos captions")
    pc.printout("commentdata\t")
    print("Get a list of all the comments on the target's posts")
    pc.printout("comments\t")
    print("Get total comments of target's posts")
    pc.printout("followers\t")
    print("Get target followers")
    pc.printout("followings\t")
    print("Get users followed by target")
    pc.printout("fwersemail\t")
    print("Get email of target followers")
    pc.printout("fwingsemail\t")
    print("Get email of users followed by target")
    pc.printout("fwersnumber\t")
    print("Get phone number of target followers")
    pc.printout("fwingsnumber\t")
    print("Get phone number of users followed by target")    
    pc.printout("hashtags\t")
    print("Get hashtags used by target")
    pc.printout("info\t\t")
    print("Get target info")
    pc.printout("likes\t\t")
    print("Get total likes of target's posts")
    pc.printout("mediatype\t")
    print("Get target's posts type (photo or video)")
    pc.printout("photodes\t")
    print("Get description of target's photos")
    pc.printout("photos\t\t")
    print("Download target's photos in output folder")
    pc.printout("propic\t\t")
    print("Download target's profile picture")
    pc.printout("stories\t\t")
    print("Download target's stories")
    pc.printout("tagged\t\t")
    print("Get list of users tagged by target")
    pc.printout("target\t\t")
    print("Set new target")
    pc.printout("wcommented\t")
    print("Get a list of user who commented target's photos")
    pc.printout("wtagged\t\t")
    print("Get a list of user who tagged target")


def signal_handler(sig, frame):
    pc.printout("\nGoodbye!\n", pc.RED)
    sys.exit(0)

=======
from src.print_color import print_color
import src.artwork as artwork
import sys
import signal
import os
import subprocess
import configparser

def signal_handler(sig, frame):
    print_color("\nGoodbye!\n", "red")
    sys.exit(0)

try:
    import readline
    readline_available = True
except ImportError:
    readline_available = False

# Define available commands
commands = [
    'list', 'help', 'quit', 'exit',
    'addrs', 'cache', 'captions', 'commentdata',
    'comments', 'followers', 'followings',
    'fwersemail', 'fwingsemail', 'fwersnumber',
    'fwingsnumber', 'hashtags', 'info', 'likes',
    'mediatype', 'photodes', 'photos', 'propic',
    'stories', 'tagged', 'target', 'wcommented',
    'wtagged', 'file=y', 'file=n', 'json=y', 'json=n'
]
>>>>>>> 5473b8d (Secon commit)

def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def _quit():
<<<<<<< HEAD
    pc.printout("Goodbye!\n", pc.RED)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
if is_windows:
    pyreadline.Readline().parse_and_bind("tab: complete")
    pyreadline.Readline().set_completer(completer)
else:
    gnureadline.parse_and_bind("tab: complete")
    gnureadline.set_completer(completer)

parser = argparse.ArgumentParser(description='Osintgram is a OSINT tool on Instagram. It offers an interactive shell '
                                             'to perform analysis on Instagram account of any users by its nickname ')
parser.add_argument('id', type=str,  # var = id
                    help='username')
parser.add_argument('-C','--cookies', help='clear\'s previous cookies', action="store_true")
parser.add_argument('-j', '--json', help='save commands output as JSON file', action='store_true')
parser.add_argument('-f', '--file', help='save output in a file', action='store_true')
parser.add_argument('-c', '--command', help='run in single command mode & execute provided command', action='store')
parser.add_argument('-o', '--output', help='where to store photos', action='store')

args = parser.parse_args()


api = Osintgram(args.id, args.file, args.json, args.command, args.output, args.cookies)



commands = {
    'list':             cmdlist,
    'help':             cmdlist,
    'quit':             _quit,
    'exit':             _quit,
    'setup':            api.setup_accounts,
    'accounts':         api.show_account_status,
    'addrs':            api.get_addrs,
    'cache':            api.clear_cache,
    'captions':         api.get_captions,
    "commentdata":      api.get_comment_data,
    'comments':         api.get_total_comments,
    'followers':        api.get_followers,
    'followings':       api.get_followings,
    'fwersemail':       api.get_fwersemail,
    'fwingsemail':      api.get_fwingsemail,
    'fwersnumber':      api.get_fwersnumber,
    'fwingsnumber':     api.get_fwingsnumber,
    'hashtags':         api.get_hashtags,
    'info':             api.get_user_info,
    'likes':            api.get_total_likes,
    'mediatype':        api.get_media_type,
    'photodes':         api.get_photo_description,
    'photos':           api.get_user_photo,
    'propic':           api.get_user_propic,
    'stories':          api.get_user_stories,
    'tagged':           api.get_people_tagged_by_user,
    'target':           api.change_target,
    'wcommented':       api.get_people_who_commented,
    'wtagged':          api.get_people_who_tagged
}


signal.signal(signal.SIGINT, signal_handler)
if is_windows:
    pyreadline.Readline().parse_and_bind("tab: complete")
    pyreadline.Readline().set_completer(completer)
else:
    gnureadline.parse_and_bind("tab: complete")
    gnureadline.set_completer(completer)

if not args.command:
    printlogo()


while True:
    if args.command:
        cmd = args.command
        _cmd = commands.get(args.command)
    else:
        signal.signal(signal.SIGINT, signal_handler)
        if is_windows:
            pyreadline.Readline().parse_and_bind("tab: complete")
            pyreadline.Readline().set_completer(completer)
        else:
            gnureadline.parse_and_bind("tab: complete")
            gnureadline.set_completer(completer)
        pc.printout("Run a command: ", pc.YELLOW)
        cmd = input()

        _cmd = commands.get(cmd)

    if _cmd:
        _cmd()
    elif cmd == "FILE=y":
        api.set_write_file(True)
    elif cmd == "FILE=n":
        api.set_write_file(False)
    elif cmd == "JSON=y":
        api.set_json_dump(True)
    elif cmd == "JSON=n":
        api.set_json_dump(False)
    elif cmd == "":
        print("")
    else:
        pc.printout("Unknown command\n", pc.RED)

    if args.command:
        break
=======
    print_color("Goodbye!\n", "red")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Set up readline completion if available
if readline_available:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

def print_banner():
    banner = r"""
________         .__        __                               
\_____  \   _____|__| _____/  |_  ________________    _____  
 /   |   \ /  ___/  |/    \   __\/ ___\_  __ \__  \  /     \ 
/    |    \\___ \|  |   |  \  | / /_/  >  | \// __ \|  Y Y  \\
\_______  /____  >__|___|  /__| \___  /|__|  (____  /__|_|  /
        \/     \/        \/    /_____/            \/      \/ 
"""
    print_color(banner, "cyan")
    print_color("\nVersion 1.1[Custom-Build] - DemonKing369\n", "yellow")

def print_commands():
    commands = """
Run a command: list
FILE=y/n        Enable/disable output in a '<target username>_<command>.txt' file'
JSON=y/n        Enable/disable export in a '<target username>_<command>.json' file'
addrs           Get all registered addressed by target photos
cache           Clear cache of the tool
captions        Get target's photos captions
commentdata     Get a list of all the comments on the target's posts
comments        Get total comments of target's posts
followers       Get target followers
followings      Get users followed by target
fwersemail      Get email of target followers
fwingsemail     Get email of users followed by target
fwersnumber     Get phone number of target followers
fwingsnumber    Get phone number of users followed by target
hashtags        Get hashtags used by target
info            Get target info
likes           Get total likes of target's posts
mediatype       Get target's posts type (photo or video)
photodes        Get description of target's photos
photos          Download target's photos in output folder
propic          Download target's profile picture
stories         Download target's stories
tagged          Get list of users tagged by target
target          Set new target
wcommented      Get a list of user who commented target's photos
wtagged         Get a list of user who tagged target
"""
    print_color(commands, "white")

def check_accounts():
    """Check if accounts are configured, if not run setup"""
    try:
        if not os.path.exists("config/credentials.ini"):
            print_color("No Instagram accounts configured.\n", "yellow")
            print_color("Would you like to set up your accounts now? (y/n): ", "yellow")
            if input().lower() == 'y':
                subprocess.run([sys.executable, "setup_accounts.py"])
                if not os.path.exists("config/credentials.ini"):
                    print_color("Account setup failed. Please run setup_accounts.py manually.\n", "red")
                    sys.exit(1)
            else:
                print_color("Please run setup_accounts.py to configure your accounts.\n", "red")
                sys.exit(1)
        
        print_color("\nChecking Instagram accounts...", "yellow")
        # Your existing account checking code here
        print_color("Successfully loaded accounts", "green")
    except Exception as e:
        print_color(f"Error checking accounts: {str(e)}", "red")
        sys.exit(1)

def get_user_info_safe(osint, target):
    """Safely get user info with proper error handling"""
    try:
        # Try to get user info using the API
        user_info = osint.get_user_info()
        if user_info:
            return user_info
    except KeyError as e:
        if 'data' in str(e):
            print_color("Warning: Instagram API returned unexpected response", "yellow")
            print_color("Trying alternative method...", "yellow")
            try:
                # Try alternative method to get user info
                user_info = osint.get_user_info_by_username(target)
                if user_info:
                    return user_info
            except Exception as e:
                if "not found" in str(e).lower():
                    print_color("Account does not exist or has been deleted", "red")
                elif "private" in str(e).lower():
                    print_color("Account is private", "red")
                else:
                    print_color("Could not fetch user info using alternative method", "yellow")
    except Exception as e:
        if "not found" in str(e).lower():
            print_color("Account does not exist or has been deleted", "red")
        elif "private" in str(e).lower():
            print_color("Account is private", "red")
        else:
            print_color(f"Error fetching user info: {str(e)}", "yellow")
    
    return None

def check_account_exists(osint, target):
    """Check if account exists and its privacy status"""
    try:
        # Try to get user info
        user_info = osint.get_user_info()
        if user_info:
            return True, user_info.get('is_private', False)
    except Exception as e:
        if "not found" in str(e).lower():
            return False, False
        elif "private" in str(e).lower():
            return True, True
        else:
            try:
                # Try alternative method
                user_info = osint.get_user_info_by_username(target)
                if user_info:
                    return True, user_info.get('is_private', False)
            except Exception as e:
                if "not found" in str(e).lower():
                    return False, False
                elif "private" in str(e).lower():
                    return True, True
    
    return None, None

def load_proxy_settings():
    """Load proxy settings from config/proxy.ini"""
    proxy_config = {
        'enabled': False,
        'host': None,
        'port': None,
        'username': None,
        'password': None
    }
    
    try:
        if os.path.exists("config/proxy.ini"):
            config = configparser.ConfigParser()
            config.read("config/proxy.ini")
            
            if 'Proxy' in config:
                proxy_config['enabled'] = config['Proxy'].getboolean('enabled', False)
                proxy_config['host'] = config['Proxy'].get('host')
                proxy_config['port'] = config['Proxy'].get('port')
                proxy_config['username'] = config['Proxy'].get('username')
                proxy_config['password'] = config['Proxy'].get('password')
                
                if proxy_config['enabled'] and proxy_config['host'] and proxy_config['port']:
                    print_color("Proxy settings loaded", "green")
                    return proxy_config
    except Exception as e:
        print_color(f"Error loading proxy settings: {str(e)}", "red")
    
    return proxy_config

def main():
    if len(sys.argv) < 2:
        print_color("Usage: python3 main.py <target_username>", "red")
        sys.exit(1)

    target = sys.argv[1]
    is_file = False
    is_json = False
    is_cli = True
    output_dir = "output"
    clear_cookies = False

    # Load proxy settings
    proxy_config = load_proxy_settings()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print_color(f"Output directory: {os.path.abspath(output_dir)}", "cyan")

    # Initialize Osintgram
    try:
        print_color("\nInitializing Osintgram...", "yellow")
        
        # Initialize with proxy settings if enabled
        if proxy_config['enabled']:
            print_color("Using proxy server...", "cyan")
            print_color(f"Proxy: {proxy_config['host']}:{proxy_config['port']}", "cyan")
            osint = Osintgram(
                target, 
                is_file, 
                is_json, 
                is_cli, 
                output_dir, 
                clear_cookies,
                proxy_host=proxy_config['host'],
                proxy_port=proxy_config['port'],
                proxy_username=proxy_config['username'],
                proxy_password=proxy_config['password']
            )
        else:
            osint = Osintgram(target, is_file, is_json, is_cli, output_dir, clear_cookies)
        
        # Set the initial target
        try:
            print_color(f"Setting target: {target}", "yellow")
            osint.setTarget(target)
            
            # Check if account exists and its privacy status
            exists, is_private = check_account_exists(osint, target)
            if exists is False:
                print_color("Error: Account does not exist or has been deleted", "red")
                sys.exit(1)
            elif exists is True and is_private:
                print_color("Warning: Account is private", "yellow")
                print_color("Some features might not work properly", "yellow")
            
            # Get initial user info to verify target
            user_info = get_user_info_safe(osint, target)
            if user_info:
                print_color("\nTarget Information:", "cyan")
                print_color(f"Username: {user_info.get('username', 'N/A')}", "white")
                print_color(f"Full Name: {user_info.get('full_name', 'N/A')}", "white")
                print_color(f"Posts: {user_info.get('media_count', 'N/A')}", "white")
                print_color(f"Followers: {user_info.get('follower_count', 'N/A')}", "white")
                print_color(f"Following: {user_info.get('following_count', 'N/A')}", "white")
                print_color(f"Private: {user_info.get('is_private', 'N/A')}", "white")
                print_color(f"Verified: {user_info.get('is_verified', 'N/A')}", "white")
            else:
                print_color("Warning: Could not fetch detailed user info", "yellow")
                print_color("Some features might not work properly", "yellow")
            
            print_color(f"\nTarget set to: {target}", "green")
        except Exception as e:
            print_color(f"Error setting initial target: {str(e)}", "red")
            print_color("Please check if the username exists and try again.", "yellow")
            sys.exit(1)

        # Print banner
        print_banner()
        print_color("\nType 'list' to see available commands", "cyan")
        print_color("Type 'help' for more information", "cyan")
        print_color("Type 'exit' or 'quit' to exit\n", "cyan")

    except Exception as e:
        print_color(f"Error initializing Osintgram: {str(e)}", "red")
        print_color("Please check your internet connection and try again.", "yellow")
        sys.exit(1)

    while True:
        try:
            print_color("\nRun a command: ", "yellow", end="")
            command = input().strip().lower()

            if command == "list":
                print_commands()
            elif command == "exit" or command == "quit":
                _quit()
            elif command == "target":
                print_color("Enter new target username: ", "yellow", end="")
                new_target = input().strip()
                try:
                    osint.setTarget(new_target)
                    
                    # Check if new account exists and its privacy status
                    exists, is_private = check_account_exists(osint, new_target)
                    if exists is False:
                        print_color("Error: Account does not exist or has been deleted", "red")
                        continue
                    elif exists is True and is_private:
                        print_color("Warning: Account is private", "yellow")
                        print_color("Some features might not work properly", "yellow")
                    
                    # Verify new target
                    user_info = get_user_info_safe(osint, new_target)
                    if user_info:
                        print_color("\nNew Target Information:", "cyan")
                        print_color(f"Username: {user_info.get('username', 'N/A')}", "white")
                        print_color(f"Full Name: {user_info.get('full_name', 'N/A')}", "white")
                        print_color(f"Posts: {user_info.get('media_count', 'N/A')}", "white")
                        print_color(f"Followers: {user_info.get('follower_count', 'N/A')}", "white")
                        print_color(f"Following: {user_info.get('following_count', 'N/A')}", "white")
                        print_color(f"Private: {user_info.get('is_private', 'N/A')}", "white")
                        print_color(f"Verified: {user_info.get('is_verified', 'N/A')}", "white")
                    else:
                        print_color("Warning: Could not fetch detailed user info", "yellow")
                        print_color("Some features might not work properly", "yellow")
                    
                    print_color(f"Target set to: {new_target}", "green")
                    target = new_target
                except Exception as e:
                    print_color(f"Error setting target: {str(e)}", "red")
                    print_color("Please check if the username exists and try again.", "yellow")
                    continue
            elif command == "file=y":
                osint.set_write_file(True)
                print_color("File output enabled", "green")
            elif command == "file=n":
                osint.set_write_file(False)
                print_color("File output disabled", "green")
            elif command == "json=y":
                osint.set_json_dump(True)
                print_color("JSON output enabled", "green")
            elif command == "json=n":
                osint.set_json_dump(False)
                print_color("JSON output disabled", "green")
            elif command == "cache":
                osint.clear_cache()
                print_color("Cache cleared", "green")
            elif command == "addrs":
                osint.get_addrs()
            elif command == "captions":
                osint.get_captions()
            elif command == "commentdata":
                osint.get_comment_data()
            elif command == "comments":
                osint.get_total_comments()
            elif command == "followers":
                osint.get_followers()
            elif command == "followings":
                osint.get_followings()
            elif command == "fwersemail":
                osint.get_fwersemail()
            elif command == "fwingsemail":
                osint.get_fwingsemail()
            elif command == "fwersnumber":
                osint.get_fwersnumber()
            elif command == "fwingsnumber":
                osint.get_fwingsnumber()
            elif command == "hashtags":
                osint.get_hashtags()
            elif command == "info":
                print_color("\nFetching user info...", "yellow")
                user_info = get_user_info_safe(osint, target)
                if user_info:
                    print_color("\nUser Information:", "cyan")
                    print_color(f"Username: {user_info.get('username', 'N/A')}", "white")
                    print_color(f"Full Name: {user_info.get('full_name', 'N/A')}", "white")
                    print_color(f"Biography: {user_info.get('biography', 'N/A')}", "white")
                    print_color(f"Followers: {user_info.get('follower_count', 'N/A')}", "white")
                    print_color(f"Following: {user_info.get('following_count', 'N/A')}", "white")
                    print_color(f"Posts: {user_info.get('media_count', 'N/A')}", "white")
                    print_color(f"Private: {user_info.get('is_private', 'N/A')}", "white")
                    print_color(f"Verified: {user_info.get('is_verified', 'N/A')}", "white")
                else:
                    exists, is_private = check_account_exists(osint, target)
                    if exists is False:
                        print_color("Account does not exist or has been deleted", "red")
                    elif exists is True and is_private:
                        print_color("Account is private", "red")
                    else:
                        print_color("Failed to fetch user information", "red")
                        print_color("Please try again later", "yellow")
            elif command == "likes":
                osint.get_likes()
            elif command == "mediatype":
                osint.get_media_type()
            elif command == "photodes":
                osint.get_photo_description()
            elif command == "photos":
                print_color(f"\nDownloading photos to: {os.path.abspath(output_dir)}/{target}_photos/", "yellow")
                osint.get_user_photo()
                print_color(f"Photos saved in: {os.path.abspath(output_dir)}/{target}_photos/", "green")
            elif command == "propic":
                print_color(f"\nDownloading profile picture to: {os.path.abspath(output_dir)}/{target}_propic.jpg", "yellow")
                osint.get_user_propic()
                print_color(f"Profile picture saved as: {os.path.abspath(output_dir)}/{target}_propic.jpg", "green")
            elif command == "stories":
                print_color(f"\nDownloading stories to: {os.path.abspath(output_dir)}/{target}_stories/", "yellow")
                osint.get_user_stories()
                print_color(f"Stories saved in: {os.path.abspath(output_dir)}/{target}_stories/", "green")
            elif command == "tagged":
                osint.get_people_tagged_by_user()
            elif command == "wcommented":
                osint.get_people_who_commented()
            elif command == "wtagged":
                osint.get_people_who_tagged()
            else:
                print_color("Unknown command. Type 'list' to see all available commands.", "red")

        except KeyboardInterrupt:
            print_color("\nExiting...", "yellow")
            break
        except Exception as e:
            print_color(f"Error: {str(e)}", "red")
            print_color("Please try again or check your internet connection.", "yellow")

if __name__ == "__main__":
    # Check for account configuration first
    check_accounts()
    main()
>>>>>>> 5473b8d (Secon commit)
