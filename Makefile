.PHONY: setup clean install

setup:
	@echo "####### Setup for Osintgram #######"
	@if [ -f config/credentials.ini ]; then \
		echo "Current accounts:"; \
		accounts=$$(grep -o 'account[0-9]*' config/credentials.ini | sort -V | uniq); \
		if [ -z "$$accounts" ]; then \
			echo "You don't have any accounts added. Please add one."; \
		else \
			count=1; \
			for acc in $$accounts; do \
				username=$$(grep -A1 "$$acc" config/credentials.ini | grep "username" | cut -d'=' -f2 | tr -d ' '); \
				if [ -n "$$username" ]; then \
					echo "$$count. $$username"; \
					count=$$((count + 1)); \
				fi; \
			done | sort -u; \
		fi; \
	else \
		echo "You don't have any accounts added. Please add one."; \
	fi
	@echo ""
	@echo "1. Add new accounts"
	@echo "2. Replace existing accounts"
	@echo "3. Add more accounts to existing ones"
	@echo "4. Add OpenAI API Key"
	@echo "5. Exit"
	@read -p "Enter your choice (1-5): " choice; \
	case "$$choice" in \
		1|3) \
			read -p "How many accounts do you want to add? (1-10): " num_accounts; \
			if [ "$$num_accounts" -ge 1 ] && [ "$$num_accounts" -le 10 ]; then \
				python3 setup_accounts.py --add $$num_accounts; \
			else \
				echo "Invalid number of accounts. Please enter a number between 1 and 10."; \
			fi; \
			;; \
		2) \
			if [ -f config/credentials.ini ]; then \
				echo "Select account to replace:"; \
				accounts=$$(grep -o 'account[0-9]*' config/credentials.ini | sort -V | uniq); \
				if [ -z "$$accounts" ]; then \
					echo "No accounts found to replace."; \
				else \
					valid_count=0; \
					> /tmp/accounts.tmp; \
					for acc in $$accounts; do \
						username=$$(grep -A1 "$$acc" config/credentials.ini | grep "username" | cut -d'=' -f2 | tr -d ' '); \
						if [ -n "$$username" ] && ! grep -q "$$username" /tmp/accounts.tmp; then \
							valid_count=$$((valid_count + 1)); \
							echo "$$valid_count. $$username" >> /tmp/accounts.tmp; \
						fi; \
					done; \
					if [ $$valid_count -gt 0 ]; then \
						cat /tmp/accounts.tmp; \
						read -p "Enter account number to replace (1-$$valid_count): " acc_num; \
						if [ "$$acc_num" -ge 1 ] && [ "$$acc_num" -le $$valid_count ]; then \
							acc_to_replace=$$(sed -n "$$acc_num p" /tmp/accounts.tmp | cut -d' ' -f2); \
							acc_section=$$(grep -B1 "username = $$acc_to_replace" config/credentials.ini | head -n1 | cut -d'[' -f2 | cut -d']' -f1); \
							acc_num=$$(echo "$$acc_section" | sed 's/account//'); \
							if [ -n "$$acc_num" ]; then \
								python3 setup_accounts.py --replace $$acc_num; \
							else \
								echo "Error: Could not determine account number."; \
							fi; \
						else \
							echo "Invalid account number. Please try again."; \
						fi; \
					else \
						echo "No valid accounts found to replace."; \
					fi; \
					rm -f /tmp/accounts.tmp; \
				fi; \
			else \
				echo "No accounts found to replace."; \
			fi; \
			;; \
		4) \
			mkdir -p config; \
			read -p "Enter your OpenAI API Key: " api_key; \
			if [ -f config/ai_config.ini ]; then \
				sed -i "s/^api_key = .*/api_key = $$api_key/" config/ai_config.ini; \
				sed -i "s/^enabled = .*/enabled = true/" config/ai_config.ini; \
			else \
				echo "[OpenAI]" > config/ai_config.ini; \
				echo "enabled = true" >> config/ai_config.ini; \
				echo "api_key = $$api_key" >> config/ai_config.ini; \
				echo "model = gpt-3.5-turbo" >> config/ai_config.ini; \
				echo "max_tokens = 100" >> config/ai_config.ini; \
			fi; \
			echo -e "\e[32mAPI Key configured successfully!\e[0m"; \
			;; \
		5) \
			echo "Setup cancelled."; \
			;; \
		*) \
			echo "Invalid choice. Please try again."; \
			;; \
	esac

clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@rm -rf src/__pycache__
	@rm -rf *.pyc
	@echo "Done!"

install:
	@echo "Installing dependencies..."
	@pip3 install -r requirements.txt
	@echo "Done!"

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