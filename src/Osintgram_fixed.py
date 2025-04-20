import datetime
import json
import sys
import urllib
import os
import codecs
from pathlib import Path
import time
import configparser
import requests
import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context

from geopy.geocoders import Nominatim
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ClientError,
    ClientLoginRequired,
    ClientThrottledError
)

from prettytable import PrettyTable

from src import printcolors as pc
from src.print_color import print_color
from src import config
from src.ai_analyzer import AIAnalyzer
from src.target_prioritizer import TargetPrioritizer
from src.ip_rotator import IPRotator


class Osintgram:
    api = None
    api2 = None
    geolocator = Nominatim(user_agent="http")
    user_id = None
    target_id = None
    is_private = True
    following = False
    target = ""
    writeFile = False
    jsonDump = False
    cli_mode = False
    output_dir = "output"
    current_account = None
    retry_count = 0
    MAX_RETRIES = 3
    target_prioritizer = None
    targets_data = {}  # Store data for multiple targets
    ip_rotator = IPRotator()
    proxy = None
    ai_analyzer = None  # Add AI analyzer attribute

    def __init__(self, target, is_file, is_json, is_cli, output_dir, clear_cookies):
        try:
            self.target = target
            self.writeFile = is_file
            self.jsonDump = is_json
            self.cli_mode = is_cli
            self.output_dir = output_dir
            self.retry_count = 0
            self.MAX_RETRIES = 3
            self.target_prioritizer = None
            self.targets_data = {}
            self.ip_rotator = IPRotator()
            self.proxy = None
            self.ai_analyzer = None

            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)

            # Load proxy configuration
            self._load_proxy_config()

            # Clear cookies if requested
            if clear_cookies:
                self.clear_cookies(clear_cookies)

            # Attempt login
            if not self.login_with_retry():
                raise Exception("Failed to login to Instagram")

            # Initialize AI analyzer
            self.ai_analyzer = AIAnalyzer()
            
            # Load AI configuration
            self._load_ai_config()

            print_color("Osintgram initialized successfully", "green")
        except Exception as e:
            print_color(f"Error initializing Osintgram: {str(e)}", "red")
            raise

    def setTarget(self, target):
        """
        Set the target user and initialize necessary data
        """
        try:
            self.target = target
            if not target:
                print_color("Target username cannot be empty", "red")
                return False
                
            # First get user info by username
            user = self.api.user_info_by_username(target)
            if not user:
                print_color(f"Could not find user {target}", "red")
                return False
                
            self.target_id = user.pk
            self.is_private = user.is_private
            self.following = self.check_following(user)
            
            # Create output directory
            if not self.output_dir:
                self.output_dir = "output"
            output_path = os.path.join(self.output_dir, str(self.target))
            os.makedirs(output_path, exist_ok=True)
            
            # Print target banner
            self.__printTargetBanner__(user)
            return True
            
        except Exception as e:
            print_color(f"Error setting target: {str(e)}", "red")
            return False

    def get_user_photo(self):
        if self.check_private_profile():
            return

        limit = -1
        if self.cli_mode:
            user_input = ""
        else:
            pc.printout("How many photos you want to download (default all): ", pc.YELLOW)
            user_input = input()
          
        try:
            if user_input == "":
                pc.printout("Downloading all photos available...\n")
            else:
                limit = int(user_input)
                pc.printout("Downloading " + user_input + " photos...\n")
        except ValueError:
            pc.printout("Wrong value entered\n", pc.RED)
            return

        os.makedirs(self.output_dir, exist_ok=True)
        data = []
        counter = 0

        try:
            result = self.api.user_feed(str(self.target_id))
            if not result or 'items' not in result:
                print_color("No photos found or error accessing user feed", "red")
                return
                
            data.extend(result.get('items', []))

            next_max_id = result.get('next_max_id')
            while next_max_id:
                results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
                data.extend(results.get('items', []))
                next_max_id = results.get('next_max_id')

            if not data:
                print_color("No photos found in user feed", "red")
                return

            for item in data:
                if counter == limit:
                    break
                    
                try:
                    if "image_versions2" in item:
                        counter += 1
                        url = item["image_versions2"]["candidates"][0]["url"]
                        photo_id = item["id"]
                        end = os.path.join(self.output_dir, f"{self.target}_{photo_id}.jpg")
                        
                        response = requests.get(url, stream=True)
                        if response.status_code == 200:
                            with open(end, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            sys.stdout.write(f"\rDownloaded {counter} photos")
                            sys.stdout.flush()
                        else:
                            print_color(f"\nFailed to download photo {photo_id}: HTTP {response.status_code}", "red")
                            
                    elif "carousel_media" in item:
                        carousel = item["carousel_media"]
                        for i in carousel:
                            if counter == limit:
                                break
                            counter += 1
                            url = i["image_versions2"]["candidates"][0]["url"]
                            photo_id = i["id"]
                            end = os.path.join(self.output_dir, f"{self.target}_{photo_id}.jpg")
                            
                            response = requests.get(url, stream=True)
                            if response.status_code == 200:
                                with open(end, 'wb') as f:
                                    for chunk in response.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                sys.stdout.write(f"\rDownloaded {counter} photos")
                                sys.stdout.flush()
                            else:
                                print_color(f"\nFailed to download carousel photo {photo_id}: HTTP {response.status_code}", "red")
                                
                except Exception as e:
                    print_color(f"\nError processing photo: {str(e)}", "red")
                    continue

            print_color(f"\nSuccessfully downloaded {counter} photos to {self.output_dir}", "green")

        except Exception as e:
            print_color(f"Error downloading photos: {str(e)}", "red")
            return

    def get_fwingsnumber(self):
        """Get phone numbers of users followed by target"""
        if self.check_private_profile():
            return
       
        print_color("Searching for phone numbers of users followed by target...\n", "yellow")

        try:
            # Get user's followings
            followings = self.api.user_following(self.target_id)
            if not followings:
                print_color("No followings found\n", "red")
                return
       
            results = []
            total = len(followings)
            processed = 0

            for user_id, user_info in followings.items():
                processed += 1
                sys.stdout.write(f"\rProcessing {processed}/{total} users")
                sys.stdout.flush()

                try:
                    # Get detailed user info which includes contact info
                    user_detail = self.api.user_info(user_id)
                    if user_detail.contact_phone_number:
                        results.append({
                            'id': user_id,
                            'username': user_info.username,
                            'full_name': user_info.full_name,
                            'phone': user_detail.contact_phone_number
                        })
                except Exception as e:
                    continue
        
            print("\n")

            if results:
                t = PrettyTable(['ID', 'Username', 'Full Name', 'Phone'])
                t.align["ID"] = "l"
                t.align["Username"] = "l"
                t.align["Full Name"] = "l"
                t.align["Phone"] = "l"

                for user in results:
                    t.add_row([str(user['id']), user['username'], user['full_name'], user['phone']])

                print(t)

                if self.writeFile:
                    file_name = os.path.join(self.output_dir, f"{self.target}_fwingsnumber.txt")
                    with open(file_name, "w") as f:
                        f.write(str(t))

                if self.jsonDump:
                    json_data = {'followings_phone_numbers': results}
                    json_file_name = os.path.join(self.output_dir, f"{self.target}_fwingsnumber.json")
                    with open(json_file_name, 'w') as f:
                        json.dump(json_data, f)
            else:
                print_color("No phone numbers found\n", "red")
        except Exception as e:
            print_color(f"Error getting phone numbers: {str(e)}\n", "red") 