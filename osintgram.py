#!/usr/bin/env python3

import os
import sys
import argparse
from src.Osintgram import Osintgram
from src.print_color import print_color

def main():
    parser = argparse.ArgumentParser(description='Osintgram - Instagram OSINT Tool')
    parser.add_argument('username', help='Instagram username to analyze')
    parser.add_argument('--config', '-c', help='Path to config file', default='config/config.ini')
    parser.add_argument('--ai-config', '-a', help='Path to AI config file', default='config/ai_config.ini')
    
    args = parser.parse_args()
    
    try:
        # Initialize Osintgram
        osint = Osintgram(args.username, args.config, args.ai_config)
        
        # Print welcome message
        print_color("Osintgram - Instagram OSINT Tool", "green")
        print_color(f"Analyzing profile: {args.username}", "blue")
        print()
        
        # Get profile summary
        print_color("Profile Summary:", "yellow")
        osint.get_profile_summary()
        print()
        
        # Get followers analysis
        print_color("Followers Analysis:", "yellow")
        osint.get_followers()
        print()
        
        # Get posts analysis
        print_color("Posts Analysis:", "yellow")
        osint.get_posts_analysis()
        print()
        
        # Get hashtags analysis
        print_color("Hashtags Analysis:", "yellow")
        osint.get_hashtags()
        print()
        
        # Get sentiment analysis
        print_color("Sentiment Analysis:", "yellow")
        osint.get_sentiment_analysis()
        print()
        
        # Get hashtag categories
        print_color("Hashtag Categories:", "yellow")
        osint.get_hashtag_categories()
        print()
        
        # Get timeline correlation
        print_color("Timeline Correlation:", "yellow")
        osint.get_timeline_correlation()
        print()
        
        # Generate comprehensive report
        print_color("Generating Comprehensive Report...", "yellow")
        osint.get_ai_report()
        
    except Exception as e:
        print_color(f"Error: {str(e)}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main() 