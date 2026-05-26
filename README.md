# Skysecure AI Agent

An intelligent AI Agent built with FastAPI and Groq LLM, featuring conversational memory and a clean dark UI.

## Live Demo
🔗 https://skysecure-agent-production.up.railway.app/

## Features
- AI Agent — Powered by Groq's LLaMA 3.3 70B model
- Conversational Memory — Remembers last 5 exchanges in session
- Clean Dark UI — Professional dark-themed chat interface
- REST API — FastAPI backend with /chat endpoint
- Live Deployment — Hosted on Railway

## Tech Stack
- Backend — FastAPI + Uvicorn
- AI — Groq API (LLaMA 3.3 70B)
- Deployment — Railway
- Language — Python 3.13

## Project Structure
skysecure-agent/
├── main.py          # FastAPI app + UI
├── agent.py         # Groq AI agent logic
├── requirements.txt # Dependencies
├── Procfile         # Railway start command
└── .env             # API keys (not committed)

## Getting Started

1. Clone the repo
git clone https://github.com/Kushal-ctrl-del/skysecure-agent

2. Install dependencies
pip install -r requirements.txt

3. Add .env file
GROQ_API_KEY=your_groq_api_key_here

4. Run locally
uvicorn main:app --reload

## Author
Kushal Sankla
AI Developer · Solutions Architect · Prompt Engineer
GitHub: https://github.com/Kushal-ctrl-del
Portfolio: https://kushalsankla.vercel.app
