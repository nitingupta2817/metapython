import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import html as html_lib

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MetaScan · SEO Inspector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Syne:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Mono', monospace;
        background-color: #0a0b0e;
        color: #c9cdd6;
    }

    .stApp {
        background: #0a0b0e;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        padding: 2.5rem 3rem 4rem;
        max-width: 1200px;
    }

    .hero {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        padding: 2.8rem 0 1.6rem;
        border-bottom: 1px solid #1e2130;
        margin-bottom: 2.4rem;
    }

    .hero-icon {
        font-size: 2.8rem;
        filter: drop-shadow(0 0 14px #3b82f680);
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #f0f2f7;
        margin: 0;
        line-height: 1;
    }

    .hero-title span {
        color: #3b82f6;
    }

    .hero-sub {
        font-size: 0.72rem;
        color: #555c72;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-top: 0.35rem;
    }

    .stTextArea textarea {
        background: #0f1117 !important;
        border: 1px solid #1e2130 !important;
        border-radius: 6px !important;
        color: #c9cdd6 !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.82rem !important;
        padding: 0.9rem 1rem !important;
        resize: vertical;
    }

    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px #3b82f620 !important;
    }

    label[data-testid="stWidgetLabel"] {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #555c72 !important;
        margin-bottom: 0.4rem;
    }

    .stButton > button {
        background: #3b82f6 !important;
        color: #fff !important;
        border: none !important;
        border-radius: 5px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 0.55rem 1.6rem !important;
    }

    .stButton > button:hover {
        background: #2563eb !important;
        box-shadow: 0 0 18px #3b82f640 !important;
    }

    .stDownloadButton > button {
        background: transparent !important;
        border: 1px solid #3b82f660 !important;
        color: #3b82f6 !important;
        border-radius: 5px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.74rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        padding: 0.5rem 1.4rem !important;
    }

    .stDownloadButton > button:hover {
        background: #3b82f610 !important;
        border-color: #3b82f6 !important;
    }

    .url-box {
        background: #0f1117;
        border: 1px solid #1e2130;
        border-radius: 8px;
        padding: 1rem 1.3rem;
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 2.2rem;
        word-break: break-all;
    }

    .meta-card {
        background: #0d0f16;
        border: 1px solid #1e2130;
        border-radius: 8px;
        padding: 1.4rem;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }

    .metric-label {
        font-size: 0.62rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #404655;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #e2e8f0;
        line-height: 1.3;
        word-break: break-word;
    }

    .metric-badge {
        display: inline-block;
        font-size: 0.62rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        letter-spacing: 0.1em;
        padding: 0.18rem 0.55rem;
        border-radius: 3px;
        margin-left: 0.5rem;
        vertical-align: middle;
    }

    .badge-good {
        background: #14532d30;
        color: #4ade80;
        border: 1px solid #4ade8040;
    }

    .badge-warn {
        background: #7c280030;
        color: #f97316;
        border: 1px solid #f9731640;
    }

    .section-title {
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #4a5270;
        font-weight: 600;
        margin-top: 1.4rem;
        margin-bottom: 0.6rem;
    }

    .error-card {
        background: #1a0a0a;
        border: 1px solid #7f1d1d50;
        border-left: 3px solid #ef4444;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        font-size: 0.78rem;
        color: #fca5a5;
        margin-top: 0.8rem;
    }

    .summary-bar {
        display: flex;
        gap: 1.2rem;
        padding: 1rem 1.4rem;
        background: #0d0f16;
        border: 1px solid #1e2130;
        border-radius: 7px;
        margin: 2rem 0 1.2rem;
        flex-wrap: wrap;
    }

    .summary-item {
        font-size: 0.72rem;
        color: #555c72;
    }

    .summary-item strong {
        color: #94a3b8;
        font-weight: 600;
    }

    .scorecard-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1.2rem;
        background: #0d0f16;
        border: 1px solid #1e2130;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
    }

    .scorecard-row.error-row {
        border-left: 3px solid #ef4444;
    }

    .sc-url {
        font-size: 0.72rem;
        color: #64748b;
        flex: 1;
        min-width: 180px;
        word-break: break-all;
    }

    .sc-score {
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        min-width: 36px;
        text-align: center;
    }

    .sc-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
    }

    .sc-chip {
        font-size: 0.62rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        letter-spacing: 0.08em;
        padding: 0.2rem 0.6rem;
        border-radius: 3px;
    }

    .chip-ok {
        background: #14532d30;
        color: #4ade80;
        border: 1px solid #4ade8040;
    }

    .chip-warn {
        background: #7c280030;
        color: #fb923c;
        border: 1px solid #fb923c40;
    }

    .chip-fail {
        background: #450a0a30;
        color: #f87171;
        border: 1px solid #f8717140;
    }

    .stDataFrame {
        border-radius: 6px;
        overflow: hidden;
    }

    [data-testid="stDataFrameResizable"] {
        border: 1px solid #1e2130 !important;
        border-radius: 6px !important;
    }

    .stProgress > div > div {
        background: #3b82f6 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem 1rem 3rem;
        }

        .hero-title {
            font-size: 2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🔍</div>
        <div>
            <div class="hero-title">Meta<span>Scan</span></div>
            <div class="hero-sub">SEO Metadata Inspector · v2.0</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Input ────────────────────────────────────────────────────────────────────
url_input = st.text_area(
    "Target URLs",
    placeholder="https://example.com  https://another-site.com",
    height=90,
)

col_btn, col_tip = st.columns([1, 5])

with col_btn:
    run = st.button("⚡  Scan URLs")

with col_tip:
    st.caption("Separate multiple URLs with spaces or newlines")


# ── Helpers ──────────────────────────────────────────────────────────────────
def normalize_url(url):
    url = url.strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def error_result(message):
    return {
        "title": "",
        "title_len": None,
        "description": "",
        "desc_len": None,
        "h1_texts": [],
        "h2_texts": [],
        "error": message,
    }


def get_meta_data(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        response = requests.get(
            url,
            timeout=15,
            headers=headers,
            allow_redirects=True,
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.content, "lxml")
        page_text = soup.get_text(" ", strip=True).lower()

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        title = title or "No title found"
        title_len = len(title)

        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag.get("content", "").strip() if desc_tag else ""
        description = description or "No description found"
        desc_len = len(description)

        h1_texts = [
            tag.get_text(strip=True)
            for tag in soup.find_all("h1")
            if tag.get_text(strip=True)
        ]

        h2_texts = [
            tag.get_text(strip=True)
            for tag in soup.find_all("h2")
            if tag.get_text(strip=True)
        ]

        js_warning_phrases = [
            "javascript is disabled",
            "enable javascript",
            "please enable javascript",
            "you need to enable javascript",
            "requires javascript",
            "javascript required",
        ]

        has_js_warning = any(phrase in page_text for phrase in js_warning_phrases)

        has_real_content = (
            title != "No title found"
            or description != "No description found"
            or len(h1_texts) > 0
            or len(h2_texts) > 0
        )

        if has_js_warning and not has_real_content:
            return error_result(
                "JavaScript required: This page does not expose its SEO content in raw HTML. "
                "Use Playwright or Selenium for this URL."
            )

        return {
            "title": title,
            "title_len": title_len,
            "description": description,
            "desc_len": desc_len,
            "h1_texts": h1_texts,
            "h2_texts": h2_texts,
            "error": "",
        }

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else ""

        if status_code == 403:
            return error_result(
                "403 Forbidden: This website blocked automated scanning. "
                "It may use bot protection, firewall rules, Cloudflare, or IP restrictions."
            )

        return error_result(str(e))

    except requests.exceptions.RequestException as e:
        return error_result(str(e))

    except Exception as e:
        return error_result(f"Unexpected error: {str(e)}")


def badge(length, limit):
    if length is None:
        return '<span class="metric-badge badge-warn">⚠ N/A</span>'

    if length <= limit:
        return f'<span class="metric-badge badge-good">✓ {length} chars</span>'

    return f'<span class="metric-badge badge-warn">⚠ {length} chars</span>'


def make_tag_dataframe(tags, tag_name):
    if not tags:
        return pd.DataFrame(
            {
                "No.": [],
                tag_name: [],
            }
        )

    return pd.DataFrame(
        {
            "No.": [f"{i:02d}" for i in range(1, len(tags) + 1)],
            tag_name: tags,
        }
    )


def prepare_dataframe(rows):
    df = pd.DataFrame(rows)

    numeric_cols = ["Title Length", "Description Length"]
    text_cols = [
        "URL",
        "Meta Title",
        "Meta Description",
        "H1 Tags",
        "H2 Tags",
        "Error",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in text_cols:
        df[col] = df[col].fillna("").astype(str)

    return df


def render_meta_card(title, title_len, description, desc_len):
    safe_title = html_lib.escape(title)
    safe_description = html_lib.escape(description)

    st.markdown(
        f"""
        <div class="meta-card">
            <div class="metric-label">Meta Title {badge(title_len, 60)}</div>
            <div class="metric-value">{safe_title}</div>
            <br>
            <div class="metric-label">Meta Description {badge(desc_len, 160)}</div>
            <div class="metric-value">{safe_description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_scorecard(all_rows):
    st.markdown(
        """
        <div style="margin-top:2.8rem; margin-bottom:1rem;">
            <div style="font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700;
                        color:#f0f2f7; letter-spacing:-0.01em;">SEO Scorecard</div>
            <div style="font-size:0.63rem; letter-spacing:0.14em; text-transform:uppercase;
                        color:#404655; margin-top:0.25rem;">Per-URL audit · 4 checks</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="display:flex;gap:1rem;margin-bottom:1rem;flex-wrap:wrap;">
            <span class="sc-chip chip-ok" style="font-size:0.63rem;">✓ Pass</span>
            <span class="sc-chip chip-warn" style="font-size:0.63rem;">⚠ Too long</span>
            <span class="sc-chip chip-fail" style="font-size:0.63rem;">✗ Missing / Error</span>
            <span style="font-size:0.63rem;color:#404655;align-self:center;">
                Title ≤60ch &nbsp;·&nbsp; Desc ≤160ch &nbsp;·&nbsp; Exactly 1 H1 &nbsp;·&nbsp; H2s present
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for row in all_rows:
        safe_url = html_lib.escape(row["URL"])

        if row["Error"]:
            st.markdown(
                f"""
                <div class="scorecard-row error-row">
                    <div class="sc-url">{safe_url}</div>
                    <div class="sc-score" style="color:#f87171;">–</div>
                    <div class="sc-chips">
                        <span class="sc-chip chip-fail">✗ Fetch Error</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            continue

        tlen = int(row["Title Length"])
        dlen = int(row["Description Length"])

        h1s = [item for item in row["H1 Tags"].split(" | ") if item.strip()]
        h2s = [item for item in row["H2 Tags"].split(" | ") if item.strip()]

        title_chip = (
            f'<span class="sc-chip chip-ok">✓ Title {tlen}ch</span>'
            if tlen <= 60
            else f'<span class="sc-chip chip-warn">⚠ Title {tlen}ch</span>'
        )

        desc_chip = (
            f'<span class="sc-chip chip-ok">✓ Desc {dlen}ch</span>'
            if dlen <= 160
            else f'<span class="sc-chip chip-warn">⚠ Desc {dlen}ch</span>'
        )

        if len(h1s) == 1:
            h1_chip = f'<span class="sc-chip chip-ok">✓ {len(h1s)} H1</span>'
        elif len(h1s) > 1:
            h1_chip = f'<span class="sc-chip chip-warn">⚠ {len(h1s)} H1s</span>'
        else:
            h1_chip = '<span class="sc-chip chip-fail">✗ No H1</span>'

        h2_chip = (
            f'<span class="sc-chip chip-ok">✓ {len(h2s)} H2s</span>'
            if len(h2s) > 0
            else '<span class="sc-chip chip-fail">✗ No H2</span>'
        )

        issues = sum(
            [
                tlen > 60,
                dlen > 160,
                len(h1s) != 1,
                len(h2s) == 0,
            ]
        )

        score = 4 - issues

        score_color = (
            "#4ade80"
            if score == 4
            else "#fb923c"
            if score >= 2
            else "#f87171"
        )

        st.markdown(
            f"""
            <div class="scorecard-row">
                <div class="sc-url">{safe_url}</div>
                <div class="sc-score" style="color:{score_color};">{score}/4</div>
                <div class="sc-chips">
                    {title_chip}
                    {desc_chip}
                    {h1_chip}
                    {h2_chip}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Scan logic ───────────────────────────────────────────────────────────────
if run and url_input.strip():
    urls = [normalize_url(u) for u in url_input.split() if normalize_url(u)]
    all_rows = []

    progress = st.progress(0)

    for i, url in enumerate(urls):
        progress.progress(i / len(urls), text=f"Scanning {i + 1}/{len(urls)}...")

        safe_url = html_lib.escape(url)

        st.markdown(
            f'<div class="url-box">Scanning: {safe_url}</div>',
            unsafe_allow_html=True,
        )

        with st.spinner("Fetching..."):
            result = get_meta_data(url)

        if result["error"]:
            safe_error = html_lib.escape(result["error"])

            st.markdown(
                f"""
                <div class="error-card">
                    <strong>Request Failed</strong><br><br>
                    {safe_error}
                </div>
                """,
                unsafe_allow_html=True,
            )

            all_rows.append(
                {
                    "URL": url,
                    "Meta Title": "",
                    "Title Length": None,
                    "Meta Description": "",
                    "Description Length": None,
                    "H1 Tags": "",
                    "H2 Tags": "",
                    "Error": result["error"],
                }
            )

            continue

        title = result["title"]
        title_len = result["title_len"]
        description = result["description"]
        desc_len = result["desc_len"]
        h1_texts = result["h1_texts"]
        h2_texts = result["h2_texts"]

        render_meta_card(title, title_len, description, desc_len)

        st.markdown(
            f'<div class="section-title">H1 Tags · {len(h1_texts)} found</div>',
            unsafe_allow_html=True,
        )

        if h1_texts:
            h1_df = make_tag_dataframe(h1_texts, "H1 Tag")
            st.dataframe(h1_df, width="stretch", hide_index=True)
        else:
            st.info("No H1 tags found")

        st.markdown(
            f'<div class="section-title">H2 Tags · {len(h2_texts)} found</div>',
            unsafe_allow_html=True,
        )

        if h2_texts:
            h2_df = make_tag_dataframe(h2_texts, "H2 Tag")
            st.dataframe(h2_df, width="stretch", hide_index=True)
        else:
            st.info("No H2 tags found")

        all_rows.append(
            {
                "URL": url,
                "Meta Title": title,
                "Title Length": title_len,
                "Meta Description": description,
                "Description Length": desc_len,
                "H1 Tags": " | ".join(h1_texts),
                "H2 Tags": " | ".join(h2_texts),
                "Error": "",
            }
        )

    progress.progress(1.0, text="Done ✓")

    # ── Summary + download ───────────────────────────────────────────────────
    if all_rows:
        success_count = sum(1 for row in all_rows if not row["Error"])
        failed_count = len(all_rows) - success_count

        st.markdown(
            f"""
            <div class="summary-bar">
                <div class="summary-item">Total&nbsp;&nbsp;<strong>{len(all_rows)}</strong></div>
                <div class="summary-item">✓ Success&nbsp;&nbsp;<strong>{success_count}</strong></div>
                <div class="summary-item">✗ Failed&nbsp;&nbsp;<strong>{failed_count}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        df = prepare_dataframe(all_rows)

        st.dataframe(df, width="stretch", hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.download_button(
            label="↓  Export CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="metascan_results.csv",
            mime="text/csv",
        )

        render_scorecard(all_rows)

elif run:
    st.error("Please enter at least one URL before scanning.")
