import html
import time
import traceback

import streamlit as st
from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
    extract_text,
    clip_text,
    invoke_with_retry,
    llm,
)
from pdf_export import build_report_pdf

st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1rem;
}
.hero h1 span { color: #ff8c32; }
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #a09890;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
    color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
.stTextInput > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
}

.stDownloadButton > button,
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.8rem !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.45) !important;
}

.download-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.25);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(8px);
}
.download-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 0.4rem;
    font-weight: 500;
}
.download-desc {
    font-size: 0.88rem;
    color: #a09890;
    margin-bottom: 1.2rem;
    line-height: 1.5;
}

.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.step-card.active {
    border-color: rgba(255,140,50,0.4);
    background: rgba(255,140,50,0.04);
}
.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.7;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
}
.status-waiting { color: #555; }
.status-running { color: #ff8c32; }
.status-done    { color: #50c878; }

.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cdc8bf;
    white-space: pre-wrap;
}

.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.15);
}

.stSpinner > div { color: #ff8c32 !important; }
div[data-testid="stAlert"], .stAlert { visibility: visible !important; }

.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 2rem 0 1rem;
}

.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #605850;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


if "results" not in st.session_state:
    st.session_state.results = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "done" not in st.session_state:
    st.session_state.done = False
if "error" not in st.session_state:
    st.session_state.error = None
if "error_details" not in st.session_state:
    st.session_state.error_details = None
if "report_name" not in st.session_state:
    st.session_state.report_name = "research_report.md"

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button(
        "⚡  Run Research Pipeline",
        use_container_width=True,
        disabled=st.session_state.running,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;
            padding:0.25rem 0.7rem;
            font-size:0.75rem;
            color:#a09890;
            font-family:'DM Sans',sans-serif;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
    r = st.session_state.results

    def s(step):
        if step in r:
            return "done"
        if st.session_state.running:
            for key in ["search", "reader", "writer", "critic"]:
                if key not in r:
                    return "running" if key == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent", s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent", s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain", s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain", s("critic"), "Reviews & scores the report")


def fail_step(step_name: str, exc: Exception):
    st.session_state.error = f"{step_name} failed: {exc}"
    st.session_state.error_details = traceback.format_exc()
    st.session_state.running = False
    st.session_state.done = False
    st.rerun()


if run_btn:
    if not (topic or "").strip():
        st.warning("Please enter a research topic first.")
    elif llm is None or writer_chain is None or critic_chain is None:
        st.session_state.error = "No working LLM is configured. Check GROQ_API_KEY / GOOGLE_API_KEY in .env."
        st.session_state.error_details = None
        st.session_state.running = False
        st.session_state.done = False
    else:
        st.session_state.results = {}
        st.session_state.error = None
        st.session_state.error_details = None
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = (st.session_state.get("topic_input") or "").strip()
    progress_bar = st.progress(0, text="Initializing pipeline...")
    status_placeholder = st.empty()

    def on_wait(seconds, attempt, total):
        status_placeholder.warning(
            f"Groq rate limit reached. Waiting {seconds:.1f}s, then retrying ({attempt}/{total})..."
        )

    try:
        progress_bar.progress(25, text="Step 1/4: Searching web for information...")
        status_placeholder.info("Search Agent is gathering recent web information...")
        search_agent = build_search_agent()
        sr = invoke_with_retry(search_agent, {
            "messages": [{"role": "user", "content": f"Find recent, reliable and detailed information about: {topic_val}"}]
        }, on_wait=on_wait)
        results["search"] = extract_text(sr)
        st.session_state.results = dict(results)
    except Exception as e:
        fail_step("Search", e)

    try:
        progress_bar.progress(50, text="Step 2/4: Scraping and reading content...")
        status_placeholder.info("Reader Agent is scraping top resources for deeper content...")
        reader_agent = build_reader_agent()
        rr = invoke_with_retry(reader_agent, {
            "messages": [{"role": "user", "content":
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{clip_text(results['search'], 900)}"
            }]
        }, on_wait=on_wait)
        results["reader"] = extract_text(rr)
        st.session_state.results = dict(results)
    except Exception as e:
        fail_step("Reader", e)

    try:
        progress_bar.progress(75, text="Step 3/4: Writing research report...")
        status_placeholder.info("Writer is synthesizing the research into a structured report...")
        research_combined = (
            f"SEARCH RESULTS:\n{clip_text(results['search'], 2200)}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{clip_text(results['reader'], 2200)}"
        )
        results["writer"] = invoke_with_retry(writer_chain, {
            "topic": topic_val,
            "research": research_combined,
        }, on_wait=on_wait)
        st.session_state.results = dict(results)
    except Exception as e:
        fail_step("Writer", e)

    try:
        progress_bar.progress(90, text="Step 4/4: Reviewing and critiquing...")
        status_placeholder.info("Critic is reviewing the report for quality...")
        time.sleep(2)
        results["critic"] = invoke_with_retry(critic_chain, {
            "report": clip_text(results["writer"], 2800),
        }, on_wait=on_wait)
        st.session_state.results = dict(results)
    except Exception as e:
        fail_step("Critic", e)

    progress_bar.progress(100, text="Pipeline completed!")
    st.session_state.report_name = f"research_report_{int(time.time())}.md"
    st.session_state.running = False
    st.session_state.done = True
    st.rerun()

r = st.session_state.results

if st.session_state.error:
    st.error(st.session_state.error)
    if st.session_state.error_details:
        with st.expander("See full error details"):
            st.code(st.session_state.error_details)

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{html.escape(str(r["search"]))}</div></div>',
                unsafe_allow_html=True,
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{html.escape(str(r["reader"]))}</div></div>',
                unsafe_allow_html=True,
            )

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)

    if "writer" in r:
        st.markdown("""
        <div class="download-card">
            <div class="download-title">📥 Export & Download Report</div>
            <div class="download-desc">
                Download your complete research report and critic feedback as a publication-ready PDF or formatted Markdown document.
            </div>
        """, unsafe_allow_html=True)

        pdf_name = st.session_state.report_name.replace(".md", ".pdf")
        topic_title = (st.session_state.get("topic_input") or "Research Report").strip()

        try:
            pdf_bytes = build_report_pdf(
                topic=topic_title,
                report=r["writer"],
                feedback=r.get("critic"),
            )
        except Exception as pdf_err:
            st.error(f"Failed to generate PDF: {pdf_err}")
            pdf_bytes = None

        dl_pdf, dl_md = st.columns(2)
        with dl_pdf:
            if pdf_bytes:
                st.download_button(
                    label="📄  Download Report (.pdf)",
                    data=pdf_bytes,
                    file_name=pdf_name,
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_download_pdf",
                )
            else:
                st.button("⚠️ PDF Unavailable", disabled=True, use_container_width=True)
        with dl_md:
            st.download_button(
                label="📝  Download Report (.md)",
                data=r["writer"],
                file_name=st.session_state.report_name,
                mime="text/markdown",
                use_container_width=True,
                key="btn_download_md",
            )
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
