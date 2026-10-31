"""Builds the basic and the improved prompt for a given task."""


def basic_prompt(task: str) -> str:
    """Basic prompt = just the bare task."""
    return task.strip()


def improved_prompt(task: str, role: str, context: str,
                    constraints: list, output_format: str) -> str:
    """Improved prompt = Role + Context + Task + Constraints + Output format."""
    lines = [
        f"Role: You are {role}.",
        f"Context: {context}",
        f"Task: {task.strip()}",
        "Constraints:",
    ]
    lines += [f"- {c}" for c in constraints]
    lines.append(f"Output format: {output_format}")
    return "\n".join(lines)


FORMAT_TEXT = {
    "bullets": "Use bullet points only (one point per line, starting with '-').",
    "table": "Give the answer as a Markdown table.",
    "code": "Give the code inside a fenced code block, followed by a short explanation.",
    "paragraph": "Write in short plain paragraphs, no bullet points.",
}


def auto_improve(task: str, audience: str, max_words: int, fmt: str,
                 bullet_count: int = 0):
    """Builds an improved prompt for a custom task entered in the UI.
    Returns (prompt, checks) where checks is used by the evaluator."""
    constraints = [f"Keep the answer under {max_words} words.",
                   f"Write for {audience}; use simple, clear language.",
                   "Do not add an introduction or a conclusion."]
    checks = {"max_words": max_words}
    if fmt == "bullets":
        n = bullet_count or 4
        constraints.append(f"Use exactly {n} bullet points.")
        checks["bullets"] = n
    elif fmt == "table":
        checks["table"] = True
    elif fmt == "code":
        checks["code_block"] = True
    prompt = improved_prompt(
        task=task,
        role="an expert teacher and communicator in this topic",
        context=f"The answer is for {audience}.",
        constraints=constraints,
        output_format=FORMAT_TEXT[fmt],
    )
    return prompt, checks
