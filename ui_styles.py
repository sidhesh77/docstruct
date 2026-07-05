"""Shared UI styles and helpers for DocStruct."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 45%, #4338ca 100%);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.45);
}

.hero h1 {
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(90deg, #ffffff, #c7d2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #c7d2fe;
    font-size: 1.05rem;
    margin: 0;
}

.stat-card {
    background: linear-gradient(145deg, #151d32, #1a2440);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.stat-card .value {
    font-size: 2rem;
    font-weight: 700;
    color: #a5b4fc;
    line-height: 1.2;
}

.stat-card .label {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.pipeline-step {
    background: #151d32;
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.pipeline-step.active {
    border-color: #6366f1;
    background: rgba(99, 102, 241, 0.12);
}

.pipeline-step.done {
    border-color: #22c55e;
    background: rgba(34, 197, 94, 0.1);
}

.auth-box {
    max-width: 440px;
    margin: 2rem auto;
    background: linear-gradient(160deg, #151d32, #1a2440);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
}

.auth-logo {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.auth-title {
    text-align: center;
    font-size: 1.75rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.25rem;
}

.auth-subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

.badge-ai { background: rgba(99, 102, 241, 0.2); color: #a5b4fc; }
.badge-demo { background: rgba(251, 191, 36, 0.15); color: #fcd34d; }
.badge-pass { background: rgba(34, 197, 94, 0.15); color: #86efac; }
.badge-fail { background: rgba(239, 68, 68, 0.15); color: #fca5a5; }

.feature-pill {
    display: inline-block;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    color: #c7d2fe;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.8rem;
    margin: 0.2rem;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #151d32);
    border-right: 1px solid rgba(99, 102, 241, 0.15);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
}

.stDownloadButton > button {
    border-radius: 10px;
    border-color: rgba(99, 102, 241, 0.4);
}
</style>
"""


def inject_styles() -> None:
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str) -> None:
    import streamlit as st

    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(value: str, label: str) -> None:
    import streamlit as st

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="value">{value}</div>
            <div class="label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )