# Osintgram - Instagram OSINT Tool

A powerful Instagram OSINT tool with AI capabilities for gathering and analyzing Instagram data.

## Features

- Multiple account support
- AI-powered analysis
- IP rotation
- Profile information gathering
- Media analysis
- Hashtag analysis
- Follower/following analysis
- And much more!

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Arunking9/Insta-Ocent-tool-Custom.git
cd Insta-Ocent-tool-Custom
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Configure your accounts:
```bash
python3 setup_accounts.py
```

4. (Optional) Configure AI features:
```bash
python3 setup_ai.py
```

## Usage

1. Run the tool:
```bash
python3 main.py <target_username>
```

2. Available commands:
- `list` - Show all available commands
- `info` - Get target info
- `propic` - Download profile picture
- `followers` - Get followers list
- `following` - Get following list
- `hashtags` - Get used hashtags
- `fwersemail` - Get followers emails
- `fwingsemail` - Get following emails
- `fwersnumber` - Get followers phone numbers
- `fwingsnumber` - Get following phone numbers
- `posts` - Get posts info
- `stories` - Get stories info
- `highlights` - Get highlights info
- `tagged` - Get tagged posts
- `wtagged` - Get posts where target is tagged
- `saved` - Get saved posts
- `tagged` - Get tagged posts
- `wtagged` - Get posts where target is tagged
- `saved` - Get saved posts

## AI Features

The tool includes AI-powered analysis capabilities:
- Profile summary generation
- Sentiment analysis
- Hashtag categorization
- Timeline correlation
- Comprehensive reports

To enable AI features, run `setup_ai.py` and configure your OpenAI API key.

## Requirements

- Python 3.7+
- Instagram account(s)
- (Optional) OpenAI API key for AI features

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with Instagram's terms of service.

## License

MIT License

## Contributors

- DemonKing369 (Main Developer)
