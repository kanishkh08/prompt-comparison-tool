# Prompt Comparison and Improvement Tool

A small app that takes a task, builds a **basic prompt** and an **improved prompt**
(Role + Context + Constraints + Output format), shows both outputs side by side,
and explains which prompt works better.

## Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit web app (main) |
| `cli.py` | Command-line version |
| `prompt_builder.py` | Builds basic and improved prompts |
| `evaluator.py` | Rule-based scoring (word limit, bullets, table, code block, subject line, no filler intro) and verdict |
| `llm.py` | Claude API calls (live mode) + optional AI judge |
| `examples.json` | 5 selected examples with prompts and saved outputs |
| `REPORT.md` | Short project report |

## Setup
```
pip install -r requirements.txt
```

## Run
**Web app (demo mode works with no API key):**
```
streamlit run app.py
```
- Tab 1 "Selected examples": 5 ready examples with saved outputs.
- Tab 2 "Your own task (no API key)": the app makes both prompts; you paste them into claude.ai/ChatGPT, paste the answers back, and the app scores them.
- Tab 3 "Your own task (API key)": choose *Live* mode in the sidebar, paste your Anthropic API key.

**Command line:**
```
python cli.py --example 1                       # offline demo (1-5)
python cli.py --task "Explain gravity" --audience "Class 6 students" --format bullets   # live, needs ANTHROPIC_API_KEY
```

## How the comparison works
1. Basic prompt = the task as typed.
2. Improved prompt = Role + Context + Task + Constraints + Output format.
3. Both are sent to the model (live) or loaded from `examples.json` (demo).
4. `evaluator.py` checks each output against the constraints and gives a score out of 100.
5. The higher score wins; the explanation lists which requirements the basic prompt missed.
   In live mode the model also writes its own short explanation.
