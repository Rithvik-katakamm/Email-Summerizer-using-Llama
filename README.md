# 📧 Intelligent Email Summarizer

> **Privacy-first email automation** that transforms your Gmail inbox into actionable insights using **local AI** and **structured outputs**.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-green.svg)
![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-red.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🚀 **What This Does**

A **smart email management system** that automatically:
- 📥 Pulls unread emails from Gmail
- 🧠 Analyzes them with **local Llama 3.2** (no data sent to cloud)
- 🎯 Identifies high-priority emails requiring immediate attention
- 📱 Sends **instant iMessage alerts** for urgent items
- 📊 Provides **structured summaries** with actionable insights

**Perfect for busy professionals** who need to stay on top of important emails without constantly checking their inbox.

## ⚡ **Key Features**

### **🔒 Privacy-First Design**
- **100% local processing** - your emails never leave your device
- Uses **Ollama** for on-device AI inference
- **No cloud API calls** for email analysis

### **🎯 Smart Priority Detection**  
- **1-10 priority scoring** based on content analysis
- **Automatic action item extraction** from email content
- **Deadline and date recognition** for time-sensitive tasks
- **Intelligent categorization** of email types

### **📱 Instant Notifications**
- **iMessage integration** for immediate high-priority alerts
- **Configurable thresholds** for what constitutes "urgent"
- **Clean, actionable summaries** delivered to your phone

### **🛠️ Production-Ready Architecture**
- **Structured outputs** using Pydantic models for reliability
- **Error handling** and graceful failure modes
- **Configurable via JSON** - no code changes needed
- **Modular design** with clean separation of concerns

## 📋 **Example Output**

### High Priority Alert (iMessage):
```
📧 Email Alert:
You have 3 high priority emails:
1. Interview Tomorrow - Confirm availability by March 14th
2. Project Deadline - Submit report by Friday 5 PM  
3. Client Meeting - Reschedule required ASAP
```

### Console Analysis:
```
🔴 [8/10] Interview Tomorrow - Marketing Coordinator
   From: alex.chen@greentech.com
   Interview invitation with specific time slots available
   Actions: Reply within 2 business days, Confirm availability

🟡 [6/10] Quarterly Report Due Next Week  
   From: manager@company.com
   Q1 reports due Friday March 22nd by 5 PM
   Actions: Complete quarterly report, Include discussed metrics
```

## 🏗️ **Technical Architecture**

### **Core Components**
- **`GmailFetcher`** - Secure Gmail API integration with OAuth2
- **`EmailSummarizer`** - Local Llama 3.2 analysis with structured outputs  
- **`NotificationSender`** - Native macOS iMessage integration
- **`main.py`** - Orchestrates the complete workflow

### **Technology Stack**
- **Python 3.7+** with modern async/await patterns
- **Ollama + Llama 3.2** for local AI inference
- **Pydantic** for structured data validation
- **Google Gmail API** for secure email access
- **AppleScript** for native iMessage integration

### **Design Patterns**
- **Single Responsibility Principle** - each class has one clear purpose
- **Dependency Injection** - configuration-driven behavior
- **Structured Data** - type-safe outputs using Pydantic models
- **Error Boundaries** - graceful handling of API failures

## 🎯 **Use Cases**

**Perfect for:**
- 👨‍💼 **Executives** managing high email volumes
- 🎓 **Job seekers** tracking application responses  
- 📈 **Project managers** monitoring deadline communications
- 🏢 **Consultants** staying responsive to client requests
- 🚀 **Anyone** who wants intelligent email prioritization

## 📊 **Performance**

- **~2GB RAM usage** (Llama 3.2 3B model)
- **~3-5 seconds per email** analysis time
- **Batch processing** for efficiency with multiple emails
- **Local inference** - no network latency for AI analysis

## 🔧 **Installation & Setup**

### **Prerequisites**
- macOS (for iMessage integration)
- Python 3.7+
- Ollama installed locally

### **Quick Start**
```bash
# Clone the repository
git clone https://github.com/Rithvik-katakamm/Email-Summerizer-using-Llama.git
cd Email-Summerizer-using-Llama

# Set up environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install and configure Ollama
ollama pull llama3.2:3b

# Configure your settings
cp config.json.example config.json
# Edit config.json with your Gmail and phone details

# Set up Gmail API credentials (see setup guide)
# Download credentials.json from Google Cloud Console

# Run the system
python src/main.py
```

### **Gmail API Setup**
1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 Desktop App credentials  
3. Download `credentials.json`
4. Add yourself as a test user in OAuth consent screen

*Detailed setup instructions available in the [testing/SETUP.md](testing/SETUP.md) file.*

## 💡 **What Makes This Special**

### **Privacy-Focused**
Unlike cloud-based solutions, this processes your emails entirely **on your local machine**. Your sensitive email content never leaves your device.

### **Actually Actionable**  
Instead of generic summaries, extracts **specific action items** with deadlines and priorities, helping you **act** rather than just read.

### **Intelligent Prioritization**
Uses advanced prompt engineering with structured outputs to provide **consistent, reliable** priority scoring and categorization.

### **Native Integration**
Leverages **macOS iMessage** for notifications that feel natural and immediate, not just another app notification.

## 🛣️ **Future Roadmap**

- [ ] **Calendar integration** - detect meeting conflicts and scheduling
- [ ] **Slack integration** - extend to other communication channels  
- [ ] **Custom models** - fine-tune for specific email patterns
- [ ] **iOS Shortcuts** - trigger analysis from mobile
- [ ] **Advanced filtering** - ML-based sender importance scoring

## 🔗 **Connect**

Built by **Rithvik Katakamm** - demonstrating expertise in AI/ML integration, API development, local AI deployment, structured data processing, macOS automation, and privacy-focused software design.

---

**Built with ❤️ for personal productivity and email sanity.**
