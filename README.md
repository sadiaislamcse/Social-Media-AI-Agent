# 🤖 Social Media AI Agent

> A fully autonomous Facebook content agent that runs 24/7 — controlled entirely from Telegram.

---

## 🚀 What It Does

I used to spend hours every week planning content, writing posts, finding images, and scheduling everything manually. So I automated the entire workflow using AI.

**Now the system works like this:**

1. Open Telegram → type your niche and language
2. Bot generates a **7-day content calendar** using AI
3. Writes professional **Facebook posts** automatically
4. Creates **matching images** with Stability AI
5. Shows a **preview** before publishing
6. One tap → **publishes directly to Facebook**
7. Runs in the **cloud 24/7** — even when your laptop is closed

---

## ✨ Features

- 🗓️ **AI Content Calendar** — 7-day plan generated based on your niche and audience problems
- ✍️ **Smart Post Generator** — Professional posts in English or Bangla using Llama 3
- 🎨 **Image Generation** — Matching visuals created with Stability AI
- 📱 **Telegram Control Panel** — Full bot control from your phone
- 📤 **Auto Publisher** — Posts directly to Facebook via Graph API
- 🔁 **Regenerate & Skip** — Preview, regenerate, or skip any post before publishing
- ☁️ **Cloud Hosted** — Runs on Railway 24/7 without any manual intervention

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Bot Interface | Telegram Bot API |
| AI / LLM | Groq (Llama 3.3 70B) |
| Image Generation | Stability AI (SDXL) |
| Publishing | Facebook Graph API |
| Hosting | Railway |
| CI/CD | GitHub Actions |

---

## 📁 Project Structure

```
├── bot.py               # Telegram bot — main control interface
├── main.py              # Standalone runner (without Telegram)
├── generator.py         # AI post generator (Groq/LLaMA)
├── publisher.py         # Facebook Graph API publisher
├── planner.py           # Random topic & tone planner
├── calendar_planner.py  # 7-day AI content calendar generator
├── image.py             # Stability AI image generator
├── memory.py            # Post history tracker
├── config.py            # Environment variable loader
├── schedule.py          # Time-based scheduler
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/sadiaislamcse/Social-Media-AI-Agent.git
cd Social-Media-AI-Agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file or add these to your hosting platform:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_telegram_chat_id
GROQ_API_KEY=your_groq_api_key
PAGE_ID=your_facebook_page_id
PAGE_ACCESS_TOKEN=your_facebook_page_token
STABILITY_API_KEY=your_stability_ai_key
```

### 4. Run the bot
```bash
python bot.py
```

---

## 📱 How to Use (Telegram Commands)

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/setniche` | Set your content niche |
| `/calendar` | Generate 7-day content calendar |
| `/viewcalendar` | View current calendar progress |
| `/postnow` | Generate & publish next post |
| `/status` | Check bot status |
| `/end` | Stop the bot |

**Or just type:**
```
niche: Digital Marketing
language: Bangla
```

---

## 💡 What I Learned

The hardest part wasn't writing the code.

It was making everything work together **reliably** — handling token expiry, image generation timeouts, API conflicts, failed requests, retries… real production problems.

This project taught me that building with AI is not just calling an API. It's about designing **systems that can run on their own**, handle failures, and keep working without supervision.

---

## 🔗 Connect

If you're interested in agentic AI, automation, or autonomous workflows — let's connect!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/sadiaislamcse)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/sadiaislamcse)

---

## 📌 Tags

`#AIAgent` `#Automation` `#Python` `#FacebookMarketing` `#AgenticAI` `#BuildInPublic`
