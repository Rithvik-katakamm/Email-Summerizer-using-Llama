from typing import List
from pydantic import BaseModel
from ollama import chat

class EmailAnalysis(BaseModel):
    """Structured output for email analysis"""
    priority: int  # 1-10 scale (1=low, 10=critical)
    has_action_items: bool
    action_items: List[str]  # Empty list if no action items
    summary: str  # 2-3 sentences max, very concise

class EmailSummarizer:
    """Analyzes emails using Ollama with structured outputs"""
    
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
    
    def analyze_email(self, email_content: str, subject: str = "", sender: str = "") -> EmailAnalysis:
        """Analyze a single email and return structured results"""
        
        # Create the analysis prompt
        prompt = f"""
Analyze this email and provide a structured analysis. Be very concise and actionable.

EMAIL:
Subject: {subject}
From: {sender}
Content: {email_content}

Rate priority 1-10 where:
- 1-3: Informational, no urgency
- 4-6: Important but not urgent  
- 7-8: High priority, needs attention soon
- 9-10: Critical, immediate action required

For action items, be specific. If there are deadlines, mention them.
Summary should be 2-3 sentences maximum.
"""

        try:
            response = chat(
                model=self.model,
                format=EmailAnalysis.model_json_schema(),
                messages=[{
                    'role': 'user', 
                    'content': prompt
                }],
                options={'temperature': 0}  # More consistent results
            )
            
            # Parse the structured response
            analysis = EmailAnalysis.model_validate_json(response.message.content)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing email: {e}")
            # Return default analysis if something goes wrong
            return EmailAnalysis(
                priority=5,
                has_action_items=False,
                action_items=[],
                summary="Could not analyze this email properly."
            )
    
    def analyze_emails_batch(self, emails: List[dict]) -> List[dict]:
        """Analyze multiple emails and return results with original email data"""
        results = []
        
        for email in emails:
            analysis = self.analyze_email(
                email_content=email.get('body', ''),
                subject=email.get('subject', ''),
                sender=email.get('sender', '')
            )
            
            # Combine original email data with analysis
            result = {
                'original': email,
                'analysis': analysis
            }
            results.append(result)
        
        return results
    
    def get_high_priority_emails(self, analyzed_emails: List[dict], threshold: int = 7) -> List[dict]:
        """Filter emails above priority threshold"""
        return [email for email in analyzed_emails 
                if email['analysis'].priority >= threshold]
    
    def format_priority_summary(self, high_priority_emails: List[dict]) -> str:
        """Format high priority emails for text message"""
        if not high_priority_emails:
            return "No high priority emails."
        
        count = len(high_priority_emails)
        summary = f"You have {count} high priority email{'s' if count > 1 else ''}:\n"
        
        for i, email in enumerate(high_priority_emails[:3], 1):  # Max 3 for text
            analysis = email['analysis']
            subject = email['original'].get('subject', 'No Subject')[:50]  # Truncate long subjects
            
            if analysis.action_items:
                action = analysis.action_items[0][:60]  # First action item, truncated
                summary += f"{i}. {subject} - {action}\n"
            else:
                summary += f"{i}. {subject} - {analysis.summary[:60]}\n"
        
        if count > 3:
            summary += f"...and {count - 3} more"
        
        return summary.strip()
    
    def format_all_emails_summary(self, analyzed_emails: List[dict]) -> str:
        """Format all emails for detailed summary"""
        if not analyzed_emails:
            return "No unread emails."
        
        summary = f"Summary of {len(analyzed_emails)} unread emails:\n\n"
        
        for i, email in enumerate(analyzed_emails, 1):
            analysis = email['analysis']
            original = email['original']
            
            priority_text = "🔴" if analysis.priority >= 8 else "🟡" if analysis.priority >= 6 else "🟢"
            
            summary += f"{i}. {priority_text} [{analysis.priority}/10] {original.get('subject', 'No Subject')}\n"
            summary += f"   From: {original.get('sender', 'Unknown')}\n"
            summary += f"   {analysis.summary}\n"
            
            if analysis.action_items:
                summary += f"   Actions: {', '.join(analysis.action_items)}\n"
            
            summary += "\n"
        
        return summary.strip()
