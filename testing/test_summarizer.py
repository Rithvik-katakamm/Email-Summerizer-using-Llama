#!/usr/bin/env python3
"""
Test script to verify the email summarizer works without Gmail API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.email_summarizer import EmailSummarizer
from src.notification_sender import NotificationSender

def test_summarizer():
    """Test the email summarizer with sample emails"""
    
    # Sample emails for testing
    test_emails = [
        {
            'subject': 'Interview Tomorrow - Marketing Coordinator',
            'sender': 'alex.chen@greentech.com',
            'body': '''Dear Ms. Thompson,

We would like to invite you to participate in interviews for the Marketing Coordinator position. The interviews will be held on:

* Tuesday, March 14th at 2 PM EST (1 hour)
* Thursday, March 16th at 10 AM EST (1 hour)

Please reply to confirm your availability within the next two business days. Call (555) 123-4567.

Best regards,
Alex Chen''',
            'date': '2024-03-12',
            'id': 'test1'
        },
        {
            'subject': 'Quarterly Report Due Next Week',
            'sender': 'manager@company.com',
            'body': '''Hi Team,

Just a reminder that the Q1 quarterly reports are due next Friday, March 22nd by 5 PM. Please make sure to include all the metrics we discussed in the last meeting.

Let me know if you have any questions.

Thanks,
Sarah''',
            'date': '2024-03-15',
            'id': 'test2'
        },
        {
            'subject': 'Weekly Newsletter - Tech Updates',
            'sender': 'newsletter@techsite.com',
            'body': '''This week in tech:

- New AI model released by OpenAI
- Apple announces new MacBook Pro
- Tesla stock hits new high

Read more at our website.

Unsubscribe | Privacy Policy''',
            'date': '2024-03-15',
            'id': 'test3'
        }
    ]
    
    print("🧪 Testing Email Summarizer...")
    print("="*50)
    
    # Initialize summarizer
    summarizer = EmailSummarizer(model="llama3.2:3b")
    
    # Test each email
    for i, email in enumerate(test_emails, 1):
        print(f"\n📧 Testing Email {i}:")
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        print("-" * 30)
        
        try:
            analysis = summarizer.analyze_email(
                email_content=email['body'],
                subject=email['subject'],
                sender=email['sender']
            )
            
            print(f"Priority: {analysis.priority}/10")
            print(f"Has Action Items: {analysis.has_action_items}")
            if analysis.action_items:
                print(f"Action Items: {analysis.action_items}")
            print(f"Summary: {analysis.summary}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("="*50)
    
    # Test batch analysis
    print("\n🔄 Testing Batch Analysis...")
    try:
        analyzed_emails = summarizer.analyze_emails_batch(test_emails)
        high_priority = summarizer.get_high_priority_emails(analyzed_emails, threshold=7)
        
        print(f"✅ Analyzed {len(analyzed_emails)} emails")
        print(f"📈 Found {len(high_priority)} high priority emails")
        
        if high_priority:
            priority_summary = summarizer.format_priority_summary(high_priority)
            print("\n🚨 Priority Summary:")
            print(priority_summary)
        
        print("\n📋 Full Summary:")
        full_summary = summarizer.format_all_emails_summary(analyzed_emails)
        print(full_summary)
        
    except Exception as e:
        print(f"❌ Batch analysis error: {e}")

def test_notifications():
    """Test iMessage notifications (optional)"""
    print("\n📱 Testing Notifications...")
    
    # This will only work if you update the phone number
    test_phone = "+1234567890"  # Update this to your actual number to test
    
    notifier = NotificationSender(phone_number=test_phone)
    
    # Uncomment to test (make sure to update phone number first)
    # notifier.send_imessage("🧪 Test message from Email Summarizer!")

if __name__ == "__main__":
    print("🚀 Email Summarizer Test Suite")
    print("="*50)
    
    test_summarizer()
    
    # Uncomment to test notifications
    # test_notifications()
    
    print("\n✅ Testing complete!")
    print("\nTo test with real Gmail:")
    print("1. Set up Gmail API credentials")
    print("2. Update config.json with your details")
    print("3. Run: python src/main.py")
