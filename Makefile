SHELL := /bin/bash

setup:

	@echo -e "\e[34m####### Setup for Osintgram #######\e[0m"
	@[ -d config ] || mkdir config || exit 1
	@echo -n "{}" > config/settings.json
	
	# Get number of accounts
	@read -p "How many Instagram accounts do you want to add? (1-10): " num_accounts; \
	if ! [[ "$$num_accounts" =~ ^[1-9]$|^10$ ]]; then \
		echo -e "\e[31mPlease enter a number between 1 and 10\e[0m"; \
		exit 1; \
	fi
	
	# Get switch delay
	@read -p "Enter switch delay in seconds (recommended: 60): " switch_delay; \
	if ! [[ "$$switch_delay" =~ ^[0-9]+$ ]] || [ "$$switch_delay" -le 0 ]; then \
		echo -e "\e[31mPlease enter a positive number\e[0m"; \
		exit 1; \
	fi
	
	# Create credentials.ini with header
	@echo -e "[Accounts]\n# Add your Instagram accounts below\n# Format: account_name = username:password\n# You can add as many accounts as you want" > config/credentials.ini
	
	# Get account credentials
	@for i in $$(seq 1 $$num_accounts); do \
		echo -e "\n\e[36mAccount $$i:\e[0m"; \
		read -p "Username: " username; \
		read -sp "Password: " password; \
		echo ""; \
		if [ -z "$$username" ] || [ -z "$$password" ]; then \
			echo -e "\e[31mUsername and password cannot be empty\e[0m"; \
			exit 1; \
		fi; \
		echo "account$$i = $$username:$$password" >> config/credentials.ini; \
	done
	
	# Add settings section
	@echo -e "\n[Settings]\n# Maximum number of accounts to use simultaneously\nmax_accounts = $$num_accounts\n# Time to wait before switching accounts (in seconds)\nswitch_delay = $$switch_delay" >> config/credentials.ini
	
	@echo -e "\n\e[32mSetup Successful - config/credentials.ini created with $$num_accounts account(s)\e[0m"

run:

	@echo -e "\e[34m######## Building and Running Osintgram with Docker-compose ########\e[0m"
	@[ -d config ] || { echo -e "\e[31mConfig folder not found! Please run 'make setup' before running this command.\e[0m"; exit 1; }
	@echo -e "\e[34m[#] Killing old docker processes\e[0m"
	@docker-compose rm -fs || exit 1
	@echo -e "\e[34m[#] Building docker container\e[0m"
	@docker-compose build || exit 1
	@read -p "Target Username: " username; \
	docker-compose run --rm osintgram $$username

build-run-testing:

	@echo -e "\e[34m######## Building and Running Osintgram with Docker-compose for Testing/Debugging ########\e[0m"
	@[ -d config ] || { echo -e "\e[31mConfig folder not found! Please run 'make setup' before running this command.\e[0m"; exit 1; }
	@echo -e "\e[34m[#] Killing old docker processes\e[0m"
	@docker-compose rm -fs || exit 1
	@echo -e "\e[34m[#] Building docker container\e[0m"
	@docker-compose build || exit 1
	@echo -e "\e[34m[#] Running docker container in detached mode\e[0m"
	@docker-compose run --name osintgram-testing -d --rm --entrypoint "sleep infinity" osintgram || exit 1
	@echo -e "\e[32m[#] osintgram-test container is now Running!\e[0m"

cleanup-testing:
	@echo -e "\e[34m######## Cleanup Build-run-testing Container ########\e[0m"
	@docker-compose down
	@echo -e "\e[32m[#] osintgram-test container has been removed\e[0m"