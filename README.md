# 🛎️ Smart Support Desk

> An AI-powered customer support triage system that reads incoming emails, retrieves the most relevant company policy using vector search, and auto-drafts structured replies — all running locally.

---

## 🧠 What It Does

E-commerce support teams handle hundreds of tickets daily. This system automates the first layer:

1. **Reads** an incoming customer email
2. **Searches** a local ChromaDB vector store for the most relevant company policy
3. **Injects** that policy as context into an LLM prompt
4. **Returns** a structured output: Priority, Category, and a draft reply — grounded only in policy

No hallucinations. If the policy doesn't cover the case, the system escalates to a human agent.

---

## 🏗️ Architecture

```
Customer Email
      │
      ▼
 ChromaDB (local vector store)
 ── semantic search over company policies ──►  Matched Policy
                                                      │
                                                      ▼
                                          Prompt = Policy + Email
                                                      │
                                                      ▼
                                            MiniCPM (LLM via API)
                                                      │
                                                      ▼
                                    ┌─────────────────────────────┐
                                    │  PRIORITY: Urgent / Low     │
                                    │  CATEGORY: Refund / ...     │
                                    │  DRAFT REPLY: ...           │
                                    └─────────────────────────────┘
```

---

## 📂 Project Structure

```
smart-support-desk/
├── notebook/
│   └── Smart_Support_Desk.ipynb   # Full working notebook
├── data/
│   └── sample_policies.json       # Sample company knowledge base
├── .env.example                   # Template for your API key
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/smart-support-desk.git
cd smart-support-desk
```

### 2. Install dependencies
```bash
pip install openai chromadb python-dotenv
```

### 3. Set up your API key
```bash
cp .env.example .env
# Then edit .env and add your MiniCPM API key
```

`.env.example`:
```
MINICPM_KEY=your_api_key_here
```

> 🔑 Get a MiniCPM API key at [modelbest.cn](https://modelbest.cn)

### 4. Run the notebook
```bash
jupyter notebook notebook/Smart_Support_Desk.ipynb
```

---

## 📋 Sample Output

**Input email:**
> *"I bought a dress 40 days ago and never opened it. Can I return it for cash?"*

**Output:**
```
PRIORITY: Low
CATEGORY: Refund

DRAFT REPLY: Thank you for reaching out. Our refund policy covers unused items
within 30 days of purchase. However, since your purchase was 40 days ago, it
falls outside the refund window. The good news — you are within our 45-day
exchange window and can swap for a different size or color. A human agent will
review cash return options for you shortly.
```

---

## 🧩 Key Design Decisions

| Decision | Reason |
|---|---|
| ChromaDB (local) | Zero-cost, no cloud dependency, fully offline vector search |
| `n_results=1` retrieval | Focused context — avoids prompt noise for single-issue tickets |
| Structured output template | Enables downstream automation (routing, CRM logging, etc.) |
| "Escalate to human" fallback | Prevents confident wrong answers when policy doesn't match |

---

## 🔧 Tech Stack

- **[ChromaDB](https://www.trychroma.com/)** — local vector database for policy retrieval
- **[MiniCPM-V-4.6-Thinking](https://modelbest.cn)** — lightweight LLM for response generation
- **[OpenAI Python SDK](https://github.com/openai/openai-python)** — used as the API client (OpenAI-compatible endpoint)
- **Python** · **Jupyter Notebook** · **python-dotenv**

---

## 💡 Potential Extensions

- [ ] Wrap as a **FastAPI** microservice (`POST /ticket` → structured JSON response)
- [ ] Add a **Streamlit** UI for manual ticket testing
- [ ] Expand the knowledge base with real policy documents (PDF ingestion)
- [ ] Increase `n_results` to retrieve multiple policies for complex edge cases
- [ ] Log outputs to a database for analytics and model improvement

---

## 👤 Author

**Sachin Jha** — Data Analyst & AI Engineer  
[LinkedIn](https://linkedin.com/in/sachin-jha-74b4a679) · [GitHub](https://github.com/Sachinjha369)

---

## 📄 License

MIT License — free to use, modify, and build on.
