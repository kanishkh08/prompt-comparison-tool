"""Simple rule-based scoring so the comparison works even without an API."""
import re


def _bullets(text):
    return [l for l in text.splitlines() if re.match(r"\s*([-*•]|\d+[.)])\s+", l)]


def _has_table(text):
    return any("|" in l for l in text.splitlines()) and bool(re.search(r"\|\s*:?-{3,}", text))


def evaluate(text: str, checks: dict):
    """Returns (list of (check, passed, detail), score 0-100)."""
    results = []
    words = len(text.split())
    if "max_words" in checks:
        ok = words <= checks["max_words"]
        results.append(("Word limit", ok, f"{words} words (limit {checks['max_words']})"))
    if "bullets" in checks:
        n = len(_bullets(text))
        results.append(("Bullet count", n == checks["bullets"], f"{n} bullets (needed {checks['bullets']})"))
    if checks.get("table"):
        ok = _has_table(text)
        results.append(("Table format", ok, "table found" if ok else "no table"))
    if checks.get("code_block"):
        ok = "```" in text
        results.append(("Code block", ok, "code block found" if ok else "no code block"))
    if checks.get("subject_line"):
        ok = text.lstrip().lower().startswith("subject:")
        results.append(("Subject line", ok, "present" if ok else "missing"))
    if checks.get("no_intro"):
        first = text.strip().split("\n")[0].lower()
        bad = first.startswith(("sure", "certainly", "of course", "great", "here is", "here's"))
        results.append(("No filler intro", not bad, "clean start" if not bad else "starts with filler"))
    score = round(100 * sum(r[1] for r in results) / len(results)) if results else 0
    return results, score


def verdict(basic_text, improved_text, checks):
    b_res, b_score = evaluate(basic_text, checks)
    i_res, i_score = evaluate(improved_text, checks)
    if i_score > b_score:
        winner = "Improved prompt"
    elif i_score < b_score:
        winner = "Basic prompt"
    else:
        winner = "Tie"
    reasons = [f"{n}: improved -> {d}" for (n, ok, d), (_, bok, _) in zip(i_res, b_res)
               if ok and not bok]
    explanation = (f"{winner} works better (score: basic {b_score}/100, improved {i_score}/100). "
                   + ("It followed these requirements that the basic prompt missed: "
                      + "; ".join(reasons) + "." if reasons else ""))
    return winner, b_score, i_score, explanation, b_res, i_res
