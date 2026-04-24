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
            messages=[{"role": "user", "content": prompt}]
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
    if provider == "claude":
        return ask_claude(prompt)
    if provider == "gemini":
        return ask_gemini(prompt)
    return ask_gemini(prompt)
