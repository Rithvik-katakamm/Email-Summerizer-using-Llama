#!/usr/bin/env python3
"""
Simple Email Summarizer
Pulls unread Gmail emails, analyzes them with Ollama, sends iMessage alerts for high priority emails
"""

import json
import os
import sys
from gmail_fetcher import GmailFetcher
from email_summarizer import EmailSummarizer
from notification_sender import NotificationSender

def load_config(config_path: str = "config.json") -> dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file {config_path} not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Invalid JSON in {config_path}")
        sys.exit(1)

def main():
    """Main function - does exactly what you asked for"""
    print("🔄 Starting Email Summarizer...")
    
    # Load config
    config = load_config()
    
    # Initialize components
    gmail = GmailFetcher(
        credentials_file=config['gmail']['credentials_file'],
        token_file=config['gmail']['token_file'],
        target_email=config['gmail']['email_address']
    )
    
    summarizer = EmailSummarizer(model=config['ai']['model'])
    notifier = NotificationSender(phone_number=config['notifications']['phone_number'])
    
    print("📧 Fetching unread emails...")
    
    # Get unread emails
    emails = gmail.get_unread_emails(max_results=config['settings']['max_emails_to_process'])
    
    if not emails:
        print("✅ No unread emails found!")
        notifier.send_imessage("📧 No unread emails in your inbox!")
        return
    
    print(f"📊 Analyzing {len(emails)} emails...")
    
    # Analyze all emails
    analyzed_emails = summarizer.analyze_emails_batch(emails)
    
    # Get high priority emails
    high_priority = summarizer.get_high_priority_emails(
        analyzed_emails, 
        threshold=config['ai']['priority_threshold']
    )
    
    # Send priority alert if needed
    if high_priority:
        print(f"🚨 Found {len(high_priority)} high priority emails!")
        priority_summary = summarizer.format_priority_summary(high_priority)
        print("Priority Summary:")
        print(priority_summary)
        print("\n" + "="*50 + "\n")
        
        # Send the priority alert
        notifier.send_priority_alert(priority_summary)
    else:
        print("✅ No high priority emails found.")
    
    # Always ask if they want full summary
    print("\n📋 Email Analysis Complete!")
    print(f"Total emails: {len(emails)}")
    print(f"High priority: {len(high_priority)}")
    
    # Ask for full summary
    while True:
        response = input("\nDo you want a summary of every unread email? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("📱 Sending full email summary...")
            full_summary = summarizer.format_all_emails_summary(analyzed_emails)
            print("\nFull Summary:")
            print(full_summary)
            notifier.send_full_summary(full_summary)
            break
        elif response in ['n', 'no']:
            print("✅ Done!")
            break
        else:
            print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    main()
