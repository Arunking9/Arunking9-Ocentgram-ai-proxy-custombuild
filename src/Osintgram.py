import datetime
import json
import sys
import urllib
import os
import codecs
<<<<<<< HEAD
import time
import random
from pathlib import Path
from typing import List, Tuple, Optional

import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from geopy.geocoders import Nominatim
from instagram_private_api import Client as AppClient
from instagram_private_api import ClientCookieExpiredError, ClientLoginRequiredError, ClientError, ClientThrottledError
=======
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
>>>>>>> 5473b8d (Secon commit)

from prettytable import PrettyTable

from src import printcolors as pc
<<<<<<< HEAD
from src import config

class AccountManager:
    def __init__(self):
        self.accounts = config.get_accounts()
        self.settings = config.get_settings()
        self.current_account_index = 0
        self.rate_limited_accounts = set()
        self.last_switch_time = 0
        
    def get_next_account(self) -> Optional[Tuple[str, str]]:
        """Get the next available account, considering rate limits and switch delay."""
        current_time = time.time()
        
        # Check if we need to wait before switching
        if current_time - self.last_switch_time < self.settings["switch_delay"]:
            return None
            
        # Try to find an account that's not rate limited
        for _ in range(len(self.accounts)):
            if self.current_account_index not in self.rate_limited_accounts:
                account = self.accounts[self.current_account_index]
                self.current_account_index = (self.current_account_index + 1) % len(self.accounts)
                self.last_switch_time = current_time
                return account
            self.current_account_index = (self.current_account_index + 1) % len(self.accounts)
            
        # If all accounts are rate limited, clear the rate limited set and try again
        if len(self.rate_limited_accounts) == len(self.accounts):
            self.rate_limited_accounts.clear()
            return self.get_next_account()
            
        return None
        
    def mark_account_rate_limited(self, account_index: int):
        """Mark an account as rate limited."""
        self.rate_limited_accounts.add(account_index)
        
    def get_current_account_index(self) -> int:
        """Get the current account index."""
        return (self.current_account_index - 1) % len(self.accounts)
=======
from src.print_color import print_color
from src import config
from src.ai_analyzer import AIAnalyzer
from src.target_prioritizer import TargetPrioritizer
from src.ip_rotator import IPRotator

>>>>>>> 5473b8d (Secon commit)

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
<<<<<<< HEAD
    account_manager = None

    def __init__(self, target, is_file, is_json, is_cli, output_dir, clear_cookies):
        self.output_dir = output_dir or self.output_dir        
        self.account_manager = AccountManager()
        self.clear_cookies(clear_cookies)
        self.cli_mode = is_cli
        if not is_cli:
            print("\nAttempt to login...")
        self.login_with_account_switching()
        self.setTarget(target)
        self.writeFile = is_file
        self.jsonDump = is_json

    def login_with_account_switching(self):
        """Attempt to login with account switching on failure."""
        while True:
            account = self.account_manager.get_next_account()
            if not account:
                pc.printout("All accounts are rate limited. Waiting before retrying...\n", pc.YELLOW)
                time.sleep(self.account_manager.settings["switch_delay"])
                continue
                
            try:
                self.login(account[0], account[1])
                break
            except (ClientError, ClientLoginRequiredError) as e:
                pc.printout(f"Login failed for account {account[0]}: {str(e)}\n", pc.RED)
                self.account_manager.mark_account_rate_limited(self.account_manager.get_current_account_index())
                continue

    def handle_rate_limit(self):
        """Handle rate limiting by switching accounts."""
        current_account_index = self.account_manager.get_current_account_index()
        self.account_manager.mark_account_rate_limited(current_account_index)
        pc.printout(f"Account {self.api.username} rate limited. Switching accounts...\n", pc.YELLOW)
        self.login_with_account_switching()
=======
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

    def _load_proxy_config(self):
        """Load proxy configuration from ip_config.ini"""
        config = configparser.ConfigParser()
        config_path = os.path.join('config', 'ip_config.ini')
        if os.path.exists(config_path):
            config.read(config_path)
            if config.getboolean('IP', 'enabled', fallback=False):
                if config.getboolean('IP', 'use_tor', fallback=False):
                    self.proxy = config.get('IP', 'tor_proxy', fallback='socks5h://127.0.0.1:9050')
                    print_color(f"Using Tor proxy: {self.proxy}", "green")

    def _load_ai_config(self):
        """Load AI configuration from ai_config.ini"""
        config = configparser.ConfigParser()
        config_path = os.path.join('config', 'ai_config.ini')
        if os.path.exists(config_path):
            config.read(config_path)
            if config.getboolean('AI', 'enabled', fallback=False):
                self.ai_analyzer.enabled = True
                self.ai_analyzer.api_key = config.get('AI', 'api_key', fallback='')
                self.ai_analyzer.model = config.get('AI', 'model', fallback='gpt-3.5-turbo')
                self.ai_analyzer.max_tokens = config.getint('AI', 'max_tokens', fallback=1000)
                print_color("AI features enabled", "green")
            else:
                print_color("AI features disabled", "yellow")
        else:
            print_color("AI configuration not found. AI features disabled.", "yellow")
>>>>>>> 5473b8d (Secon commit)

    def clear_cookies(self,clear_cookies):
        if clear_cookies:
            self.clear_cache()

    def setTarget(self, target):
<<<<<<< HEAD
        self.target = target
        user = self.get_user(target)
        self.target_id = user['id']
        self.is_private = user['is_private']
        self.following = self.check_following()
        self.__printTargetBanner__()
        self.output_dir = self.output_dir + "/" + str(self.target)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def __get_feed__(self):
        data = []
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                result = self.api.user_feed(str(self.target_id))
                data.extend(result.get('items', []))

                next_max_id = result.get('next_max_id')
                while next_max_id:
                    results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
                    data.extend(results.get('items', []))
                    next_max_id = results.get('next_max_id')

                return data
            except (ClientError, ClientThrottledError) as e:
                retry_count += 1
                if retry_count < max_retries:
                    self.handle_rate_limit()
                else:
                    raise e

    def __get_comments__(self, media_id):
        comments = []
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                result = self.api.media_comments(str(media_id))
                comments.extend(result.get('comments', []))

                next_max_id = result.get('next_max_id')
                while next_max_id:
                    results = self.api.media_comments(str(media_id), max_id=next_max_id)
                    comments.extend(results.get('comments', []))
                    next_max_id = results.get('next_max_id')

                return comments
            except (ClientError, ClientThrottledError) as e:
                retry_count += 1
                if retry_count < max_retries:
                    self.handle_rate_limit()
                else:
                    raise e

    def __printTargetBanner__(self):
        pc.printout("\nLogged as ", pc.GREEN)
        pc.printout(self.api.username, pc.CYAN)
        pc.printout(". Target: ", pc.GREEN)
        pc.printout(str(self.target), pc.CYAN)
        pc.printout(" [" + str(self.target_id) + "]")
        if self.is_private:
            pc.printout(" [PRIVATE PROFILE]", pc.BLUE)
        if self.following:
            pc.printout(" [FOLLOWING]", pc.GREEN)
        else:
            pc.printout(" [NOT FOLLOWING]", pc.RED)

        print('\n')
=======
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

    def __get_feed__(self):
        """
        Get user's media feed
        """
        try:
            if not self.target_id:
                print_color("Target not set. Please set a target first.", "red")
                return []
                
            # Get user's media using user_medias
            medias = self.api.user_medias(self.target_id)
            if not medias:
                print_color(f"No media found for user {self.target}", "red")
                return []
                
            # Convert medias to the expected format
            data = []
            for media in medias:
                media_dict = {
                    'id': media.id,
                    'caption': {'text': media.caption_text} if media.caption_text else None,
                    'taken_at': media.taken_at.timestamp(),
                    'like_count': media.like_count,
                    'comment_count': media.comment_count,
                    'media_type': media.media_type,
                    'usertags': media.usertags if hasattr(media, 'usertags') else None
                }
                data.append(media_dict)
                
            return data
            
        except Exception as e:
            print_color(f"Error getting feed: {str(e)}", "red")
            return []

    def __get_comments__(self, media_id):
        comments = []

        result = self.api.media_comments(str(media_id))
        comments.extend(result.get('comments', []))

        next_max_id = result.get('next_max_id')
        while next_max_id:
            results = self.api.media_comments(str(media_id), max_id=next_max_id)
            comments.extend(results.get('comments', []))
            next_max_id = results.get('next_max_id')

        return comments

    def __printTargetBanner__(self, user_info):
        pc.printout("\nLogged as ", pc.GREEN)
        pc.printout(self.api.username, pc.CYAN)
        pc.printout(" (" + str(self.api.user_id) + ") ")
        pc.printout("target: ", pc.GREEN)
        pc.printout(str(self.target), pc.CYAN)
        pc.printout(" (private: " + str(self.is_private) + ")")
        pc.printout(" [" + str(user_info.media_count) + " posts, " + str(user_info.follower_count) + " followers, " + str(user_info.following_count) + " following]\n")
>>>>>>> 5473b8d (Secon commit)

    def change_target(self):
        pc.printout("Insert new target username: ", pc.YELLOW)
        line = input()
        self.setTarget(line)
        return

    def get_addrs(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target localizations...\n")

        data = self.__get_feed__()

        locations = {}

        for post in data:
            if 'location' in post and post['location'] is not None:
                if 'lat' in post['location'] and 'lng' in post['location']:
                    lat = post['location']['lat']
                    lng = post['location']['lng']
                    locations[str(lat) + ', ' + str(lng)] = post.get('taken_at')

        address = {}
        for k, v in locations.items():
            details = self.geolocator.reverse(k)
            unix_timestamp = datetime.datetime.fromtimestamp(v)
            address[details.address] = unix_timestamp.strftime('%Y-%m-%d %H:%M:%S')

        sort_addresses = sorted(address.items(), key=lambda p: p[1], reverse=True)

        if len(sort_addresses) > 0:
            t = PrettyTable()

            t.field_names = ['Post', 'Address', 'time']
            t.align["Post"] = "l"
            t.align["Address"] = "l"
            t.align["Time"] = "l"
            pc.printout("\nWoohoo! We found " + str(len(sort_addresses)) + " addresses\n", pc.GREEN)

            i = 1

            json_data = {}
            addrs_list = []

            for address, time in sort_addresses:
                t.add_row([str(i), address, time])

                if self.jsonDump:
                    addr = {
                        'address': address,
                        'time': time
                    }
                    addrs_list.append(addr)

                i = i + 1

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_addrs.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['address'] = addrs_list
                json_file_name = self.output_dir + "/" + self.target + "_addrs.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_captions(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target captions...\n")

        captions = []

        data = self.__get_feed__()
        counter = 0

        try:
            for item in data:
                if "caption" in item:
                    if item["caption"] is not None:
                        text = item["caption"]["text"]
                        captions.append(text)
                        counter = counter + 1
                        sys.stdout.write("\rFound %i" % counter)
                        sys.stdout.flush()

        except AttributeError:
            pass

        except KeyError:
            pass

        json_data = {}

        if counter > 0:
            pc.printout("\nWoohoo! We found " + str(counter) + " captions\n", pc.GREEN)

            file = None

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_captions.txt"
                file = open(file_name, "w")

            for s in captions:
                print(s + "\n")

                if self.writeFile:
                    file.write(s + "\n")

            if self.jsonDump:
                json_data['captions'] = captions
                json_file_name = self.output_dir + "/" + self.target + "_followings.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            if file is not None:
                file.close()

        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

        return

    def get_total_comments(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target total comments...\n")

        comments_counter = 0
        posts = 0

        data = self.__get_feed__()

        for post in data:
            comments_counter += post['comment_count']
            posts += 1

        if self.writeFile:
            file_name = self.output_dir + "/" + self.target + "_comments.txt"
            file = open(file_name, "w")
            file.write(str(comments_counter) + " comments in " + str(posts) + " posts\n")
            file.close()

        if self.jsonDump:
            json_data = {
                'comment_counter': comments_counter,
                'posts': posts
            }
            json_file_name = self.output_dir + "/" + self.target + "_comments.json"
            with open(json_file_name, 'w') as f:
                json.dump(json_data, f)

        pc.printout(str(comments_counter), pc.MAGENTA)
        pc.printout(" comments in " + str(posts) + " posts\n")

    def get_comment_data(self):
        if self.check_private_profile():
            return

        pc.printout("Retrieving all comments, this may take a moment...\n")
        data = self.__get_feed__()
        
        _comments = []
        t = PrettyTable(['POST ID', 'ID', 'Username', 'Comment'])
        t.align["POST ID"] = "l"
        t.align["ID"] = "l"
        t.align["Username"] = "l"
        t.align["Comment"] = "l"

        for post in data:
            post_id = post.get('id')
            comments = self.api.media_n_comments(post_id)
            for comment in comments:
                t.add_row([post_id, comment.get('user_id'), comment.get('user').get('username'), comment.get('text')])
                comment = {
                        "post_id": post_id,
                        "user_id":comment.get('user_id'), 
                        "username": comment.get('user').get('username'),
                        "comment": comment.get('text')
                    }
                _comments.append(comment)
        
        print(t)
        if self.writeFile:
            file_name = self.output_dir + "/" + self.target + "_comment_data.txt"
            with open(file_name, 'w') as f:
                f.write(str(t))
                f.close()
        
        if self.jsonDump:
            file_name_json = self.output_dir + "/" + self.target + "_comment_data.json"
            with open(file_name_json, 'w') as f:
                f.write("{ \"Comments\":[ \n")
                f.write('\n'.join(json.dumps(comment) for comment in _comments) + ',\n')
                f.write("]} ")


    def get_followers(self):
<<<<<<< HEAD
=======
        """Get target followers with AI analysis"""
        followers = self._get_followers_impl()
        if followers:
            ai_analysis = self.ai_analyzer.analyze_followers(followers)
            if self.ai_analyzer.enabled:
                pc.printout("\nAI Analysis of Followers:\n", pc.CYAN)
                print(ai_analysis)
        return followers

    def _get_followers_impl(self):
>>>>>>> 5473b8d (Secon commit)
        if self.check_private_profile():
            return

        pc.printout("Searching for target followers...\n")

        _followers = []
        followers = []


<<<<<<< HEAD
        rank_token = AppClient.generate_uuid()
=======
        rank_token = Client.generate_uuid()
>>>>>>> 5473b8d (Secon commit)
        data = self.api.user_followers(str(self.target_id), rank_token=rank_token)

        _followers.extend(data.get('users', []))

        next_max_id = data.get('next_max_id')
        while next_max_id:
            sys.stdout.write("\rCatched %i followers" % len(_followers))
            sys.stdout.flush()
            results = self.api.user_followers(str(self.target_id), rank_token=rank_token, max_id=next_max_id)
            _followers.extend(results.get('users', []))
            next_max_id = results.get('next_max_id')

        print("\n")
            
        for user in _followers:
            u = {
                'id': user['pk'],
                'username': user['username'],
                'full_name': user['full_name']
            }
            followers.append(u)

        t = PrettyTable(['ID', 'Username', 'Full Name'])
        t.align["ID"] = "l"
        t.align["Username"] = "l"
        t.align["Full Name"] = "l"

        json_data = {}
        followings_list = []

        for node in followers:
            t.add_row([str(node['id']), node['username'], node['full_name']])

            if self.jsonDump:
                follow = {
                    'id': node['id'],
                    'username': node['username'],
                    'full_name': node['full_name']
                }
                followings_list.append(follow)

        if self.writeFile:
            file_name = self.output_dir + "/" + self.target + "_followers.txt"
            file = open(file_name, "w")
            file.write(str(t))
            file.close()

        if self.jsonDump:
            json_data['followers'] = followers
            json_file_name = self.output_dir + "/" + self.target + "_followers.json"
            with open(json_file_name, 'w') as f:
                json.dump(json_data, f)

        print(t)

    def get_followings(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target followings...\n")

        _followings = []
        followings = []

<<<<<<< HEAD
        rank_token = AppClient.generate_uuid()
=======
        rank_token = Client.generate_uuid()
>>>>>>> 5473b8d (Secon commit)
        data = self.api.user_following(str(self.target_id), rank_token=rank_token)

        _followings.extend(data.get('users', []))

        next_max_id = data.get('next_max_id')
        while next_max_id:
            sys.stdout.write("\rCatched %i followings" % len(_followings))
            sys.stdout.flush()
            results = self.api.user_following(str(self.target_id), rank_token=rank_token, max_id=next_max_id)
            _followings.extend(results.get('users', []))
            next_max_id = results.get('next_max_id')

        print("\n")

        for user in _followings:
            u = {
                'id': user['pk'],
                'username': user['username'],
                'full_name': user['full_name']
            }
            followings.append(u)

        t = PrettyTable(['ID', 'Username', 'Full Name'])
        t.align["ID"] = "l"
        t.align["Username"] = "l"
        t.align["Full Name"] = "l"

        json_data = {}
        followings_list = []

        for node in followings:
            t.add_row([str(node['id']), node['username'], node['full_name']])

            if self.jsonDump:
                follow = {
                    'id': node['id'],
                    'username': node['username'],
                    'full_name': node['full_name']
                }
                followings_list.append(follow)

        if self.writeFile:
            file_name = self.output_dir + "/" + self.target + "_followings.txt"
            file = open(file_name, "w")
            file.write(str(t))
            file.close()

        if self.jsonDump:
            json_data['followings'] = followings_list
            json_file_name = self.output_dir + "/" + self.target + "_followings.json"
            with open(json_file_name, 'w') as f:
                json.dump(json_data, f)

        print(t)

    def get_hashtags(self):
<<<<<<< HEAD
        if self.check_private_profile():
            return

        pc.printout("Searching for target hashtags...\n")

        hashtags = []
        counter = 1
        texts = []

        data = self.api.user_feed(str(self.target_id))
        texts.extend(data.get('items', []))

        next_max_id = data.get('next_max_id')
        while next_max_id:
            results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
            texts.extend(results.get('items', []))
            next_max_id = results.get('next_max_id')

        for post in texts:
            if post['caption'] is not None:
                caption = post['caption']['text']
                for s in caption.split():
                    if s.startswith('#'):
                        hashtags.append(s.encode('UTF-8'))
                        counter += 1

        if len(hashtags) > 0:
            hashtag_counter = {}

            for i in hashtags:
                if i in hashtag_counter:
                    hashtag_counter[i] += 1
                else:
                    hashtag_counter[i] = 1

            ssort = sorted(hashtag_counter.items(), key=lambda value: value[1], reverse=True)

            file = None
            json_data = {}
            hashtags_list = []

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_hashtags.txt"
                file = open(file_name, "w")

            for k, v in ssort:
                hashtag = str(k.decode('utf-8'))
                print(str(v) + ". " + hashtag)
                if self.writeFile:
                    file.write(str(v) + ". " + hashtag + "\n")
                if self.jsonDump:
                    hashtags_list.append(hashtag)

            if file is not None:
                file.close()

            if self.jsonDump:
                json_data['hashtags'] = hashtags_list
                json_file_name = self.output_dir + "/" + self.target + "_hashtags.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_user_info(self):
        try:
            endpoint = 'users/{user_id!s}/full_detail_info/'.format(**{'user_id': self.target_id})
            content = self.api._call_api(endpoint)
           
            data = content['user_detail']['user']

            pc.printout("[ID] ", pc.GREEN)
            pc.printout(str(data['pk']) + '\n')
            pc.printout("[FULL NAME] ", pc.RED)
            pc.printout(str(data['full_name']) + '\n')
            pc.printout("[BIOGRAPHY] ", pc.CYAN)
            pc.printout(str(data['biography']) + '\n')
            pc.printout("[FOLLOWED] ", pc.BLUE)
            pc.printout(str(data['follower_count']) + '\n')
            pc.printout("[FOLLOW] ", pc.GREEN)
            pc.printout(str(data['following_count']) + '\n')
            pc.printout("[BUSINESS ACCOUNT] ", pc.RED)
            pc.printout(str(data['is_business']) + '\n')
            if data['is_business']:
                if not data['can_hide_category']:
                    pc.printout("[BUSINESS CATEGORY] ")
                    pc.printout(str(data['category']) + '\n')
            pc.printout("[VERIFIED ACCOUNT] ", pc.CYAN)
            pc.printout(str(data['is_verified']) + '\n')
            if 'public_email' in data and data['public_email']:
                pc.printout("[EMAIL] ", pc.BLUE)
                pc.printout(str(data['public_email']) + '\n')
            pc.printout("[HD PROFILE PIC] ", pc.GREEN)
            pc.printout(str(data['hd_profile_pic_url_info']['url']) + '\n')
            if 'fb_page_call_to_action_id' in data and data['fb_page_call_to_action_id']: 
                pc.printout("[FB PAGE] ", pc.RED)
                pc.printout(str(data['connected_fb_page']) + '\n')
            if 'whatsapp_number' in data and data['whatsapp_number']:
                pc.printout("[WHATSAPP NUMBER] ", pc.GREEN)
                pc.printout(str(data['whatsapp_number']) + '\n')
            if 'city_name' in data and data['city_name']:
                pc.printout("[CITY] ", pc.YELLOW)
                pc.printout(str(data['city_name']) + '\n')
            if 'address_street' in data and data['address_street']:
                pc.printout("[ADDRESS STREET] ", pc.RED)
                pc.printout(str(data['address_street']) + '\n')
            if 'contact_phone_number' in data and data['contact_phone_number']:
                pc.printout("[CONTACT PHONE NUMBER] ", pc.CYAN)
                pc.printout(str(data['contact_phone_number']) + '\n')

            if self.jsonDump:
                user = {
                    'id': data['pk'],
                    'full_name': data['full_name'],
                    'biography': data['biography'],
                    'edge_followed_by': data['follower_count'],
                    'edge_follow': data['following_count'],
                    'is_business_account': data['is_business'],
                    'is_verified': data['is_verified'],
                    'profile_pic_url_hd': data['hd_profile_pic_url_info']['url']
                }
                if 'public_email' in data and data['public_email']:
                    user['email'] = data['public_email']
                if 'fb_page_call_to_action_id' in data and data['fb_page_call_to_action_id']: 
                    user['connected_fb_page'] = data['fb_page_call_to_action_id']
                if 'whatsapp_number' in data and data['whatsapp_number']:
                    user['whatsapp_number'] = data['whatsapp_number']
                if 'city_name' in data and data['city_name']:
                    user['city_name'] = data['city_name']
                if 'address_street' in data and data['address_street']:
                    user['address_street'] = data['address_street']
                if 'contact_phone_number' in data and data['contact_phone_number']:
                    user['contact_phone_number'] = data['contact_phone_number']

                json_file_name = self.output_dir + "/" + self.target + "_info.json"
                with open(json_file_name, 'w') as f:
                    json.dump(user, f)

        except ClientError as e:
            print(e)
            pc.printout("Oops... " + str(self.target) + " non exist, please enter a valid username.", pc.RED)
            pc.printout("\n")
            exit(2)

    def get_total_likes(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target total likes...\n")

        like_counter = 0
        posts = 0

        data = self.__get_feed__()

        for post in data:
            like_counter += post['like_count']
            posts += 1

        if self.writeFile:
            file_name = self.output_dir + "/" + self.target + "_likes.txt"
            file = open(file_name, "w")
            file.write(str(like_counter) + " likes in " + str(like_counter) + " posts\n")
            file.close()

        if self.jsonDump:
            json_data = {
                'like_counter': like_counter,
                'posts': like_counter
            }
            json_file_name = self.output_dir + "/" + self.target + "_likes.json"
            with open(json_file_name, 'w') as f:
                json.dump(json_data, f)

        pc.printout(str(like_counter), pc.MAGENTA)
        pc.printout(" likes in " + str(posts) + " posts\n")
=======
        """Get hashtags used by target"""
        if self.check_private_profile():
            return

        try:
            print_color("Fetching media to extract hashtags...", "yellow")
            media = self.api.user_medias(self.target_id)
            
            if not media:
                print_color("No media found for this user", "yellow")
                return

            hashtags = set()
            total_media = len(media)
            processed = 0

            for item in media:
                processed += 1
                sys.stdout.write(f"\rProcessing media {processed}/{total_media}")
                sys.stdout.flush()

                if item.caption_text:
                    # Extract hashtags from caption
                    caption_hashtags = re.findall(r'#(\w+)', item.caption_text)
                    hashtags.update(caption_hashtags)

            print("\n")  # New line after progress

            if hashtags:
                # Create a PrettyTable for the hashtags
                t = PrettyTable(['Hashtag'])
                t.align["Hashtag"] = "l"
                
                for hashtag in sorted(hashtags):
                    t.add_row([hashtag])

                print("\nFound hashtags:")
                print(t)

                if self.writeFile:
                    file_name = os.path.join(self.output_dir, f"{self.target}_hashtags.txt")
                    with open(file_name, "w") as f:
                        f.write(str(t))
                    print_color(f"\nHashtags saved to {file_name}", "green")

                if self.jsonDump:
                    json_data = {'hashtags': sorted(list(hashtags))}
                    json_file_name = os.path.join(self.output_dir, f"{self.target}_hashtags.json")
                    with open(json_file_name, 'w') as f:
                        json.dump(json_data, f, indent=4)
                    print_color(f"JSON data saved to {json_file_name}", "green")
            else:
                print_color("No hashtags found in user's media", "yellow")

        except Exception as e:
            print_color(f"Error getting hashtags: {str(e)}", "red")

    def get_user_info(self):
        """Get target's basic information"""
        if self.check_private_profile():
            return

        try:
            print_color("Fetching user information...", "yellow")
            user_info = self.api.user_info_by_username(self.target)
            
            if not user_info:
                print_color("Error: Could not fetch user information", "red")
                return

            # Create a PrettyTable for better formatting
            t = PrettyTable(['Field', 'Value'])
            t.align["Field"] = "l"
            t.align["Value"] = "l"

            # Add user information to the table
            t.add_row(['ID', str(user_info.pk)])
            t.add_row(['Username', user_info.username])
            t.add_row(['Full Name', user_info.full_name])
            t.add_row(['Biography', user_info.biography])
            t.add_row(['Profile Picture URL', user_info.profile_pic_url])
            t.add_row(['External URL', user_info.external_url])
            t.add_row(['Number of Posts', str(user_info.media_count)])
            t.add_row(['Followers', str(user_info.follower_count)])
            t.add_row(['Following', str(user_info.following_count)])
            t.add_row(['Is Private', str(user_info.is_private)])
            t.add_row(['Is Verified', str(user_info.is_verified)])

            print("\nTarget user info:")
            print(t)

            if self.writeFile:
                file_name = os.path.join(self.output_dir, f"{self.target}_info.txt")
                with open(file_name, "w") as f:
                    f.write(str(t))
                print_color(f"\nInformation saved to {file_name}", "green")

            if self.jsonDump:
                json_data = {
                    'id': str(user_info.pk),
                    'username': user_info.username,
                    'full_name': user_info.full_name,
                    'biography': user_info.biography,
                    'profile_pic_url': user_info.profile_pic_url,
                    'external_url': user_info.external_url,
                    'media_count': user_info.media_count,
                    'follower_count': user_info.follower_count,
                    'following_count': user_info.following_count,
                    'is_private': user_info.is_private,
                    'is_verified': user_info.is_verified
                }
                json_file_name = os.path.join(self.output_dir, f"{self.target}_info.json")
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f, indent=4)
                print_color(f"JSON data saved to {json_file_name}", "green")

        except Exception as e:
            print_color(f"Error getting user info: {str(e)}", "red")

    def get_likes(self):
        """Get total likes of target's posts"""
        if self.check_private_profile():
            return

        print_color("Getting total likes...\n", "yellow")

        try:
            # Get user's media
            medias = self.api.user_medias(self.target_id)
            if not medias:
                print_color("No posts found\n", "red")
                return

            total_likes = 0
            for media in medias:
                total_likes += media.like_count

            print_color(f"\nTotal likes: {total_likes}\n", "green")

            if self.writeFile:
                file_name = os.path.join(self.output_dir, f"{self.target}_total_likes.txt")
                with open(file_name, "w") as f:
                    f.write(f"Total likes: {total_likes}")

            if self.jsonDump:
                json_data = {'total_likes': total_likes}
                json_file_name = os.path.join(self.output_dir, f"{self.target}_total_likes.json")
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

        except Exception as e:
            print_color(f"Error getting total likes: {str(e)}\n", "red")
>>>>>>> 5473b8d (Secon commit)

    def get_media_type(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target captions...\n")

        counter = 0
        photo_counter = 0
        video_counter = 0

        data = self.__get_feed__()

        for post in data:
            if "media_type" in post:
                if post["media_type"] == 1:
                    photo_counter = photo_counter + 1
                elif post["media_type"] == 2:
                    video_counter = video_counter + 1
                counter = counter + 1
                sys.stdout.write("\rChecked %i" % counter)
                sys.stdout.flush()

        sys.stdout.write(" posts")
        sys.stdout.flush()

        if counter > 0:

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_mediatype.txt"
                file = open(file_name, "w")
                file.write(str(photo_counter) + " photos and " + str(video_counter) + " video posted by target\n")
                file.close()

            pc.printout("\nWoohoo! We found " + str(photo_counter) + " photos and " + str(video_counter) +
                        " video posted by target\n", pc.GREEN)

            if self.jsonDump:
                json_data = {
                    "photos": photo_counter,
                    "videos": video_counter
                }
                json_file_name = self.output_dir + "/" + self.target + "_mediatype.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_people_who_commented(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for users who commented...\n")

        data = self.__get_feed__()
        users = []

        for post in data:
            comments = self.__get_comments__(post['id'])
            for comment in comments:
                if not any(u['id'] == comment['user']['pk'] for u in users):
                    user = {
                        'id': comment['user']['pk'],
                        'username': comment['user']['username'],
                        'full_name': comment['user']['full_name'],
                        'counter': 1
                    }
                    users.append(user)
                else:
                    for user in users:
                        if user['id'] == comment['user']['pk']:
                            user['counter'] += 1
                            break

        if len(users) > 0:
            ssort = sorted(users, key=lambda value: value['counter'], reverse=True)

            json_data = {}

            t = PrettyTable()

            t.field_names = ['Comments', 'ID', 'Username', 'Full Name']
            t.align["Comments"] = "l"
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"

            for u in ssort:
                t.add_row([str(u['counter']), u['id'], u['username'], u['full_name']])

            print(t)

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_users_who_commented.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['users_who_commented'] = ssort
                json_file_name = self.output_dir + "/" + self.target + "_users_who_commented.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_people_who_tagged(self):
<<<<<<< HEAD
        if self.check_private_profile():
            return

        pc.printout("Searching for users who tagged target...\n")

        posts = []

        result = self.api.usertag_feed(self.target_id)
        posts.extend(result.get('items', []))

        next_max_id = result.get('next_max_id')
        while next_max_id:
            results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
            posts.extend(results.get('items', []))
            next_max_id = results.get('next_max_id')

        if len(posts) > 0:
            pc.printout("\nWoohoo! We found " + str(len(posts)) + " photos\n", pc.GREEN)

            users = []

            for post in posts:
                if not any(u['id'] == post['user']['pk'] for u in users):
                    user = {
                        'id': post['user']['pk'],
                        'username': post['user']['username'],
                        'full_name': post['user']['full_name'],
                        'counter': 1
                    }
                    users.append(user)
                else:
                    for user in users:
                        if user['id'] == post['user']['pk']:
                            user['counter'] += 1
                            break

            ssort = sorted(users, key=lambda value: value['counter'], reverse=True)

            json_data = {}

            t = PrettyTable()

            t.field_names = ['Photos', 'ID', 'Username', 'Full Name']
            t.align["Photos"] = "l"
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"

            for u in ssort:
                t.add_row([str(u['counter']), u['id'], u['username'], u['full_name']])

            print(t)

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_users_who_tagged.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['users_who_tagged'] = ssort
                json_file_name = self.output_dir + "/" + self.target + "_users_who_tagged.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)
=======
        """Get list of users who tagged the target"""
        if self.check_private_profile():
            return

        print_color("Searching for users who tagged target...\n", "yellow")

        try:
            # Get user's media where they are tagged
            medias = self.api.usertag_medias(self.target_id)
            if not medias:
                print_color("No users found who tagged the target\n", "red")
                return

            users = []
            for media in medias:
                user = media.user
                if not any(u['id'] == user.pk for u in users):
                    users.append({
                        'id': user.pk,
                        'username': user.username,
                        'full_name': user.full_name,
                        'counter': 1
                    })
                else:
                    for u in users:
                        if u['id'] == user.pk:
                            u['counter'] += 1
                            break

            if users:
                # Sort by number of tags
                users.sort(key=lambda x: x['counter'], reverse=True)

                t = PrettyTable(['Photos', 'ID', 'Username', 'Full Name'])
                t.align["Photos"] = "l"
                t.align["ID"] = "l"
                t.align["Username"] = "l"
                t.align["Full Name"] = "l"

                for user in users:
                    t.add_row([str(user['counter']), str(user['id']), user['username'], user['full_name']])

                print(t)

                if self.writeFile:
                    file_name = os.path.join(self.output_dir, f"{self.target}_users_who_tagged.txt")
                    with open(file_name, "w") as f:
                        f.write(str(t))

                if self.jsonDump:
                    json_data = {'users_who_tagged': users}
                    json_file_name = os.path.join(self.output_dir, f"{self.target}_users_who_tagged.json")
                    with open(json_file_name, 'w') as f:
                        json.dump(json_data, f)
            else:
                print_color("No users found who tagged the target\n", "red")

        except Exception as e:
            print_color(f"Error getting users who tagged target: {str(e)}\n", "red")
>>>>>>> 5473b8d (Secon commit)

    def get_photo_description(self):
        if self.check_private_profile():
            return

<<<<<<< HEAD
        content = requests.get("https://www.instagram.com/" + str(self.target) + "/?__a=1")
        data = content.json()

        dd = data['graphql']['user']['edge_owner_to_timeline_media']['edges']

        if len(dd) > 0:
            pc.printout("\nWoohoo! We found " + str(len(dd)) + " descriptions\n", pc.GREEN)

            count = 1

            t = PrettyTable(['Photo', 'Description'])
            t.align["Photo"] = "l"
            t.align["Description"] = "l"

            json_data = {}
            descriptions_list = []

            for i in dd:
                node = i.get('node')
                descr = node.get('accessibility_caption')
                t.add_row([str(count), descr])

                if self.jsonDump:
                    description = {
                        'description': descr
                    }
                    descriptions_list.append(description)

                count += 1

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_photodes.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['descriptions'] = descriptions_list
                json_file_name = self.output_dir + "/" + self.target + "_descriptions.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)
=======
        pc.printout("Getting photos descriptions...\n")
        
        try:
            medias = self.api.user_medias(self.target_id)
            if not medias:
                pc.printout("No photos found\n", pc.RED)
                return
                
            descriptions = []
            for media in medias:
                if media.caption_text:
                    descriptions.append(media.caption_text)
                    
            if descriptions:
                pc.printout("\nFound " + str(len(descriptions)) + " descriptions\n", pc.GREEN)

                if self.writeFile:
                    file_name = self.output_dir + "/" + self.target + "_photos_descriptions.txt"
                    with open(file_name, "w", encoding="utf-8") as f:
                        for description in descriptions:
                            f.write(description + "\n")

                if self.jsonDump:
                    json_data = {"descriptions": descriptions}
                    json_file_name = self.output_dir + "/" + self.target + "_photos_descriptions.json"
                    with open(json_file_name, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=2)
                        
                for description in descriptions:
                    print(description + "\n")
            else:
                pc.printout("No descriptions found\n", pc.RED)
                
        except Exception as e:
            pc.printout(f"Error getting photo descriptions: {str(e)}\n", pc.RED)
>>>>>>> 5473b8d (Secon commit)

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

<<<<<<< HEAD
        data = []
        counter = 0

        result = self.api.user_feed(str(self.target_id))
        data.extend(result.get('items', []))

        next_max_id = result.get('next_max_id')
        while next_max_id:
            results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
            data.extend(results.get('items', []))
            next_max_id = results.get('next_max_id')

        try:
            for item in data:
                if counter == limit:
                    break
                if "image_versions2" in item:
                    counter = counter + 1
                    url = item["image_versions2"]["candidates"][0]["url"]
                    photo_id = item["id"]
                    end = self.output_dir + "/" + self.target + "_" + photo_id + ".jpg"
                    urllib.request.urlretrieve(url, end)
                    sys.stdout.write("\rDownloaded %i" % counter)
                    sys.stdout.flush()
                else:
                    carousel = item["carousel_media"]
                    for i in carousel:
                        if counter == limit:
                            break
                        counter = counter + 1
                        url = i["image_versions2"]["candidates"][0]["url"]
                        photo_id = i["id"]
                        end = self.output_dir + "/" + self.target + "_" + photo_id + ".jpg"
                        urllib.request.urlretrieve(url, end)
                        sys.stdout.write("\rDownloaded %i" % counter)
                        sys.stdout.flush()

        except AttributeError:
            pass

        except KeyError:
            pass

        sys.stdout.write(" photos")
        sys.stdout.flush()

        pc.printout("\nWoohoo! We downloaded " + str(counter) + " photos (saved in " + self.output_dir + " folder) \n", pc.GREEN)

    def get_user_propic(self):

        try:
            endpoint = 'users/{user_id!s}/full_detail_info/'.format(**{'user_id': self.target_id})
            content = self.api._call_api(endpoint)

            data = content['user_detail']['user']

            if "hd_profile_pic_url_info" in data:
                URL = data["hd_profile_pic_url_info"]['url']
            else:
                #get better quality photo
                items = len(data['hd_profile_pic_versions'])
                URL = data["hd_profile_pic_versions"][items-1]['url']

            if URL != "":
                end = self.output_dir + "/" + self.target + "_propic.jpg"
                urllib.request.urlretrieve(URL, end)
                pc.printout("Target propic saved in output folder\n", pc.GREEN)

            else:
                pc.printout("Sorry! No results found :-(\n", pc.RED)
        
        except ClientError as e:
            error = json.loads(e.error_response)
            print(error['message'])
            print(error['error_title'])
            exit(2)
=======
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        data = []
        counter = 0

        try:
            # Get user's media feed
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
                        
                        # Download and save the photo
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
                            
                            # Download and save the carousel photo
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

    def get_user_propic(self):
        """Download target's profile picture"""
        if self.check_private_profile():
            return

        try:
            print_color("Fetching profile picture...", "yellow")
            user_info = self.api.user_info_by_username(self.target)
            
            if not user_info:
                print_color("Error: Could not fetch user information", "red")
                return

            profile_pic_url = user_info.profile_pic_url_hd
            if not profile_pic_url:
                print_color("Error: Could not get profile picture URL", "red")
                return

            # Download the image
            response = requests.get(profile_pic_url)
            if response.status_code == 200:
                # Create output directory if it doesn't exist
                os.makedirs(self.output_dir, exist_ok=True)
                
                # Save the image
                file_path = os.path.join(self.output_dir, f"{self.target}_profile_pic.jpg")
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print_color(f"Profile picture downloaded to {file_path}", "green")
            else:
                print_color(f"Failed to download profile picture. Status code: {response.status_code}", "red")

        except Exception as e:
            print_color(f"Error downloading profile picture: {str(e)}", "red")
>>>>>>> 5473b8d (Secon commit)

    def get_user_stories(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for target stories...\n")

        data = self.api.user_reel_media(str(self.target_id))

        counter = 0

        if data['items'] is not None:  # no stories avaibile
            counter = data['media_count']
            for i in data['items']:
                story_id = i["id"]
                if i["media_type"] == 1:  # it's a photo
                    url = i['image_versions2']['candidates'][0]['url']
                    end = self.output_dir + "/" + self.target + "_" + story_id + ".jpg"
                    urllib.request.urlretrieve(url, end)

                elif i["media_type"] == 2:  # it's a gif or video
                    url = i['video_versions'][0]['url']
                    end = self.output_dir + "/" + self.target + "_" + story_id + ".mp4"
                    urllib.request.urlretrieve(url, end)

        if counter > 0:
            pc.printout(str(counter) + " target stories saved in output folder\n", pc.GREEN)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_people_tagged_by_user(self):
        pc.printout("Searching for users tagged by target...\n")

        ids = []
        username = []
        full_name = []
        post = []
        counter = 1

        data = self.__get_feed__()

        try:
            for i in data:
                if "usertags" in i:
                    c = i.get('usertags').get('in')
                    for cc in c:
                        if cc.get('user').get('pk') not in ids:
                            ids.append(cc.get('user').get('pk'))
                            username.append(cc.get('user').get('username'))
                            full_name.append(cc.get('user').get('full_name'))
                            post.append(1)
                        else:
                            index = ids.index(cc.get('user').get('pk'))
                            post[index] += 1
                        counter = counter + 1
        except AttributeError as ae:
            pc.printout("\nERROR: an error occurred: ", pc.RED)
            print(ae)
            print("")
            pass

        if len(ids) > 0:
            t = PrettyTable()

            t.field_names = ['Posts', 'Full Name', 'Username', 'ID']
            t.align["Posts"] = "l"
            t.align["Full Name"] = "l"
            t.align["Username"] = "l"
            t.align["ID"] = "l"

            pc.printout("\nWoohoo! We found " + str(len(ids)) + " (" + str(counter) + ") users\n", pc.GREEN)

            json_data = {}
            tagged_list = []

            for i in range(len(ids)):
                t.add_row([post[i], full_name[i], username[i], str(ids[i])])

                if self.jsonDump:
                    tag = {
                        'post': post[i],
                        'full_name': full_name[i],
                        'username': username[i],
                        'id': ids[i]
                    }
                    tagged_list.append(tag)

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_tagged.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['tagged'] = tagged_list
                json_file_name = self.output_dir + "/" + self.target + "_tagged.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_user(self, username):
        try:
<<<<<<< HEAD
            content = self.api.username_info(username)
            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_user_id.txt"
                file = open(file_name, "w")
                file.write(str(content['user']['pk']))
                file.close()

            user = dict()
            user['id'] = content['user']['pk']
            user['is_private'] = content['user']['is_private']

            return user
        except ClientError as e:
            pc.printout('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response), pc.RED)
            error = json.loads(e.error_response)
            if 'message' in error:
                print(error['message'])
            if 'error_title' in error:
                print(error['error_title'])
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " + error['challenge']['url'])    
            sys.exit(2)
        
=======
            user = self.api.user_info_by_username(username)
            if not user:
                return None
            
            user_data = {
                'id': user.pk,
                'is_private': user.is_private
            }
            
            if self.writeFile:
                file_name = self.output_dir + "/" + username + "_user_id.txt"
                with open(file_name, "w") as f:
                    f.write(str(user.pk))
                
            return user_data
        
        except Exception as e:
            pc.printout(f'Error getting user data: {str(e)}\n', pc.RED)
            return None
>>>>>>> 5473b8d (Secon commit)

    def set_write_file(self, flag):
        if flag:
            pc.printout("Write to file: ")
            pc.printout("enabled", pc.GREEN)
            pc.printout("\n")
        else:
            pc.printout("Write to file: ")
            pc.printout("disabled", pc.RED)
            pc.printout("\n")

        self.writeFile = flag

    def set_json_dump(self, flag):
        if flag:
            pc.printout("Export to JSON: ")
            pc.printout("enabled", pc.GREEN)
            pc.printout("\n")
        else:
            pc.printout("Export to JSON: ")
            pc.printout("disabled", pc.RED)
            pc.printout("\n")

        self.jsonDump = flag

<<<<<<< HEAD
    def login(self, u, p):
        try:
            settings_file = "config/settings.json"
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print(f'Unable to find file: {settings_file!s}')

                # login new
                self.api = AppClient(auto_patch=True, authenticate=True, username=u, password=p,
                                     on_login=lambda x: self.onlogin_callback(x, settings_file))

            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=self.from_json)
                # print('Reusing settings: {0!s}'.format(settings_file))

                # reuse auth settings
                self.api = AppClient(
                    username=u, password=p,
                    settings=cached_settings,
                    on_login=lambda x: self.onlogin_callback(x, settings_file))

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print(f'ClientCookieExpiredError/ClientLoginRequiredError: {e!s}')

            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = AppClient(auto_patch=True, authenticate=True, username=u, password=p,
                                 on_login=lambda x: self.onlogin_callback(x, settings_file))

        except ClientError as e:
            pc.printout('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response), pc.RED)
            error = json.loads(e.error_response)
            pc.printout(error['message'], pc.RED)
            pc.printout(": ", pc.RED)
            pc.printout(e.msg, pc.RED)
            pc.printout("\n")
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " + error['challenge']['url'])
            exit(9)
=======
    def login_with_retry(self):
        """Login to Instagram with retry mechanism"""
        try:
            config = configparser.ConfigParser()
            config_path = os.path.join('config', 'credentials.ini')
            
            if not os.path.exists(config_path):
                print_color("Error: credentials.ini file not found in config directory", "red")
                return False
                
            config.read(config_path)
            
            if "Accounts" not in config:
                print_color("Error: No accounts configured in credentials.ini", "red")
                return False
                
            for account_name in config["Accounts"]:
                if account_name == "count":
                    continue
                    
                username = config[account_name].get("username")
                password = config[account_name].get("password")
                
                if not username or not password:
                    print_color(f"Error: Invalid credentials for account {account_name}", "red")
                    continue
                    
                try:
                    print_color(f"Attempting to login with username: {username}", "yellow")
                    self.api = Client()
                    
                    # Set proxy if configured
                    if self.proxy:
                        print_color(f"Using proxy: {self.proxy}", "yellow")
                        self.api.set_proxy(self.proxy)
                        
                    # Set custom device info
                    self.api.set_device({
                        "app_version": "269.0.0.18.75",
                        "android_version": "28",
                        "android_release": "9.0",
                        "dpi": "640dpi",
                        "resolution": "1440x2560",
                        "manufacturer": "samsung",
                        "device": "SM-G965F",
                        "model": "star2lte",
                        "cpu": "samsungexynos9810",
                        "version_code": "314665256"
                    })
                    
                    # Set user agent
                    self.api.set_user_agent("Instagram 269.0.0.18.75 Android (28/9.0; 640dpi; 1440x2560; samsung; SM-G965F; star2lte; samsungexynos9810; en_US; 314665256)")
                    
                    # Attempt login
                    login_response = self.api.login(username, password)
                    
                    if login_response:
                        print_color(f"Successfully logged in as {username}", "green")
                        self.current_account = username
                        return True
                    else:
                        print_color(f"Login failed for {username}: Invalid response", "red")
                        
                except Exception as e:
                    error_msg = str(e).lower()
                    if "challenge_required" in error_msg:
                        print_color(f"Instagram is requesting verification for {username}. Please check your email/phone for the verification code.", "yellow")
                        try:
                            # Handle verification
                            challenge = self.api.challenge_required()
                            if challenge:
                                print_color("Please enter the verification code: ", "yellow")
                                code = input()
                                self.api.challenge_code(code)
                                print_color(f"Successfully logged in as {username}", "green")
                                self.current_account = username
                                return True
                        except Exception as ve:
                            print_color(f"Verification failed: {str(ve)}", "red")
                    elif "bad_password" in error_msg:
                        print_color(f"Incorrect password for {username}", "red")
                    elif "invalid_user" in error_msg:
                        print_color(f"Account {username} does not exist", "red")
                    elif "blocked" in error_msg:
                        print_color(f"IP blocked. Please try again later or use a different proxy.", "red")
                    else:
                        print_color(f"Login failed for {username}: {str(e)}", "red")
                    continue
                    
            print_color("Failed to login with any account", "red")
            return False
            
        except Exception as e:
            print_color(f"Critical error during login: {str(e)}", "red")
            return False
>>>>>>> 5473b8d (Secon commit)

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def onlogin_callback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)
            # print('SAVED: {0!s}'.format(new_settings_file))

<<<<<<< HEAD
    def check_following(self):
        if str(self.target_id) == self.api.authenticated_user_id:
            return True
        try:
            # Try to get user info directly
            user_info = self.api.user_info(self.target_id)
            return user_info['user']['friendship_status']['following']
=======
    def check_following(self, user_info):
        try:
            me = self.api.user_info(self.api.user_id)
            if str(self.target_id) == str(me.pk):
                return True
            friendship = self.api.user_friendship(user_info.pk)
            return friendship.following
>>>>>>> 5473b8d (Secon commit)
        except Exception as e:
            print(f"Error checking following status: {str(e)}")
            return False

    def check_private_profile(self):
<<<<<<< HEAD
        if self.is_private and not self.following:
            pc.printout("Impossible to execute command: user has private profile\n", pc.RED)
            send = input("Do you want send a follow request? [Y/N]: ")
            if send.lower() == "y":
                self.api.friendships_create(self.target_id)
                print("Sent a follow request to target. Use this command after target accepting the request.")

            return True
        return False
=======
        """
        Check if the profile is private and handle follow request if needed
        """
        try:
            if not self.target_id:
                print_color("Target not set. Please set a target first.", "red")
                return True
                
            user_info = self.api.user_info_by_username(self.target)
            if not user_info:
                print_color(f"Could not find user {self.target}", "red")
                return True
                
            if user_info.is_private:
                print_color("Impossible to execute command: user has private profile\n", "red")
                if input("Do you want send a follow request? [Y/N]: ").lower() == 'y':
                    try:
                        self.api.follow_user(self.target_id)
                        print_color("Follow request sent\n", "green")
                    except Exception as e:
                        print_color(f"Failed to send follow request: {str(e)}\n", "red")
            return True
        except Exception as e:
            print_color(f"Error checking profile: {str(e)}\n", "red")
            return True
>>>>>>> 5473b8d (Secon commit)

    def get_fwersemail(self):
        if self.check_private_profile():
            return

        followers = []
        
        try:

            pc.printout("Searching for emails of target followers... this can take a few minutes\n")

<<<<<<< HEAD
            rank_token = AppClient.generate_uuid()
=======
            rank_token = Client.generate_uuid()
>>>>>>> 5473b8d (Secon commit)
            data = self.api.user_followers(str(self.target_id), rank_token=rank_token)

            for user in data.get('users', []):
                u = {
                    'id': user['pk'],
                    'username': user['username'],
                    'full_name': user['full_name']
                }
                followers.append(u)

            next_max_id = data.get('next_max_id')
            while next_max_id:
                sys.stdout.write("\rCatched %i followers email" % len(followers))
                sys.stdout.flush()
                results = self.api.user_followers(str(self.target_id), rank_token=rank_token, max_id=next_max_id)
                
                for user in results.get('users', []):
                    u = {
                        'id': user['pk'],
                        'username': user['username'],
                        'full_name': user['full_name']
                    }
                    followers.append(u)

                next_max_id = results.get('next_max_id')
            
            print("\n")

            results = []
            
            pc.printout("Do you want to get all emails? y/n: ", pc.YELLOW)
            value = input()
            
            if value == str("y") or value == str("yes") or value == str("Yes") or value == str("YES"):
                value = len(followers)
            elif value == str(""):
                print("\n")
                return
            elif value == str("n") or value == str("no") or value == str("No") or value == str("NO"):
                while True:
                    try:
                        pc.printout("How many emails do you want to get? ", pc.YELLOW)
                        new_value = int(input())
                        value = new_value - 1
                        break
                    except ValueError:
                        pc.printout("Error! Please enter a valid integer!", pc.RED)
                        print("\n")
                        return
            else:
                pc.printout("Error! Please enter y/n :-)", pc.RED)
                print("\n")
                return

            for follow in followers:
                user = self.api.user_info(str(follow['id']))
                if 'public_email' in user['user'] and user['user']['public_email']:
                    follow['email'] = user['user']['public_email']
                    if len(results) > value:
                        break
                    results.append(follow)

        except ClientThrottledError  as e:
            pc.printout("\nError: Instagram blocked the requests. Please wait a few minutes before you try again.", pc.RED)
            pc.printout("\n")

        if len(results) > 0:

            t = PrettyTable(['ID', 'Username', 'Full Name', 'Email'])
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"
            t.align["Email"] = "l"

            json_data = {}

            for node in results:
                t.add_row([str(node['id']), node['username'], node['full_name'], node['email']])

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_fwersemail.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['followers_email'] = results
                json_file_name = self.output_dir + "/" + self.target + "_fwersemail.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_fwingsemail(self):
        if self.check_private_profile():
            return

        followings = []

        try:

            pc.printout("Searching for emails of users followed by target... this can take a few minutes\n")

<<<<<<< HEAD
            rank_token = AppClient.generate_uuid()
=======
            rank_token = Client.generate_uuid()
>>>>>>> 5473b8d (Secon commit)
            data = self.api.user_following(str(self.target_id), rank_token=rank_token)

            for user in data.get('users', []):
                u = {
                    'id': user['pk'],
                    'username': user['username'],
                    'full_name': user['full_name']
                }
                followings.append(u)

            next_max_id = data.get('next_max_id')
            
            while next_max_id:
                results = self.api.user_following(str(self.target_id), rank_token=rank_token, max_id=next_max_id)

                for user in results.get('users', []):
                    u = {
                        'id': user['pk'],
                        'username': user['username'],
                        'full_name': user['full_name']
                    }
                    followings.append(u)

                next_max_id = results.get('next_max_id')
        
            results = []
            
            pc.printout("Do you want to get all emails? y/n: ", pc.YELLOW)
            value = input()
            
            if value == str("y") or value == str("yes") or value == str("Yes") or value == str("YES"):
                value = len(followings)
            elif value == str(""):
                print("\n")
                return
            elif value == str("n") or value == str("no") or value == str("No") or value == str("NO"):
                while True:
                    try:
                        pc.printout("How many emails do you want to get? ", pc.YELLOW)
                        new_value = int(input())
                        value = new_value - 1
                        break
                    except ValueError:
                        pc.printout("Error! Please enter a valid integer!", pc.RED)
                        print("\n")
                        return
            else:
                pc.printout("Error! Please enter y/n :-)", pc.RED)
                print("\n")
                return

            for follow in followings:
                sys.stdout.write("\rCatched %i followings email" % len(results))
                sys.stdout.flush()
                user = self.api.user_info(str(follow['id']))
                if 'public_email' in user['user'] and user['user']['public_email']:
                    follow['email'] = user['user']['public_email']
                    if len(results) > value:
                        break
                    results.append(follow)
        
        except ClientThrottledError as e:
            pc.printout("\nError: Instagram blocked the requests. Please wait a few minutes before you try again.", pc.RED)
            pc.printout("\n")
        
        print("\n")

        if len(results) > 0:
            t = PrettyTable(['ID', 'Username', 'Full Name', 'Email'])
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"
            t.align["Email"] = "l"

            json_data = {}

            for node in results:
                t.add_row([str(node['id']), node['username'], node['full_name'], node['email']])

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_fwingsemail.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['followings_email'] = results
                json_file_name = self.output_dir + "/" + self.target + "_fwingsemail.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_fwingsnumber(self):
<<<<<<< HEAD
        if self.check_private_profile():
            return
       
        try:

            pc.printout("Searching for phone numbers of users followed by target... this can take a few minutes\n")

            followings = []

            rank_token = AppClient.generate_uuid()
            data = self.api.user_following(str(self.target_id), rank_token=rank_token)

            for user in data.get('users', []):
                u = {
                    'id': user['pk'],
                    'username': user['username'],
                    'full_name': user['full_name']
                }
                followings.append(u)

            next_max_id = data.get('next_max_id')
            
            while next_max_id:
                results = self.api.user_following(str(self.target_id), rank_token=rank_token, max_id=next_max_id)

                for user in results.get('users', []):
                    u = {
                        'id': user['pk'],
                        'username': user['username'],
                        'full_name': user['full_name']
                    }
                    followings.append(u)

                next_max_id = results.get('next_max_id')
       
            results = []
        
            pc.printout("Do you want to get all phone numbers? y/n: ", pc.YELLOW)
            value = input()
            
            if value == str("y") or value == str("yes") or value == str("Yes") or value == str("YES"):
                value = len(followings)
            elif value == str(""):
                print("\n")
                return
            elif value == str("n") or value == str("no") or value == str("No") or value == str("NO"):
                while True:
                    try:
                        pc.printout("How many phone numbers do you want to get? ", pc.YELLOW)
                        new_value = int(input())
                        value = new_value - 1
                        break
                    except ValueError:
                        pc.printout("Error! Please enter a valid integer!", pc.RED)
                        print("\n")
                        return
            else:
                pc.printout("Error! Please enter y/n :-)", pc.RED)
                print("\n")
                return

            for follow in followings:
                sys.stdout.write("\rCatched %i followings phone numbers" % len(results))
                sys.stdout.flush()
                user = self.api.user_info(str(follow['id']))
                if 'contact_phone_number' in user['user'] and user['user']['contact_phone_number']:
                    follow['contact_phone_number'] = user['user']['contact_phone_number']
                    if len(results) > value:
                        break
                    results.append(follow)

        except ClientThrottledError as e:
            pc.printout("\nError: Instagram blocked the requests. Please wait a few minutes before you try again.", pc.RED)
            pc.printout("\n")
        
        print("\n")

        if len(results) > 0:
            t = PrettyTable(['ID', 'Username', 'Full Name', 'Phone'])
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"
            t.align["Phone number"] = "l"

            json_data = {}

            for node in results:
                t.add_row([str(node['id']), node['username'], node['full_name'], node['contact_phone_number']])

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_fwingsnumber.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['followings_phone_numbers'] = results
                json_file_name = self.output_dir + "/" + self.target + "_fwingsnumber.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)
=======
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
>>>>>>> 5473b8d (Secon commit)

    def get_fwersnumber(self):
        if self.check_private_profile():
            return

        followings = []

        try:

            pc.printout("Searching for phone numbers of users followers... this can take a few minutes\n")


<<<<<<< HEAD
            rank_token = AppClient.generate_uuid()
=======
            rank_token = Client.generate_uuid()
>>>>>>> 5473b8d (Secon commit)
            data = self.api.user_following(str(self.target_id), rank_token=rank_token)

            for user in data.get('users', []):
                u = {
                    'id': user['pk'],
                    'username': user['username'],
                    'full_name': user['full_name']
                }
                followings.append(u)

            next_max_id = data.get('next_max_id')
            
            while next_max_id:
                results = self.api.user_following(str(self.target_id), rank_token=rank_token, max_id=next_max_id)

                for user in results.get('users', []):
                    u = {
                        'id': user['pk'],
                        'username': user['username'],
                        'full_name': user['full_name']
                    }
                    followings.append(u)

                next_max_id = results.get('next_max_id')
        
            results = []
            
            pc.printout("Do you want to get all phone numbers? y/n: ", pc.YELLOW)
            value = input()
            
            if value == str("y") or value == str("yes") or value == str("Yes") or value == str("YES"):
                value = len(followings)
            elif value == str(""):
                print("\n")
                return
            elif value == str("n") or value == str("no") or value == str("No") or value == str("NO"):
                while True:
                    try:
                        pc.printout("How many phone numbers do you want to get? ", pc.YELLOW)
                        new_value = int(input())
                        value = new_value - 1
                        break
                    except ValueError:
                        pc.printout("Error! Please enter a valid integer!", pc.RED)
                        print("\n")
                        return
            else:
                pc.printout("Error! Please enter y/n :-)", pc.RED)
                print("\n")
                return

            for follow in followings:
                sys.stdout.write("\rCatched %i followers phone numbers" % len(results))
                sys.stdout.flush()
                user = self.api.user_info(str(follow['id']))
                if 'contact_phone_number' in user['user'] and user['user']['contact_phone_number']:
                    follow['contact_phone_number'] = user['user']['contact_phone_number']
                    if len(results) > value:
                        break
                    results.append(follow)

        except ClientThrottledError as e:
            pc.printout("\nError: Instagram blocked the requests. Please wait a few minutes before you try again.", pc.RED)
            pc.printout("\n")

        print("\n")

        if len(results) > 0:
            t = PrettyTable(['ID', 'Username', 'Full Name', 'Phone'])
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"
            t.align["Phone number"] = "l"

            json_data = {}

            for node in results:
                t.add_row([str(node['id']), node['username'], node['full_name'], node['contact_phone_number']])

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_fwersnumber.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['followings_phone_numbers'] = results
<<<<<<< HEAD
                json_file_name = self.output_dir + "/" + self.target + "_fwerssnumber.json"
=======
                json_file_name = self.output_dir + "/" + self.target + "_fwersnumber.json"
>>>>>>> 5473b8d (Secon commit)
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)

            print(t)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def get_comments(self):
        if self.check_private_profile():
            return

        pc.printout("Searching for users who commented...\n")

        data = self.__get_feed__()
        users = []

        for post in data:
            comments = self.__get_comments__(post['id'])
            for comment in comments:
                print(comment['text'])
                
                # if not any(u['id'] == comment['user']['pk'] for u in users):
                #     user = {
                #         'id': comment['user']['pk'],
                #         'username': comment['user']['username'],
                #         'full_name': comment['user']['full_name'],
                #         'counter': 1
                #     }
                #     users.append(user)
                # else:
                #     for user in users:
                #         if user['id'] == comment['user']['pk']:
                #             user['counter'] += 1
                #             break

        if len(users) > 0:
            ssort = sorted(users, key=lambda value: value['counter'], reverse=True)

            json_data = {}

            t = PrettyTable()

            t.field_names = ['Comments', 'ID', 'Username', 'Full Name']
            t.align["Comments"] = "l"
            t.align["ID"] = "l"
            t.align["Username"] = "l"
            t.align["Full Name"] = "l"

            for u in ssort:
                t.add_row([str(u['counter']), u['id'], u['username'], u['full_name']])

            print(t)

            if self.writeFile:
                file_name = self.output_dir + "/" + self.target + "_users_who_commented.txt"
                file = open(file_name, "w")
                file.write(str(t))
                file.close()

            if self.jsonDump:
                json_data['users_who_commented'] = ssort
                json_file_name = self.output_dir + "/" + self.target + "_users_who_commented.json"
                with open(json_file_name, 'w') as f:
                    json.dump(json_data, f)
        else:
            pc.printout("Sorry! No results found :-(\n", pc.RED)

    def clear_cache(self):
        try:
            f = open("config/settings.json",'w')
            f.write("{}")
            pc.printout("Cache Cleared.\n",pc.GREEN)
        except FileNotFoundError:
            pc.printout("Settings.json don't exist.\n",pc.RED)
        finally:
            f.close()

<<<<<<< HEAD
    def show_account_status(self):
        """Show current account status and allow manual account switching."""
        t = PrettyTable()
        t.field_names = ['Index', 'Username', 'Status']
        t.align["Index"] = "l"
        t.align["Username"] = "l"
        t.align["Status"] = "l"

        for i, (username, _) in enumerate(self.account_manager.accounts):
            status = "Rate Limited" if i in self.account_manager.rate_limited_accounts else "Active"
            if i == self.account_manager.get_current_account_index():
                status = "Current Account"
            t.add_row([str(i), username, status])

        print("\nAccount Status:")
        print(t)
        
        pc.printout("\nCurrent account: ", pc.GREEN)
        pc.printout(self.api.username + "\n", pc.CYAN)
        
        pc.printout("\nDo you want to switch accounts? (y/n): ", pc.YELLOW)
        if input().lower() == 'y':
            self.login_with_account_switching()
            pc.printout(f"\nSwitched to account: {self.api.username}\n", pc.GREEN)

    def setup_accounts(self):
        """Interactive setup for Instagram accounts and switch delay."""
        pc.printout("\nInstagram Account Setup\n", pc.YELLOW)
        pc.printout("=====================\n", pc.YELLOW)
        
        # Get number of accounts
        while True:
            try:
                pc.printout("How many Instagram accounts do you want to add? (1-10): ", pc.YELLOW)
                num_accounts = int(input())
                if 1 <= num_accounts <= 10:
                    break
                else:
                    pc.printout("Please enter a number between 1 and 10\n", pc.RED)
            except ValueError:
                pc.printout("Please enter a valid number\n", pc.RED)
        
        # Get switch delay
        while True:
            try:
                pc.printout("Enter switch delay in seconds (recommended: 60): ", pc.YELLOW)
                switch_delay = int(input())
                if switch_delay > 0:
                    break
                else:
                    pc.printout("Please enter a positive number\n", pc.RED)
            except ValueError:
                pc.printout("Please enter a valid number\n", pc.RED)
        
        # Get account credentials
        accounts = {}
        for i in range(1, num_accounts + 1):
            pc.printout(f"\nAccount {i}:\n", pc.CYAN)
            
            while True:
                pc.printout("Username: ", pc.YELLOW)
                username = input().strip()
                if username:
                    break
                pc.printout("Username cannot be empty\n", pc.RED)
            
            while True:
                pc.printout("Password: ", pc.YELLOW)
                password = input().strip()
                if password:
                    break
                pc.printout("Password cannot be empty\n", pc.RED)
            
            accounts[f"account{i}"] = f"{username}:{password}"
        
        # Write to credentials.ini
        try:
            with open("config/credentials.ini", "w") as f:
                f.write("[Accounts]\n")
                f.write("# Add your Instagram accounts below\n")
                f.write("# Format: account_name = username:password\n")
                f.write("# You can add as many accounts as you want\n")
                for account_name, credentials in accounts.items():
                    f.write(f"{account_name} = {credentials}\n")
                
                f.write("\n[Settings]\n")
                f.write("# Maximum number of accounts to use simultaneously\n")
                f.write(f"max_accounts = {num_accounts}\n")
                f.write("# Time to wait before switching accounts (in seconds)\n")
                f.write(f"switch_delay = {switch_delay}\n")
            
            pc.printout("\nConfiguration saved successfully!\n", pc.GREEN)
            pc.printout("You can now use the 'accounts' command to view and manage your accounts.\n", pc.GREEN)
            
            # Reload account manager with new settings
            self.account_manager = AccountManager()
            
        except Exception as e:
            pc.printout(f"\nError saving configuration: {str(e)}\n", pc.RED)
=======
    def get_posts_analysis(self):
        """Get AI analysis of posts"""
        if not self.ai_analyzer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        posts = self._get_posts_impl()
        if posts:
            ai_analysis = self.ai_analyzer.analyze_posts(posts)
            pc.printout("\nAI Analysis of Posts:\n", pc.CYAN)
            print(ai_analysis)

    def get_profile_summary(self):
        """Get AI-powered profile summary"""
        if not self.ai_analyzer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            user_info = self.api.user_info_by_username(self.target)
            posts = self._get_posts_impl()
            followers = self._get_followers_impl()
            following = self._get_followings_impl()
            
            summary = self.ai_analyzer.generate_profile_summary(
                user_info=user_info,
                posts=posts,
                followers=followers,
                following=following
            )
            
            if summary:
                pc.printout("\nAI Profile Summary:\n", pc.CYAN)
                print(summary)
        except Exception as e:
            pc.printout(f"Error generating profile summary: {str(e)}\n", pc.RED)

    def get_sentiment_analysis(self, data_type="caption"):
        """Get sentiment analysis for captions or comments"""
        if not self.ai_analyzer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            if data_type == "caption":
                posts = self._get_posts_impl()
                text_data = [post.get('caption', '') for post in posts]
            else:  # comments
                posts = self._get_posts_impl()
                text_data = []
                for post in posts:
                    comments = self._get_comments_impl(post['id'])
                    text_data.extend([comment.get('text', '') for comment in comments])
            
            analysis = self.ai_analyzer.analyze_sentiment(text_data, data_type)
            
            if analysis:
                pc.printout(f"\nAI {data_type.title()} Sentiment Analysis:\n", pc.CYAN)
                print(analysis)
        except Exception as e:
            pc.printout(f"Error in sentiment analysis: {str(e)}\n", pc.RED)

    def get_hashtag_categories(self):
        """Get AI-powered hashtag categorization"""
        if not self.ai_analyzer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            hashtags = self._get_hashtags_impl()
            categories = self.ai_analyzer.categorize_hashtags(hashtags)
            
            if categories:
                pc.printout("\nAI Hashtag Categorization:\n", pc.CYAN)
                print(categories)
        except Exception as e:
            pc.printout(f"Error in hashtag categorization: {str(e)}\n", pc.RED)

    def get_timeline_correlation(self):
        """Get AI-powered timeline event correlation"""
        if not self.ai_analyzer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            posts = self._get_posts_impl()
            comments = []
            likes = []
            
            for post in posts:
                post_comments = self._get_comments_impl(post['id'])
                comments.extend(post_comments)
                likes.append(post.get('like_count', 0))
            
            correlation = self.ai_analyzer.correlate_timeline_events(posts, comments, likes)
            
            if correlation:
                pc.printout("\nAI Timeline Event Correlation:\n", pc.CYAN)
                print(correlation)
        except Exception as e:
            pc.printout(f"Error in timeline correlation: {str(e)}\n", pc.RED)

    def get_ai_report(self):
        """Generate comprehensive AI report"""
        if not self.ai_analyzer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            all_data = {
                "user_info": self.api.user_info_by_username(self.target),
                "posts": self._get_posts_impl(),
                "followers": self._get_followers_impl(),
                "following": self._get_followings_impl(),
                "hashtags": self._get_hashtags_impl()
            }
            
            report = self.ai_analyzer.generate_natural_language_report(all_data)
            
            if report:
                pc.printout("\nAI Generated Report:\n", pc.CYAN)
                print(report)
        except Exception as e:
            pc.printout(f"Error generating AI report: {str(e)}\n", pc.RED)

    def add_target_data(self, target, data):
        """Add data for a target to the targets_data dictionary"""
        self.targets_data[target] = data

    def get_target_prioritization(self):
        """Get AI-powered target prioritization"""
        if not self.target_prioritizer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            analysis = self.target_prioritizer.analyze_targets(self.targets_data)
            if analysis:
                pc.printout("\nAI Target Prioritization:\n", pc.CYAN)
                print(analysis)
        except Exception as e:
            pc.printout(f"Error in target prioritization: {str(e)}\n", pc.RED)

    def get_target_report(self):
        """Generate comprehensive AI report for all targets"""
        if not self.target_prioritizer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            report = self.target_prioritizer.generate_target_report(self.targets_data)
            if report:
                pc.printout("\nAI Target Report:\n", pc.CYAN)
                print(report)
        except Exception as e:
            pc.printout(f"Error generating target report: {str(e)}\n", pc.RED)

    def get_target_relationships(self):
        """Analyze relationships between targets"""
        if not self.target_prioritizer.enabled:
            pc.printout("AI features are disabled. Run setup_ai.py to enable them.\n", pc.RED)
            return
        
        try:
            analysis = self.target_prioritizer.analyze_target_relationships(self.targets_data)
            if analysis:
                pc.printout("\nAI Target Relationship Analysis:\n", pc.CYAN)
                print(analysis)
        except Exception as e:
            pc.printout(f"Error analyzing target relationships: {str(e)}\n", pc.RED)

    def _handle_rate_limit(self):
        """Handle rate limiting by rotating IP and retrying"""
        if self.retry_count >= self.MAX_RETRIES:
            pc.printout("Maximum retry attempts reached. Please try again later.\n", pc.RED)
            return False
        
        self.retry_count += 1
        pc.printout(f"Rate limit detected. Attempting to rotate IP (Attempt {self.retry_count}/{self.MAX_RETRIES})...\n", pc.YELLOW)
        
        if self.ip_rotator.rotate_ip():
            time.sleep(5)  # Wait for IP rotation to take effect
            return True
        else:
            pc.printout("Failed to rotate IP. Please try again later.\n", pc.RED)
            return False

    def _make_request(self, func, *args, **kwargs):
        """Wrapper for making requests with automatic IP rotation"""
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "rate limit" in str(e).lower():
                    if not self._handle_rate_limit():
                        raise e
                else:
                    raise e

    def _get_posts_impl(self):
        """Get user's posts implementation"""
        try:
            if not self.target_id:
                print_color("Target not set. Please set a target first.", "red")
                return []
                
            # Get user's media using user_medias
            medias = self.api.user_medias(self.target_id)
            if not medias:
                print_color(f"No posts found for user {self.target}", "red")
                return []
                
            # Convert medias to the expected format
            posts = []
            for media in medias:
                post = {
                    'id': media.id,
                    'caption': media.caption_text if media.caption_text else '',
                    'taken_at': media.taken_at.timestamp(),
                    'like_count': media.like_count,
                    'comment_count': media.comment_count,
                    'media_type': media.media_type,
                    'usertags': [tag.user.username for tag in media.usertags] if media.usertags else [],
                    'hashtags': [tag for tag in media.caption_text.split() if tag.startswith('#')] if media.caption_text else []
                }
                posts.append(post)
                
            return posts
            
        except Exception as e:
            print_color(f"Error getting posts: {str(e)}", "red")
            return []

    def _get_followings_impl(self):
        """Get user's followings implementation"""
        try:
            if not self.target_id:
                print_color("Target not set. Please set a target first.", "red")
                return []
                
            # Get user's followings using user_following
            followings = self.api.user_following(self.target_id)
            if not followings:
                print_color(f"No followings found for user {self.target}", "red")
                return []
                
            # Convert followings to the expected format
            following_list = []
            for user_id, user_info in followings.items():
                following = {
                    'id': user_id,
                    'username': user_info.username,
                    'full_name': user_info.full_name,
                    'is_private': user_info.is_private,
                    'is_verified': user_info.is_verified,
                    'media_count': user_info.media_count,
                    'follower_count': user_info.follower_count,
                    'following_count': user_info.following_count,
                    'biography': user_info.biography if user_info.biography else ''
                }
                following_list.append(following)
                
            return following_list
            
        except Exception as e:
            print_color(f"Error getting followings: {str(e)}", "red")
            return []
>>>>>>> 5473b8d (Secon commit)
