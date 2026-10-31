"""Prompt Comparison and Improvement Tool  -  run with:  streamlit run app.py"""
import json
import streamlit as st
from prompt_builder import basic_prompt, improved_prompt, auto_improve
from evaluator import verdict

st.set_page_config(page_title="Prompt Comparison Tool", layout="wide")
st.title("Prompt Comparison and Improvement Tool")
st.caption("Compare a basic prompt with an improved prompt (Role + Context + Constraints + Output format).")

examples = json.load(open("examples.json", encoding="utf-8"))

with st.sidebar:
    st.header("Mode")
    mode = st.radio("Select mode", ["Demo (offline, saved outputs)", "Live (Claude API)"])
    api_key = ""
    if mode.startswith("Live"):
        api_key = st.text_input("Anthropic API key", type="password")
        st.caption("Live mode is used for the 'Your own task' tab.")


def render(task, bp, ip, bo, io, checks, explanation_extra=""):
    winner, bs, is_, expl, b_res, i_res = verdict(bo, io, checks)
    c1, c2 = st.columns(2)
    for col, title, prompt, out, score, res in (
        (c1, "Basic prompt", bp, bo, bs, b_res),
        (c2, "Improved prompt", ip, io, is_, i_res),
    ):
        with col:
            st.subheader(title)
            st.code(prompt, language="text", wrap_lines=True)
            st.markdown("**Output**")
            st.markdown(out)
            st.metric("Rule score", f"{score}/100")
            for name, ok, detail in res:
                st.write(("✅ " if ok else "❌ ") + f"{name}: {detail}")
    st.divider()
    st.subheader("Which prompt works better?")
    (st.success if winner == "Improved prompt" else st.warning)(expl)
    if explanation_extra:
        st.info(explanation_extra)


tab1, tab3, tab2 = st.tabs(["Selected examples", "Your own task (no API key)", "Your own task (API key)"])

with tab1:
    pick = st.selectbox("Choose an example", examples, format_func=lambda e: f"{e['id']}. {e['title']}")
    ip = improved_prompt(pick["task"], pick["role"], pick["context"], pick["constraints"], pick["output_format"])
    render(pick["task"], basic_prompt(pick["task"]), ip, pick["basic_output"], pick["improved_output"], pick["checks"])

with tab2:
    task = st.text_input("Enter a task", "Explain how the internet works.")
    c1, c2, c3 = st.columns(3)
    audience = c1.text_input("Audience", "a Class 9 student")
    max_words = c2.slider("Max words", 30, 300, 80)
    fmt = c3.selectbox("Output format", ["bullets", "table", "code", "paragraph"])
    if st.button("Compare prompts", type="primary"):
        if not api_key:
            st.error("Select 'Live (Claude API)' in the sidebar and enter your API key.")
        else:
            import llm
            ip, checks = auto_improve(task, audience, max_words, fmt)
            checks["no_intro"] = True
            bp = basic_prompt(task)
            try:
                with st.spinner("Asking the model..."):
                    bo, io = llm.ask(bp, api_key), llm.ask(ip, api_key)
                    extra = llm.judge(task, bo, io, api_key)
                render(task, bp, ip, bo, io, checks, "Model's explanation: " + extra)
            except Exception as e:
                st.error(f"API error: {e}")

with tab3:
    st.markdown("**Manual mode - no API key needed.** Follow the 3 steps.")
    st.markdown("**Step 1:** Write your task and choose options.")
    m_task = st.text_input("Your task", "Explain how the internet works.", key="m_task")
    m1, m2, m3 = st.columns(3)
    m_aud = m1.text_input("Audience", "a Class 9 student", key="m_aud")
    m_words = m2.slider("Max words", 30, 300, 80, key="m_words")
    m_fmt = m3.selectbox("Output format", ["bullets", "table", "code", "paragraph"], key="m_fmt")
    m_bp = basic_prompt(m_task)
    m_ip, m_checks = auto_improve(m_task, m_aud, m_words, m_fmt)
    m_checks["no_intro"] = True

    st.markdown("**Step 2:** Copy each prompt (use the copy icon), paste it in claude.ai or ChatGPT "
                "in a **new chat** each time, and copy the answer.")
    p1, p2 = st.columns(2)
    p1.markdown("Basic prompt"); p1.code(m_bp, language="text", wrap_lines=True)
    p2.markdown("Improved prompt"); p2.code(m_ip, language="text", wrap_lines=True)

    st.markdown("**Step 3:** Paste both answers here and press Compare.")
    a1, a2 = st.columns(2)
    m_bo = a1.text_area("Answer to BASIC prompt", height=250, key="m_bo")
    m_io = a2.text_area("Answer to IMPROVED prompt", height=250, key="m_io")
    if st.button("Compare answers", type="primary", key="m_btn"):
        if not m_bo.strip() or not m_io.strip():
            st.error("Please paste both answers first.")
        else:
            render(m_task, m_bp, m_ip, m_bo, m_io, m_checks)
