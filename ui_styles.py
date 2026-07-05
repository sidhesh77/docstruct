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

/* ── Landing page ── */
.landing-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0 2rem 0;
    border-bottom: 1px solid rgba(99, 102, 241, 0.12);
    margin-bottom: 0;
}

.landing-logo {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e2e8f0;
}

.landing-logo span { color: #818cf8; }

.landing-hero {
    text-align: center;
    padding: 4rem 1rem 3rem;
    max-width: 820px;
    margin: 0 auto;
}

.landing-hero .tag {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 1.5rem;
}

.landing-hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 1.25rem 0;
    background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 50%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.landing-hero .subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    line-height: 1.7;
    margin: 0 auto 2rem;
    max-width: 640px;
}

.landing-stats {
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin: 2.5rem 0;
    flex-wrap: wrap;
}

.landing-stat .num {
    font-size: 2rem;
    font-weight: 800;
    color: #a5b4fc;
}

.landing-stat .lbl {
    font-size: 0.8rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.section-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
}

.section-sub {
    text-align: center;
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.feature-card {
    background: linear-gradient(160deg, #151d32, #1a2440);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 1.75rem;
    height: 100%;
    transition: border-color 0.2s, transform 0.2s;
}

.feature-card:hover {
    border-color: rgba(99, 102, 241, 0.45);
    transform: translateY(-3px);
}

.feature-card .icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
}

.feature-card h3 {
    color: #e2e8f0;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
}

.feature-card p {
    color: #94a3b8;
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0;
}

.how-step {
    text-align: center;
    padding: 1.5rem 1rem;
}

.how-step .step-num {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.1rem;
    color: white;
    margin-bottom: 1rem;
}

.how-step h4 {
    color: #e2e8f0;
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 0.4rem 0;
}

.how-step p {
    color: #64748b;
    font-size: 0.85rem;
    line-height: 1.5;
    margin: 0;
}

.tech-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.6rem;
    margin-top: 1rem;
}

.tech-chip {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.25);
    color: #c7d2fe;
    padding: 0.5rem 1.1rem;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 500;
}

.cta-box {
    background: linear-gradient(135deg, #1e1b4b, #312e81, #4338ca);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 24px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 3rem 0 2rem;
}

.cta-box h2 {
    color: #ffffff;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 0.75rem 0;
}

.cta-box p {
    color: #c7d2fe;
    font-size: 1rem;
    margin: 0 0 0.5rem 0;
}

.landing-footer {
    text-align: center;
    color: #475569;
    font-size: 0.8rem;
    padding: 2rem 0 1rem;
    border-top: 1px solid rgba(99, 102, 241, 0.1);
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