# ResearchMind · Autonomous Multi-Agent AI Research System

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-orange?logo=github)](https://github.com/Suhana-Pendhari/multi-agent-researcher)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain%20%2F%20LangGraph-1C3C3C)](https://langchain.com)

**ResearchMind** is an autonomous multi-agent research assistant designed to conduct deep, factual, end-to-end research on any topic. By coordinating a team of specialized AI agents, the system autonomously searches the live web, extracts full-text webpage data, synthesizes structured executive reports, critiques output quality, and exports publication-ready deliverables.

🔗 **Repository:** [https://github.com/Suhana-Pendhari/multi-agent-researcher](https://github.com/Suhana-Pendhari/multi-agent-researcher)

---

## 📌 Project Overview

ResearchMind automates the labor-intensive academic and market research workflow. Given a research topic, four specialized AI agents collaborate sequentially to deliver verified findings:

```
[ User Query / Topic ]
          │
          ▼
┌────────────────────────────────────────────────────────┐
│ 01. Search Agent (Tavily AI Search)                   │
│ • Discovers high-signal, up-to-date web resources      │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 02. Reader Agent (Requests + BeautifulSoup)           │
│ • Scrapes, cleans, and extracts deep DOM content       │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 03. Writer Chain (LLM + LCEL)                         │
│ • Synthesizes structured reports with data tables      │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 04. Critic Chain (LLM Quality Evaluator)              │
│ • Reviews, scores (X/10), and provides constructive gaps│
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
       [ Export as PDF (.pdf) & Markdown (.md) ]
```

---

## ✨ Features

- **Autonomous Multi-Agent Pipeline:** Seamless orchestration between discovery, content scraping, report writing, and peer review.
- **Live Web Grounding:** Uses the Tavily Search API and DOM parsing to eliminate hallucination and guarantee up-to-date facts.
- **Structured Executive Synthesis:** Generates comprehensive reports complete with introductions, structured key findings tables, policy implications, and source URLs.
- **Unbiased Critic Review:** Built-in reviewer agent that grades the report, outlines key strengths, identifies gaps, and gives an objective verdict.
- **Dual Format Export:** One-click instant download of research deliverables in both publication-grade **PDF format** (with custom headers, footers, pagination, and typography) and raw **Markdown (.md)**.
- **Modern Dark-Mode UI:** Glassmorphic Streamlit interface featuring animated step cards, real-time pipeline status trackers, and collapsible inspection panels.

---

## 🛠️ Tech Stack

| Domain | Technology / Library | Role in System |
| :--- | :--- | :--- |
| **Agent Framework** | [LangChain](https://www.langchain.com/) & [LangGraph](https://www.langchain.com/langgraph) | Agent tool-binding, LCEL chains, and state management |
| **LLM Backends** | [Groq](https://groq.com/) & [Google Gemini](https://ai.google.dev/) | High-speed inference for Writer and Critic evaluation chains |
| **Search Engine** | [Tavily Search API](https://tavily.com/) | Real-time, AI-ranked search snippet discovery |
| **Web Scraping** | `BeautifulSoup4`, `Requests`, `lxml` | HTTP document retrieval and clean DOM text extraction |
| **User Interface** | [Streamlit](https://streamlit.io/) | Glassmorphic dark dashboard with real-time pipeline tracking |
| **PDF Generation** | `fpdf2` | Production PDF document generation with custom layout & fonts |
| **Resilience & Tuning** | `Tenacity`, `python-dotenv` | Exponential backoff, rate-limit retry logic, and secret management |

---

## 📸 Outputs & Visual Showcase

### 1. ResearchMind Dashboard & Real-Time Pipeline
The modern glassmorphic dashboard allows users to submit research queries with quick-select topics while tracking pipeline progress across all four autonomous agents in real time.

![ResearchMind Dashboard](Assets/Screenshot%20(830).png)

---

### 2. Synthesized Research Report
The Writer agent synthesizes scraped web context into a clean, structured report featuring executive summaries, introductions, and section-by-section breakdowns.

![Report Overview](Assets/Screenshot%20(831).png)

---

### 3. Detailed Key Findings & Comparative Data Tables
Complex data and industry projections (e.g., employment impacts, labor exposure, skill shifts) are automatically organized into structured comparative tables with supporting evidence.

![Key Findings Table](Assets/Screenshot%20(832).png)

---

### 4. Strategic Conclusions & Verified Sources
Reports conclude with policy implications, actionable next steps, and hyperlinked references for complete transparency and citation integrity.

![Conclusions and Sources](Assets/Screenshot%20(833).png)

---

### 5. Critic Review & Quality Assessment
The Critic agent evaluates the generated report against rigorous academic standards, providing an overall quality score, verified strengths, and specific areas for refinement.

![Critic Review](Assets/Screenshot%20(834).png)

---

### 6. Export & Download Report (PDF & Markdown)
Once research and critique are finalized, users can immediately download the complete research dossier as a publication-ready PDF or formatted Markdown file.

![Export and Download](Assets/Screenshot%20(835).png)
