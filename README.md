# ResearchMind

ResearchMind is a multi-agent research assistant. Given a topic, it searches the live web, reads a source page, writes a structured report, and critiques that report.

It can be used from a Streamlit web UI or from the command line.

## Pipeline

1. **Search agent** — finds recent web results with Tavily
2. **Reader agent** — scrapes the most relevant URL
3. **Writer chain** — drafts a research report
4. **Critic chain** — scores the report and lists strengths and gaps

## Project layout

```
multi-agent-system/
├── app.py              # Streamlit UI
├── pipeline.py         # CLI orchestrator
├── pdf_export.py       # PDF report generation
├── agents.py           # Agents, prompts, and LLM setup
├── tools.py            # web_search and scrape_url
├── test_system.py      # Smoke tests
├── requirements.txt
├── .env                # API keys (not committed)
└── notes.txt           # Longer project notes
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

Optional fallback:

```
GOOGLE_API_KEY=your_google_key
```

Get keys from:

- Groq: https://console.groq.com/keys
- Tavily: https://tavily.com
- Google AI: https://aistudio.google.com/apikey

The app tries Groq first, then Google Gemini if Groq is not configured.

## Run the web UI

```powershell
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`), enter a topic, and click **Run Research Pipeline**. When a report is ready you can download it as Markdown or PDF.

## Run the CLI

```powershell
python pipeline.py
```

You will be prompted for a topic. Step output is printed in the terminal.

## Check that the system is ready

```powershell
python test_system.py
```

This checks API keys, imports, agent creation, and a simple LLM call.

## Notes

- Groq free-tier accounts have a low tokens-per-minute limit. The pipeline shortens long prompts and retries automatically if Groq returns HTTP 429.
- Keep `.env` private. It is already listed in `.gitignore`.
