import subprocess

class NotificationSender:
    """Sends iMessage notifications using AppleScript"""
    
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
    
    def send_imessage(self, message_text: str) -> bool:
        """Send iMessage using AppleScript"""
        apple_script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{self.phone_number}" of targetService
            send "{message_text}" to targetBuddy
        end tell
        '''
        
        try:
            process = subprocess.Popen(
                ['osascript', '-e', apple_script], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()
            
            if stderr:
                print(f"Error sending message: {stderr.decode()}")
                return False
            else:
                print("Message sent successfully!")
                return True
                
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False
    
    def send_priority_alert(self, priority_summary: str) -> bool:
        """Send high priority email alert"""
        message = f"📧 Email Alert:\n{priority_summary}"
        return self.send_imessage(message)
    
    def send_full_summary(self, full_summary: str) -> bool:
        """Send complete email summary"""
        # Split long messages if needed (iMessage has limits)
        if len(full_summary) > 1000:
            # Send in chunks
            chunks = [full_summary[i:i+1000] for i in range(0, len(full_summary), 1000)]
            for i, chunk in enumerate(chunks):
                message = f"📧 Email Summary ({i+1}/{len(chunks)}):\n{chunk}"
                if not self.send_imessage(message):
                    return False
            return True
        else:
            message = f"📧 Email Summary:\n{full_summary}"
            return self.send_imessage(message)
