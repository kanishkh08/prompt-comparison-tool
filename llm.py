"""LLM access. Live mode uses the Anthropic API; demo mode uses saved outputs."""
import os

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")


def ask(prompt: str, api_key: str = "") -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
    msg = client.messages.create(model=MODEL, max_tokens=1000,
                                 messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in msg.content if b.type == "text")


def judge(task, basic_out, improved_out, api_key: str = "") -> str:
    """Optional: ask the model to explain which output is better."""
    p = (f"Task: {task}\n\nOutput A (basic prompt):\n{basic_out}\n\n"
         f"Output B (improved prompt):\n{improved_out}\n\n"
         "In 3 short sentences, say which output is better and why "
         "(clarity, relevance, format, length control).")
    return ask(p, api_key)
