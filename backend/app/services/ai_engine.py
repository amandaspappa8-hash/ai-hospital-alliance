import os
from dotenv import load_dotenv

load_dotenv()


def ask_claude(prompt: str):
    try:
        import anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "Claude Error: ANTHROPIC_API_KEY missing"
        client = anthropic.Anthropic(api_key=api_key)
        res = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        out = []
        for item in res.content:
            txt = getattr(item, "text", None)
            if txt:
                out.append(txt)
        return "\n".join(out) if out else "Claude returned no text."
    except Exception as e:
        return f"Claude Error: {e}"


def ask_gemini(prompt: str):
    try:
        import google.generativeai as genai

        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Gemini Error: GOOGLE_API_KEY missing"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        res = model.generate_content(prompt)
        return getattr(res, "text", None) or "Gemini returned no text."
    except Exception as e:
        return f"Gemini Error: {e}"


def ask_ai(prompt: str, provider: str = "auto"):
    provider = (provider or "auto").lower()
    if provider == "gemini":
        return ask_gemini(prompt)
    if provider == "groq":
        return ask_ollama(prompt)
    if provider == "claude" or provider == "anthropic":
        return ask_claude(prompt)
    return ask_ollama(prompt)

def ask_groq(prompt: str):
    import os, requests
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return "Groq API key not set"
    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}
    )
    data = res.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "No response")

def ask_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    import requests
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=180
        )
        return res.json().get("response", "No response")
    except Exception as e:
        return f"Ollama error: {e}"
