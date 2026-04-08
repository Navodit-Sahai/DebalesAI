# Debales AI Assistant

A simple AI chatbot that answers questions about Debales AI using RAG, and handles everything else via web search. Built with LangGraph + Groq.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
```

Get a free Groq key at [console.groq.com](https://console.groq.com)

## Run

```bash
python main.py        # CLI
streamlit run app.py  # Web UI
```

## How it works

Every query gets routed automatically:
- Debales AI question → searches the scraped knowledge base (RAG)
- General question → searches the web (SERP)
- Both → uses both sources
- Gibberish → honest "I don't know"

## CLI commands

| Command | Action |
|---|---|
| `/rebuild` | Re-scrape Debales website |
| `/clear` | Clear chat history |
| `/quit` | Exit |

## Stack
LangGraph · Groq LLaMA-3.3-70b · FAISS · HuggingFace Embeddings · SerpAPI / DuckDuckGo