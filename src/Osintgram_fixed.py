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
        if self.check_private_profile():
            return

        print_color("Searching for phone numbers of users followed by target...\n", "yellow")

        try:
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