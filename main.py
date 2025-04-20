#!/usr/bin/env python3

from src.Osintgram import Osintgram
import argparse
from src import printcolors as pc
from src import artwork
import sys
import signal
import os
import subprocess
import configparser


def signal_handler(sig, frame):
    pc.printout("\nGoodbye!\n", pc.RED)
    sys.exit(0)


def clear_screen():
    if os.name == 'nt':
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)


def print_commands():
    pc.printout("Available commands:\n", pc.YELLOW)
    pc.printout("- addrs\t\t")
    pc.printout("Get all registered addressed by target photos\n")
    pc.printout("- captions\t")
    pc.printout("Get target's photos captions\n")
    pc.printout("- comments\t")
    pc.printout("Get total comments of target's posts\n")
    pc.printout("- followers\t")
    pc.printout("Get target's followers\n")
    pc.printout("- followings\t")
    pc.printout("Get users followed by target\n")
    pc.printout("- fwersemail\t")
    pc.printout("Get email of target's followers\n")
    pc.printout("- fwingsemail\t")
    pc.printout("Get email of users followed by target\n")
    pc.printout("- fwersnumber\t")
    pc.printout("Get phone number of target's followers\n")
    pc.printout("- fwingsnumber\t")
    pc.printout("Get phone number of users followed by target\n")
    pc.printout("- hashtags\t")
    pc.printout("Get hashtags used by target\n")
    pc.printout("- info\t\t")
    pc.printout("Get target info\n")
    pc.printout("- likes\t\t")
    pc.printout("Get total likes of target's posts\n")
    pc.printout("- mediatype\t")
    pc.printout("Get target's posts type (photo or video)\n")
    pc.printout("- photodes\t")
    pc.printout("Get description of target's photos\n")
    pc.printout("- photos\t\t")
    pc.printout("Download target's photos in output folder\n")
    pc.printout("- propic\t\t")
    pc.printout("Download target's profile picture\n")
    pc.printout("- stories\t")
    pc.printout("Download target's stories\n")
    pc.printout("- tagged\t")
    pc.printout("Get list of users tagged by target\n")
    pc.printout("- target\t")
    pc.printout("Set new target\n")
    pc.printout("- wcommented\t")
    pc.printout("Get a list of users who commented target's photos\n")
    pc.printout("- wtagged\t")
    pc.printout("Get a list of users who tagged target\n")
    pc.printout("\n")
    pc.printout("Command line commands:\n", pc.YELLOW)
    pc.printout("- exit\t\t")
    pc.printout("Exit from Osintgram\n")
    pc.printout("- help\t\t")
    pc.printout("Show this help message\n")
    pc.printout("- clear\t\t")
    pc.printout("Clear the terminal screen\n")
    pc.printout("\n")


def main():
    parser = argparse.ArgumentParser(
        description='Osintgram is a OSINT tool on Instagram. It offers an interactive shell to perform analysis on Instagram account of any users by its nickname.')
    parser.add_argument(
        '-C',
        '--clear',
        help='Clear the cookie file',
        action='store_true')
    parser.add_argument(
        '-f',
        '--file',
        help='Save results in a file',
        action='store_true')
    parser.add_argument(
        '-j',
        '--json',
        help='Save results in a JSON file',
        action='store_true')
    parser.add_argument(
        '-c',
        '--command',
        help='Run in single command mode & execute provided command',
        action='store')
    parser.add_argument(
        '-o',
        '--output',
        help='Output directory for photos',
        action='store')

    args = parser.parse_args()

    # Create config dir if not exists
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Check if credentials.ini exists
    if not os.path.isfile('config/credentials.ini'):
        pc.printout("Error: The configuration file doesn't exist.\n", pc.RED)
        pc.printout("Please run: python3 setup_accounts.py\n", pc.YELLOW)
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read('config/credentials.ini')

    if not config.has_section('Account'):
        pc.printout(
            "Error: The configuration file is missing the Account section.\n",
            pc.RED)
        pc.printout("Please run: python3 setup_accounts.py\n", pc.YELLOW)
        sys.exit(1)

    if not config.has_option(
        'Account',
        'username') or not config.has_option(
        'Account',
            'password'):
        pc.printout(
            "Error: The configuration file is missing username or password.\n",
            pc.RED)
        pc.printout("Please run: python3 setup_accounts.py\n", pc.YELLOW)
        sys.exit(1)

    api = Osintgram(
        config['Account']['username'],
        config['Account']['password'],
        args.file,
        args.json,
        args.command,
        args.output)

    # Handle signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Clear cookies if requested
    if args.clear:
        api.clear_cookies()
        pc.printout("Cookies cleared!\n", pc.GREEN)
        sys.exit(0)

    # Print banner
    clear_screen()
    artwork.print_banner()
    pc.printout("Select a target Instagram account.\n", pc.YELLOW)

    while True:
        pc.printout("target:", pc.YELLOW)
        target = input().strip()

        if not target:
            pc.printout("Please enter a valid username.\n", pc.RED)
            continue

        if api.setTarget(target):
            break

    if args.command:
        api.executeCommand(args.command)
        sys.exit(0)

    while True:
        pc.printout("\nOsintgram > ", pc.YELLOW)
        cmd = input().strip()

        if not cmd:
            continue

        if cmd == "help":
            print_commands()
        elif cmd == "exit":
            pc.printout("Goodbye!\n", pc.RED)
            sys.exit(0)
        elif cmd == "clear":
            clear_screen()
        else:
            api.executeCommand(cmd)


if __name__ == "__main__":
    main()
