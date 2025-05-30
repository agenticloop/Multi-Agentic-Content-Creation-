# Multi-Agentic Content Creation System Using Smolagents

![image](https://github.com/user-attachments/assets/7137e4e5-4eab-4bab-b8ef-b89171959869)


Welcome to the **Multi-Agentic Content Creation System**, a powerful framework designed to automate content creation across multiple platforms. This system leverages a network of specialized agents to research, create, optimize, and distribute high-quality content. From blog posts to social media updates, everything is orchestrated to ensure a seamless, engaging experience for content creators and marketers.

## 🚀 Overview

This system is composed of several agents, each responsible for a unique step in the content creation process. The flow is managed by the **Orchestrator** agent, which ensures that each task is completed and communicated effectively, even in case of failures.

### Key Agents

- **Orchestrator**: Manages the flow of the entire content creation process and ensures communication between all agents.
- **Researcher Agent**: Gathers relevant data, topics, and sources for content creation.
- **Blog Writer Agent**: Creates blog posts based on research data.
- **Twitter Agent**: Curates engaging tweets based on blog content and relevant web searches.
- **LinkedIn Agent**: Creates professional and engaging LinkedIn posts.
- **Optimizing Agent**: Refines the content to ensure it’s engaging, humanized, and user-friendly.

## 🔄 System Flow

The system operates as follows:

1. **Orchestrator Invocation**: The system starts when the `/start` endpoint is triggered. The orchestrator first checks the `/health` endpoint to confirm all agents are operational.
2. **Data Collection**: The orchestrator collects topics, links, and further information from the provided spreadsheet, passing the data to the **Researcher Agent**.
3. **Research Phase**: The **Researcher Agent** gathers in-depth data and returns the results to the orchestrator.
4. **Blog Writing**: The **Blog Writer Agent** then takes the research and generates three blog posts.
5. **Social Media Content Creation**:
   - The **Twitter Agent** creates engaging tweets, including AI-related content, humor, and news updates.
   - The **LinkedIn Agent** creates educational and entertaining posts for LinkedIn.
6. **Optimization**: The **Optimizing Agent** refines the content to make it more engaging and user-friendly.
7. **Final Output**: Once all agents complete their tasks, the orchestrator sends the content in JSON format to the user via email, including:
   - Three blog posts in JSON format
   - Tweets in JSON format
   - LinkedIn posts in JSON format

## 🧩 Agent Details

### Orchestrator Agent

The **Orchestrator** acts as the system’s central control, invoking agents and ensuring a seamless process. It handles:
- Triggering the `/start` endpoint
- Checking the health of all agents
- Coordinating data flow between agents
- Sending completion reports to the user via email

### Researcher Agent

The **Researcher Agent** dives deep into the provided links and topics to gather relevant data for blog post creation. It performs:
- Comprehensive research based on the provided sources (papers, websites, etc.)
- Returning the gathered information in an organized format for the blog writing process

### Blog Writer Agent

The **Blog Writer Agent**, known as *The Illuminator*, generates insightful blog posts by transforming research data into readable, engaging content. This agent:
- Creates three blog posts based on the information received
- Uses a humanized writing style, making complex concepts more accessible to a wide audience

### Twitter Agent

The **Twitter Agent** generates engaging tweets using the blog posts and additional web searches. It creates:
- 6 tweets from the blog posts
- 6 additional tweets based on trending AI topics, including motivational, humorous, and informative content
- Returns all tweets to the orchestrator for final processing

### LinkedIn Agent

The **LinkedIn Agent** creates professional and educational LinkedIn posts. It:
- Converts blog content into 3 educational posts
- Creates 2 humorous and 1 relatable post
- Sends the posts back to the orchestrator for final delivery

### Optimizing Agent

The **Optimizing Agent**, also known as *The Clarity Crusader*, enhances the content to ensure it’s clear, concise, and engaging. This agent:
- Refines the blog posts, tweets, and LinkedIn posts
- Improves readability by removing jargon and simplifying complex ideas
- Ensures that content aligns with the tone and style of the Agentic Loop brand

### 🔄 Workflow Diagram

Here’s a simplified view of the system's workflow:

Orchestrator -> Researcher Agent

Researcher Agent -> Blog Writer Agent

Blog Writer Agent -> Twitter Agent / LinkedIn Agent

Twitter Agent / LinkedIn Agent -> Optimizing Agent

Optimizing Agent -> Orchestrator (Sends final content via email)

## ⚙️ Setup & Installation

To set up the **Multi-Agentic Content Creation System** on your local machine, follow the steps below:

### 1. Clone the Repository

```bash
git clone https://github.com/agenticloop/Multi-Agentic-Content-Creation-.git

cd Multi-Agentic-Content-Creation-
```
### 2. Install requirements
```
pip install -r requirements.txt
```

### 3. Configure API KEYS in .env 

```
# Gemini API Keys
GEMINI_API_KEY=your_api_key

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=youremail@gmail.com
SMTP_PASSWORD=your_app_password_generated_from_google_account_details
RECIPIENT_EMAIL=recipient_email_address@gmail.com 

# Google Sheets Configuration
GOOGLE_SHEETS_ID=your_id
GOOGLE_SHEETS_RANGE=Sheet1!A:Z
GOOGLE_SERVICE_ACCOUNT_KEY=service-account-key.json # Generate from google cloud project

```

### 4. Run 
```
python main.py
```



### 🛠️ Technologies Used

Programming Language: Python

Framework: FastAPI 

Agentic library: Smolagents




### 📜 License
This project is licensed under the Apache 2.0 License.




### 📢 Contributing
We welcome contributions! If you would like to contribute to the development of this project, please follow these steps:

Fork the repository

Create a branch for your feature or bugfix

Submit a pull request with a detailed explanation of your changes




### 📞 Support
For any questions or business inquiries, please:

Reach out at contact@agenticloop.co or visit www.agenticloop.co
