"""Command-line version.  Demo:  python cli.py --example 1
Live:  python cli.py --task "Explain gravity" --audience "Class 6 students"  (needs ANTHROPIC_API_KEY)"""
import argparse, json
from prompt_builder import basic_prompt, improved_prompt, auto_improve
from evaluator import verdict


def show(task, bp, ip, bo, io, checks):
    winner, bs, is_, expl, _, _ = verdict(bo, io, checks)
    line = "=" * 70
    print(f"{line}\nTASK: {task}\n{line}")
    print(f"\n[BASIC PROMPT]\n{bp}\n\n[BASIC OUTPUT]\n{bo}")
    print(f"\n{'-'*70}\n[IMPROVED PROMPT]\n{ip}\n\n[IMPROVED OUTPUT]\n{io}")
    print(f"\n{line}\nVERDICT: {expl}\n{line}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--example", type=int, help="1-5, runs offline demo")
    ap.add_argument("--task")
    ap.add_argument("--audience", default="a beginner")
    ap.add_argument("--max-words", type=int, default=80)
    ap.add_argument("--format", default="bullets", choices=["bullets", "table", "code", "paragraph"])
    a = ap.parse_args()
    if a.example:
        e = json.load(open("examples.json", encoding="utf-8"))[a.example - 1]
        ip = improved_prompt(e["task"], e["role"], e["context"], e["constraints"], e["output_format"])
        show(e["task"], basic_prompt(e["task"]), ip, e["basic_output"], e["improved_output"], e["checks"])
    elif a.task:
        import llm
        ip, checks = auto_improve(a.task, a.audience, a.max_words, a.format)
        checks["no_intro"] = True
        show(a.task, basic_prompt(a.task), ip, llm.ask(basic_prompt(a.task)), llm.ask(ip), checks)
    else:
        ap.print_help()
