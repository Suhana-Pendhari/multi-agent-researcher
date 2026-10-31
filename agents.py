from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import os
import re
import time

load_dotenv()

GROQ_MODELS = (
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.1-8b-instant",
)
GEMINI_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
)


def clip_text(text, limit: int = 3200) -> str:
    text = str(text or "")
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n[Truncated to stay within model rate limits.]"


def is_rate_limit_error(err: Exception) -> bool:
    text = str(err).lower()
    return "429" in text or "rate_limit" in text or "rate limit" in text


def retry_wait_seconds(err: Exception, fallback: float) -> float:
    match = re.search(r"try again in ([0-9.]+)", str(err), re.I)
    if match:
        return min(25.0, float(match.group(1)) + 1.25)
    return fallback


def invoke_with_retry(runnable, payload, attempts: int = 5, on_wait=None):
    delay = 3.0
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return runnable.invoke(payload)
        except Exception as err:
            last_error = err
            if not is_rate_limit_error(err) or attempt == attempts:
                raise
            wait = retry_wait_seconds(err, delay)
            if on_wait:
                on_wait(wait, attempt, attempts)
            time.sleep(wait)
            delay = min(delay * 1.8, 20)
    raise last_error


def get_llm():
    errors = []

    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        for model_name in GROQ_MODELS:
            try:
                llm = ChatGroq(
                    model=model_name,
                    temperature=0,
                    api_key=groq_key,
                    max_tokens=1200,
                )
                print(f"LLM initialized successfully: ChatGroq ({model_name})")
                return llm
            except Exception as e:
                errors.append(f"Groq/{model_name}: {e}")

    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        os.environ["GOOGLE_API_KEY"] = google_key
        for model_name in GEMINI_MODELS:
            try:
                llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
                print(f"LLM initialized successfully: ChatGoogleGenerativeAI ({model_name})")
                return llm
            except Exception as e:
                errors.append(f"Gemini/{model_name}: {e}")

    detail = "\n".join(errors) if errors else "No GROQ_API_KEY or GOOGLE_API_KEY found."
    raise ValueError(
        "Could not initialize an LLM. Set GROQ_API_KEY or GOOGLE_API_KEY in .env.\n"
        + detail
    )


def extract_text(result) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    messages = result.get("messages") if isinstance(result, dict) else None
    if messages:
        content = getattr(messages[-1], "content", messages[-1])
    else:
        content = getattr(result, "content", result)
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(str(block.get("text") or block.get("content") or ""))
            else:
                parts.append(str(getattr(block, "text", block)))
        return "\n".join(p for p in parts if p)
    return str(content or "")


try:
    llm = get_llm()
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    llm = None

def _require_llm():
    if llm is None:
        raise RuntimeError(
            "No working LLM is configured. Check GROQ_API_KEY / GOOGLE_API_KEY "
            "and that the model name is available on your account."
        )
    return llm


def build_search_agent():
    return create_agent(
        model=_require_llm(),
        tools=[web_search],
        system_prompt=(
            "You are a web discovery agent. Always call the web_search tool "
            "before answering. Summarize the most relevant titles, URLs, and facts."
        ),
    )


def build_reader_agent():
    return create_agent(
        model=_require_llm(),
        tools=[scrape_url],
        system_prompt=(
            "You are a research reader. Always call scrape_url on the most relevant "
            "URL from the search results, then return the useful extracted content."
        ),
    )

#writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = (writer_prompt | llm | StrOutputParser()) if llm is not None else None

#critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_llm = llm.bind(max_tokens=450) if llm is not None else None
critic_chain = (critic_prompt | critic_llm | StrOutputParser()) if critic_llm is not None else None

