# 🤖 Agentic AI Portfolio Assistant

An AI-powered portfolio assistant that answers questions about **Venkata Sai Kowshik** using information from a **LinkedIn profile PDF** and a **personal summary knowledge base**.

This project demonstrates how **Agentic AI systems** can be used to create an interactive portfolio experience where visitors can ask questions and receive interview-style responses grounded in real information.

---

# 🚀 Overview

The **Agentic AI Portfolio Assistant** acts like a personal interview assistant that represents the developer online.

Instead of static portfolio pages, visitors can interact with an AI chatbot that answers questions about:

* background
* skills
* education
* professional interests
* career journey

The assistant reads information from a **knowledge base** and generates responses strictly based on that data.

If the assistant does not have enough information to answer a question, it:

1. Responds honestly that the information is unavailable
2. Logs the question
3. Sends a **Telegram notification** for tracking visitor interest

This helps understand what recruiters or visitors want to know about the developer.

---

# 📚 Knowledge Base

The assistant retrieves information from a structured knowledge base included in the project.

### Files used as knowledge sources

```
data/
   Profile.pdf
   summary.txt
```

**Profile.pdf**

* Exported LinkedIn profile
* Contains education, skills, experience, and certifications

**summary.txt**

* Personal summary describing interests, technical focus, and work style

When a question is asked, the system provides these documents as context to the AI model, ensuring responses remain **accurate and grounded**.

If the requested information does not exist in the knowledge base, the assistant replies:

> "I don't have information about that in my background."

---

# 🧠 Key Features

* AI portfolio assistant
* Interview-style conversational responses
* Knowledge-base grounded answers
* Groq LLM integration
* Gradio chat interface
* Telegram alert system
* Unknown question tracking
* Modular enterprise architecture
* Conversation memory management

---

# 🏗 Project Architecture

```
agentic-ai/
│
├── app.py
│
├── config/
│   └── settings.py
│
├── agent/
│   ├── agent.py
│   ├── prompts.py
│   └── memory.py
│
├── services/
│   ├── llm_service.py
│   └── telegram_service.py
│
├── tools/
│   ├── record_user.py
│   └── record_question.py
│
├── data/
│   ├── Profile.pdf
│   └── summary.txt
│
└── requirements.txt
```

---

# ⚙️ System Workflow

```
User Question
      ↓
Gradio Chat Interface
      ↓
Portfolio AI Agent
      ↓
Knowledge Base (PDF + Summary)
      ↓
Groq Language Model
      ↓
Tool Execution (Lead / Question Tracking)
      ↓
Telegram Notifications
      ↓
Response to User
```

---

# 🛠 Installation

### Clone the repository

```
git clone https://github.com/<your-username>/agentic-ai-portfolio-assistant.git
cd agentic-ai-portfolio-assistant
```

---

### Create virtual environment

```
python -m venv .venv
```

Activate environment

Windows

```
.venv\Scripts\activate
```

Mac/Linux

```
source .venv/bin/activate
```

---

### Install dependencies

```
pip install -r requirements.txt
```

---

### Configure environment variables

Create a `.env` file

```
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

---

### Add knowledge base files

Place your data inside the `data` directory:

```
data/
   Profile.pdf
   summary.txt
```

---

### Run the application

```
python app.py
```

Open the chatbot at:

```
http://127.0.0.1:7860
```

---

# 📩 Telegram Notifications

The system sends Telegram alerts for important events.

### Unknown Question

```
❓ Unknown Question

Do you have experience with Kubernetes?
```

### Lead Capture

```
📩 New Lead

Name: John Doe
Email: john@email.com
Notes: Interested in collaboration
```

This allows monitoring what visitors or recruiters are interested in.

---

# 💡 Example Questions

Users can ask questions such as:

* Tell me about yourself
* What technologies do you work with?
* What is your educational background?
* What are your interests in AI?

If the assistant does not know the answer, it will respond honestly.

---

# 🧩 Technologies Used

* Python
* Groq LLM API
* Gradio
* Telegram Bot API
* PyPDF
* Python-Dotenv

---

# 🔮 Future Improvements

Potential enhancements for the system include:

* vector database memory (RAG)
* recruiter analytics dashboard
* automatic email extraction
* lead scoring
* multi-model support (OpenAI, Gemini, Claude)
* containerized deployment with Docker

---

# 📄 License

MIT License

Copyright (c) 2026 Venkata Sai Kowshik

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---

# ✍️ Author

**Venkata Sai Kowshik Gowrakkavari**

📧 Email: [kowshikgowrakkavari777@gmail.com](mailto:kowshikgowrakkavari777@gmail.com)
🔗 LinkedIn:
https://www.linkedin.com/in/venkata-sai-kowshik-144984230
