import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from typing import List, Dict

class GmailFetcher:
    """Fetches unread emails from Gmail using Gmail API"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self, credentials_file: str, token_file: str, target_email: str):
        self.credentials_file = credentials_file
        self.token_file = token_file  
        self.target_email = target_email
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_unread_emails(self, max_results: int = 20) -> List[Dict[str, str]]:
        """Get unread emails from the specified email address"""
        try:
            # Query for unread emails to the target email
            query = f'is:unread to:{self.target_email}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            emails = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id'],
                    format='full'
                ).execute()
                
                email_data = self._parse_email(msg)
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except Exception as error:
            print(f'An error occurred: {error}')
            return []
    
    def _parse_email(self, message: Dict) -> Dict[str, str]:
        """Parse Gmail message into readable format"""
        try:
            payload = message['payload']
            headers = payload.get('headers', [])
            
            # Extract headers
            subject = ""
            sender = ""
            date = ""
            
            for header in headers:
                name = header.get('name', '').lower()
                value = header.get('value', '')
                
                if name == 'subject':
                    subject = value
                elif name == 'from':
                    sender = value
                elif name == 'date':
                    date = value
            
            # Extract body
            body = self._extract_body(payload)
            
            return {
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'id': message['id']
            }
            
        except Exception as e:
            print(f"Error parsing email: {e}")
            return {}
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html' and not body:
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
