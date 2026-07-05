"""
DocStruct — AI-Powered KYC Document Intelligence Platform

Run: streamlit run app.py
Demo login: demo / demo123
"""

import json
import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Streamlit Cloud / hosted deploy: load secrets into env
try:
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

from auth import authenticate, get_user_stats, init_db, register_user, save_extraction
from extract_json import extract_kyc_data
from extract_text import extract_text_from_pdf, extract_text_from_txt
from ui_styles import inject_styles, render_hero, render_stat_card
from validate_data import check_all_fields

# ----- Init -----
init_db()

st.set_page_config(
    page_title="DocStruct | Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

# ----- Session state -----
defaults = {
    "authenticated": False,
    "user": None,
    "used_sample": False,
    "page": "extract",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.used_sample = False
    st.session_state.page = "extract"
    st.rerun()


def show_login_page() -> None:
    st.markdown(
        """
        <div class="auth-logo">📄</div>
        <div class="auth-title">DocStruct</div>
        <div class="auth-subtitle">AI-Powered KYC Document Intelligence</div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_register = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="demo")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

            if submitted:
                ok, user, msg = authenticate(username, password)
                if ok:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(msg)

        st.info("**Demo account:** username `demo` · password `demo123`")

    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input("Username", key="reg_user")
            new_email = st.text_input("Email", key="reg_email")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            new_pass2 = st.text_input("Confirm Password", type="password", key="reg_pass2")
            reg_submit = st.form_submit_button("Create Account", use_container_width=True)

            if reg_submit:
                if new_pass != new_pass2:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(new_user, new_email, new_pass)
                    st.success(msg) if ok else st.error(msg)

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align:center; color:#64748b; font-size:0.85rem;">
        <span class="feature-pill">Gemini AI</span>
        <span class="feature-pill">PDF Extraction</span>
        <span class="feature-pill">Field Validation</span>
        <span class="feature-pill">Secure Auth</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    user = st.session_state.user
    with st.sidebar:
        st.markdown(f"### 👤 {user['username']}")
        st.caption(user["email"])
        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Extract", "Dashboard", "About"],
            index=["extract", "dashboard", "about"].index(st.session_state.page),
            label_visibility="collapsed",
        )
        st.session_state.page = page.lower()

        st.markdown("---")
        st.markdown("**Settings**")
        st.session_state.use_ai = st.checkbox(
            "Use Gemini AI",
            value=st.session_state.get("use_ai", True),
            help="Uncheck for rule-based demo parser (no API key needed)",
        )

        if st.session_state.use_ai:
            has_key = bool(os.getenv("GEMINI_API_KEY", "").strip()) and os.getenv(
                "GEMINI_API_KEY"
            ) != "your_api_key_here"
            if has_key:
                st.success("Gemini API connected")
            else:
                st.warning("No API key — demo mode")
        else:
            st.info("Demo parser active")

        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            logout()


def render_pipeline_step(step_num: int, label: str, status: str) -> None:
    css_class = "pipeline-step"
    if status == "active":
        css_class += " active"
    elif status == "done":
        css_class += " done"
    icon = "⏳" if status == "active" else ("✅" if status == "done" else "○")
    st.markdown(
        f'<div class="{css_class}">{icon}<br><strong>Step {step_num}</strong><br>{label}</div>',
        unsafe_allow_html=True,
    )


def render_extract_page() -> None:
    render_hero(
        "Document Extraction",
        "Upload KYC documents → AI structuring → validated JSON output",
    )

    uploaded_file = st.file_uploader(
        "Upload KYC document (PDF or TXT)",
        type=["pdf", "txt"],
        help="Supports text-based PDFs and plain text files",
    )

    col_a, col_b, _ = st.columns([1, 1, 2])
    with col_a:
        if st.button("Try sample document", use_container_width=True, type="primary"):
            sample_path = os.path.join(os.path.dirname(__file__), "samples", "sample_kyc.txt")
            with open(sample_path, "r", encoding="utf-8") as f:
                st.session_state.sample_text = f.read()
            st.session_state.used_sample = True
            st.rerun()
    with col_b:
        if st.button("Clear", use_container_width=True):
            st.session_state.used_sample = False
            st.session_state.pop("sample_text", None)
            st.rerun()

    if not uploaded_file and not st.session_state.used_sample:
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**1. Upload**")
            st.caption("Drop a PDF or TXT KYC form")
        with c2:
            st.markdown("**2. Extract**")
            st.caption("Gemini AI or rule-based parser")
        with c3:
            st.markdown("**3. Validate**")
            st.caption("PAN, phone, date & address checks")
        return

    # Pipeline indicators
    p1, p2, p3 = st.columns(3)
    with p1:
        render_pipeline_step(1, "Read Document", "active")
    with p2:
        render_pipeline_step(2, "Extract JSON", "active")
    with p3:
        render_pipeline_step(3, "Validate", "active")

    with st.spinner("Step 1/3: Reading document..."):
        if st.session_state.used_sample and not uploaded_file:
            raw_text = st.session_state.get("sample_text", "")
            file_label = "sample_kyc.txt"
        else:
            st.session_state.used_sample = False
            file_label = uploaded_file.name
            suffix = ".pdf" if uploaded_file.name.lower().endswith(".pdf") else ".txt"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            try:
                raw_text = (
                    extract_text_from_pdf(tmp_path)
                    if suffix == ".pdf"
                    else extract_text_from_txt(tmp_path)
                )
            finally:
                os.unlink(tmp_path)

    with p1:
        render_pipeline_step(1, "Read Document", "done")

    if not raw_text:
        st.error("Could not read text. Try a text-based PDF or upload a .txt file.")
        return

    with st.spinner("Step 2/3: Converting to structured JSON..."):
        try:
            data, mode = extract_kyc_data(raw_text, use_ai=st.session_state.use_ai)
        except Exception as error:
            st.error(f"Extraction failed: {error}")
            return

    with p2:
        render_pipeline_step(2, "Extract JSON", "done")

    badge = "badge-ai" if mode == "gemini" else "badge-demo"
    mode_label = "Gemini AI" if mode == "gemini" else "Demo Parser"
    st.markdown(
        f'Processed <strong>{file_label}</strong> · '
        f'<span class="badge {badge}">{mode_label}</span>',
        unsafe_allow_html=True,
    )

    with st.spinner("Step 3/3: Validating fields..."):
        report = check_all_fields(data)

    with p3:
        render_pipeline_step(3, "Validate", "done")

    ok_count = sum(1 for r in report.values() if r["ok"])
    total = len(report)
    score = f"{ok_count}/{total}"

    user_id = st.session_state.user["id"]
    save_extraction(
        user_id,
        file_label,
        json.dumps(data, indent=2),
        score,
        mode,
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_stat_card(str(ok_count), "Fields Passed")
    with m2:
        render_stat_card(str(total - ok_count), "Fields Failed")
    with m3:
        render_stat_card(f"{int(ok_count / total * 100)}%", "Accuracy")
    with m4:
        render_stat_card(mode_label, "Engine")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Extracted JSON")
        st.json(data)
        st.download_button(
            label="Download JSON",
            data=json.dumps(data, indent=2),
            file_name="kyc_data.json",
            mime="application/json",
            use_container_width=True,
        )

    with col_right:
        st.subheader("Validation Report")
        for field_name, result in report.items():
            badge_cls = "badge-pass" if result["ok"] else "badge-fail"
            status = "PASS" if result["ok"] else "FAIL"
            st.markdown(
                f'<span class="badge {badge_cls}">{status}</span> '
                f"**{field_name.replace('_', ' ').title()}**: "
                f"{result['value'] or '(empty)'}",
                unsafe_allow_html=True,
            )
            if not result["ok"]:
                st.caption(result["message"])

    with st.expander("View raw extracted text"):
        st.text(raw_text)


def render_dashboard_page() -> None:
    render_hero("Dashboard", "Your extraction history and activity overview")

    stats = get_user_stats(st.session_state.user["id"])

    c1, c2, c3 = st.columns(3)
    with c1:
        render_stat_card(str(stats["total_extractions"]), "Total Extractions")
    with c2:
        render_stat_card(st.session_state.user["username"], "Active User")
    with c3:
        ai_status = "Enabled" if st.session_state.get("use_ai", True) else "Demo"
        render_stat_card(ai_status, "AI Mode")

    st.markdown("---")
    st.subheader("Recent Activity")

    if not stats["recent"]:
        st.info("No extractions yet. Go to **Extract** and process a document.")
        return

    for item in stats["recent"]:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{item['filename']}**")
                st.caption(item["created_at"][:19].replace("T", " "))
            with col2:
                badge = "badge-ai" if item["extraction_mode"] == "gemini" else "badge-demo"
                st.markdown(
                    f'<span class="badge {badge}">{item["extraction_mode"]}</span>',
                    unsafe_allow_html=True,
                )
            with col3:
                st.markdown(
                    f'<span class="badge badge-pass">{item["validation_score"]} passed</span>',
                    unsafe_allow_html=True,
                )


def render_about_page() -> None:
    render_hero(
        "DocStruct",
        "Enterprise-grade document intelligence for KYC automation",
    )

    st.markdown(
        """
        ### Problem
        Manual data entry from KYC forms is slow, error-prone, and doesn't scale.

        ### Solution
        An end-to-end pipeline: **document upload → text extraction → AI structuring → validation → export**.

        ### Tech Stack
        | Layer | Technology |
        |-------|------------|
        | Frontend | Streamlit, Custom CSS |
        | Auth | SQLite, bcrypt |
        | AI | Google Gemini 2.0 Flash |
        | Extraction | pdfplumber |
        | Validation | Custom rule engine (PAN, phone, date) |
        """
    )

    st.markdown("---")
    st.markdown("### Architecture")
    st.code(
        """
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   Upload    │───▶│ Extract Text │───▶│  AI / Demo  │───▶│  Validate    │
│  PDF / TXT  │    │  pdfplumber  │    │   Parser    │    │  Rule Engine │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                                                                │
                                                                ▼
                                                         ┌──────────────┐
                                                         │ JSON Export  │
                                                         │  + History   │
                                                         └──────────────┘
        """,
        language="text",
    )

    st.markdown("---")
    st.markdown(
        """
        ### Resume Bullet
        > Built **DocStruct**, an AI-powered document intelligence platform that automates
        > KYC data extraction from PDFs into validated JSON — featuring secure authentication,
        > Gemini AI integration, and a full validation pipeline. Reduced manual data entry
        > time by automating field extraction and compliance checks.
        """
    )


# ----- Main routing -----
if not st.session_state.authenticated:
    show_login_page()
else:
    render_sidebar()

    if st.session_state.page == "extract":
        render_extract_page()
    elif st.session_state.page == "dashboard":
        render_dashboard_page()
    else:
        render_about_page()