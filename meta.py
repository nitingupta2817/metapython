import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import html as html_lib

st.set_page_config(
    page_title="MetaScan · SEO Inspector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

THEMES = {
    "🌙 Dark": {
        "bg":         "#0a0b0e",
        "bg2":        "#0d0f16",
        "bg3":        "#0f1117",
        "bg4":        "#111420",
        "border":     "#1e2130",
        "border2":    "#252a3d",
        "border3":    "#1a1d27",
        "text":       "#c9cdd6",
        "text2":      "#94a3b8",
        "text3":      "#555c72",
        "text4":      "#404655",
        "text5":      "#4a5270",
        "accent":     "#3b82f6",
        "accent2":    "#2563eb",
        "accent_glow":"#3b82f680",
        "accent_soft":"#3b82f620",
        "accent_bg":  "#3b82f610",
        "accent_dim": "#3b82f660",
        "h1_color":   "#bfdbfe",
        "h2_color":   "#c7d2fe",
        "title_color":"#f0f2f7",
        "num_color2": "#3d4560",
    },
    "☀️ Light": {
        "bg":         "#f0f4f8",
        "bg2":        "#ffffff",
        "bg3":        "#f8fafc",
        "bg4":        "#eef2f6",
        "border":     "#dde3ea",
        "border2":    "#c8d0da",
        "border3":    "#e4e9ef",
        "text":       "#2d3748",
        "text2":      "#4a5568",
        "text3":      "#718096",
        "text4":      "#a0aec0",
        "text5":      "#8896a8",
        "accent":     "#3b82f6",
        "accent2":    "#2563eb",
        "accent_glow":"#3b82f640",
        "accent_soft":"#3b82f615",
        "accent_bg":  "#3b82f608",
        "accent_dim": "#3b82f650",
        "h1_color":   "#1e40af",
        "h2_color":   "#3730a3",
        "title_color":"#1a202c",
        "num_color2": "#b0bec5",
    },
}

# ── Theme selector ────────────────────────────────────────────────────────────
st.sidebar.title("🎨 Theme")
selected_theme = st.sidebar.radio("Choose Theme", list(THEMES.keys()), index=0)
t = THEMES[selected_theme]

# ── Dynamic CSS ───────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Syne:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'IBM Plex Mono', monospace;
        background-color: {t['bg']};
        color: {t['text']};
    }}
    .stApp {{ background: {t['bg']}; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding: 2.5rem 3rem 4rem; max-width: 1200px; }}

    .hero {{
        display: flex; align-items: center; gap: 1.2rem;
        padding: 2.8rem 0 1.6rem;
        border-bottom: 1px solid {t['border']};
        margin-bottom: 2.4rem;
    }}
    .hero-icon {{ font-size: 2.8rem; filter: drop-shadow(0 0 14px {t['accent_glow']}); }}
    .hero-title {{
        font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 800;
        letter-spacing: -0.03em; color: {t['title_color']}; margin: 0; line-height: 1;
    }}
    .hero-title span {{ color: {t['accent']}; }}
    .hero-sub {{
        font-size: 0.72rem; color: {t['text3']}; letter-spacing: 0.14em;
        text-transform: uppercase; margin-top: 0.35rem;
    }}

    .stTextArea textarea {{
        background: {t['bg3']} !important;
        border: 1px solid {t['border']} !important;
        border-radius: 6px !important;
        color: {t['text']} !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.82rem !important;
        padding: 0.9rem 1rem !important;
        resize: vertical;
        transition: border-color 0.2s;
    }}
    .stTextArea textarea:focus {{
        border-color: {t['accent']} !important;
        box-shadow: 0 0 0 3px {t['accent_soft']} !important;
    }}
    label[data-testid="stWidgetLabel"] {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem; letter-spacing: 0.12em;
        text-transform: uppercase; color: {t['text3']} !important;
        margin-bottom: 0.4rem;
    }}

    .stButton > button {{
        background: {t['accent']} !important; color: #fff !important;
        border: none !important; border-radius: 5px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.78rem !important; font-weight: 600 !important;
        letter-spacing: 0.1em !important; text-transform: uppercase !important;
        padding: 0.55rem 1.6rem !important;
        transition: background 0.2s, box-shadow 0.2s !important;
    }}
    .stButton > button:hover {{
        background: {t['accent2']} !important;
        box-shadow: 0 0 18px {t['accent_soft']} !important;
    }}

    .stDownloadButton > button {{
        background: transparent !important;
        border: 1px solid {t['accent_dim']} !important;
        color: {t['accent']} !important; border-radius: 5px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.74rem !important; font-weight: 500 !important;
        letter-spacing: 0.1em !important; text-transform: uppercase !important;
        padding: 0.5rem 1.4rem !important; transition: all 0.2s !important;
    }}
    .stDownloadButton > button:hover {{
        background: {t['accent_bg']} !important;
        border-color: {t['accent']} !important;
    }}

    .url-header {{
        display: flex; align-items: center; gap: 0.7rem;
        padding: 1rem 1.3rem; background: {t['bg3']};
        border: 1px solid {t['border']}; border-bottom: none;
        border-radius: 8px 8px 0 0;
        font-size: 0.78rem; color: {t['text3']}; margin-top: 2.2rem;
    }}
    .url-header .dot {{
        width: 8px; height: 8px; border-radius: 50%;
        background: {t['accent']}; box-shadow: 0 0 8px {t['accent']};
    }}
    .url-header .url-text {{ color: {t['text2']}; font-weight: 500; }}

    .result-card {{
        background: {t['bg2']}; border: 1px solid {t['border']};
        border-radius: 0 0 8px 8px; padding: 1.6rem 1.8rem; margin-bottom: 0.5rem;
    }}
    .metric-row {{
        display: grid; grid-template-columns: repeat(2, 1fr);
        gap: 1rem; margin-bottom: 1.4rem;
    }}
    .metric-box {{
        background: {t['bg']}; border: 1px solid {t['border']};
        border-radius: 6px; padding: 1rem 1.2rem;
    }}
    .metric-label {{
        font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase;
        color: {t['text4']}; margin-bottom: 0.4rem;
    }}
    .metric-value {{
        font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700;
        color: {t['title_color']}; line-height: 1.3; word-break: break-word;
    }}
    .metric-badge {{
        display: inline-block; font-size: 0.62rem;
        font-family: 'IBM Plex Mono', monospace; font-weight: 600;
        letter-spacing: 0.1em; padding: 0.18rem 0.55rem;
        border-radius: 3px; margin-left: 0.5rem; vertical-align: middle;
    }}
    .badge-good {{ background: #14532d30; color: #4ade80; border: 1px solid #4ade8040; }}
    .badge-warn {{ background: #7c280030; color: #f97316; border: 1px solid #f9731640; }}

    .inner-section-label {{
        font-size: 0.6rem; letter-spacing: 0.16em; text-transform: uppercase;
        color: {t['text5']}; font-weight: 600;
        margin: 1.2rem 0 0.5rem; padding-bottom: 0.4rem;
        border-bottom: 1px solid {t['border3']};
    }}
    .tag-container {{
        background: {t['bg4']}; border: 1px solid {t['border2']};
        border-radius: 6px; padding: 0.2rem 1rem 0.5rem; margin-bottom: 0.8rem;
    }}
    .tag-row {{
        display: flex; align-items: flex-start; gap: 0.75rem;
        padding: 0.45rem 0; border-bottom: 1px solid {t['border3']};
    }}
    .tag-row:last-child {{ border-bottom: none; }}
    .tag-num {{
        min-width: 22px; font-size: 0.6rem; color: {t['num_color2']};
        font-weight: 600; padding-top: 0.05rem; text-align: right;
    }}
    .tag-text {{
        font-size: 0.78rem; color: {t['title_color']};
        line-height: 1.5; word-break: break-word;
    }}
    .tag-text.h1-text {{ color: {t['h1_color']}; }}
    .tag-text.h2-text {{ color: {t['h2_color']}; }}

    .error-card {{
        background: #1a0a0a; border: 1px solid #7f1d1d50;
        border-left: 3px solid #ef4444;
        border-radius: 0 0 8px 8px; padding: 1.2rem 1.5rem;
        font-size: 0.78rem; color: #fca5a5;
    }}
    .error-card .err-label {{
        font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase;
        color: #ef444480; margin-bottom: 0.3rem;
    }}

    hr {{ border-color: {t['border']} !important; margin: 1.5rem 0 !important; }}
    .stSpinner > div {{ border-top-color: {t['accent']} !important; }}
    .stDataFrame {{ border-radius: 6px; overflow: hidden; }}
    [data-testid="stDataFrameResizable"] {{
        border: 1px solid {t['border']} !important; border-radius: 6px !important;
    }}

    .summary-bar {{
        display: flex; gap: 1.2rem; padding: 1rem 1.4rem;
        background: {t['bg2']}; border: 1px solid {t['border']};
        border-radius: 7px; margin: 2rem 0 1.2rem; flex-wrap: wrap;
    }}
    .summary-item {{ font-size: 0.72rem; color: {t['text3']}; }}
    .summary-item strong {{ color: {t['text2']}; font-weight: 600; }}

    .stProgress > div > div {{ background: {t['accent']} !important; }}

    .scorecard-row {{
        display: flex; align-items: center; gap: 1rem;
        padding: 0.75rem 1.2rem; background: {t['bg2']};
        border: 1px solid {t['border']}; border-radius: 6px;
        margin-bottom: 0.5rem; flex-wrap: wrap;
    }}
    .scorecard-row.error-row {{ border-left: 3px solid #ef4444; }}
    .sc-url {{ font-size: 0.72rem; color: {t['text3']}; flex: 1; min-width: 180px; word-break: break-all; }}
    .sc-score {{ font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 800; min-width: 36px; text-align: center; }}
    .sc-chips {{ display: flex; flex-wrap: wrap; gap: 0.35rem; }}
    .sc-chip {{
        font-size: 0.62rem; font-family: 'IBM Plex Mono', monospace;
        font-weight: 600; letter-spacing: 0.08em;
        padding: 0.2rem 0.6rem; border-radius: 3px;
    }}
    .chip-ok   {{ background: #14532d30; color: #4ade80; border: 1px solid #4ade8040; }}
    .chip-warn {{ background: #7c280030; color: #fb923c; border: 1px solid #fb923c40; }}
    .chip-fail {{ background: #450a0a30; color: #f87171; border: 1px solid #f8717140; }}

    [data-testid="stSidebar"] {{
        background: {t['bg2']} !important;
        border-right: 1px solid {t['border']} !important;
    }}
    [data-testid="stSidebar"] label {{
        color: {t['text']} !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.8rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
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

# ── Input ─────────────────────────────────────────────────────────────────────
url_input = st.text_area(
    "Target URLs",
    placeholder="https://example.com  https://another-site.com  ...",
    height=90,
)

col_btn, col_tip = st.columns([1, 5])
with col_btn:
    run = st.button("⚡  Scan URLs")
with col_tip:
    st.markdown(
        f"<div style='font-size:0.68rem;color:{t['text4']};padding-top:0.55rem;'>"
        "Separate multiple URLs with spaces or newlines"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_meta_data(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url.strip(), timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"
        title_len = len(title)

        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag.get("content", "").strip() if desc_tag else ""
        description = description or "No description found"
        desc_len = len(description)

        h1_texts = [x.get_text(strip=True) for x in soup.find_all("h1")] or ["No H1 tags found"]
        h2_texts = [x.get_text(strip=True) for x in soup.find_all("h2")] or ["No H2 tags found"]

        return title, title_len, description, desc_len, h1_texts, h2_texts, None
    except requests.exceptions.RequestException as e:
        return None, None, None, None, None, None, str(e)


def badge(length, limit):
    if length <= limit:
        return f'<span class="metric-badge badge-good">✓ {length} chars</span>'
    return f'<span class="metric-badge badge-warn">⚠ {length} chars</span>'


def render_tag_list(items, css_class):
    rows = ""
    for idx, item in enumerate(items, 1):
        safe = html_lib.escape(item)
        rows += f"""
        <div class="tag-row">
            <span class="tag-num">{idx:02d}</span>
            <span class="tag-text {css_class}-text">{safe}</span>
        </div>"""
    return rows


# ── Scan logic ────────────────────────────────────────────────────────────────
if run and url_input.strip():
    urls = [u.strip() for u in url_input.split() if u.strip()]
    all_rows = []
    progress = st.progress(0)

    for i, url in enumerate(urls):
        progress.progress(i / len(urls), text=f"Scanning {i+1}/{len(urls)}…")

        safe_url = html_lib.escape(url)
        st.markdown(
            f"""
            <div class="url-header">
                <div class="dot"></div>
                <span>Scanning</span>
                <span class="url-text">{safe_url}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.spinner("Fetching…"):
            title, title_len, description, desc_len, h1_texts, h2_texts, error = get_meta_data(url)

        if error:
            safe_err = html_lib.escape(str(error))
            st.markdown(
                f"""
                <div class="error-card">
                    <div class="err-label">Request Failed</div>
                    {safe_err}
                </div>
                """,
                unsafe_allow_html=True,
            )
            all_rows.append({
                "URL": url, "Meta Title": "", "Title Length": "",
                "Meta Description": "", "Description Length": "",
                "H1 Tags": "", "H2 Tags": "", "Error": error,
            })
        else:
            safe_title = html_lib.escape(title)
            safe_desc  = html_lib.escape(description)
            st.markdown(
                f"""
                <div class="result-card" style="border-radius:0; border-bottom:none; padding-bottom:0.8rem;">
                    <div class="metric-row">
                        <div class="metric-box">
                            <div class="metric-label">Meta Title &nbsp;{badge(title_len, 60)}</div>
                            <div class="metric-value">{safe_title}</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-label">Meta Description &nbsp;{badge(desc_len, 160)}</div>
                            <div class="metric-value">{safe_desc}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            h1_count = len(h1_texts)
            st.markdown(
                f"""
                <div class="result-card" style="border-radius:0; border-top:none; border-bottom:none; padding-top:0; padding-bottom:0.6rem;">
                    <div class="inner-section-label">H1 Tags &nbsp;·&nbsp; {h1_count} found</div>
                    <div class="tag-container">
                        {render_tag_list(h1_texts, "h1")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            h2_count = len(h2_texts)
            st.markdown(
                f"""
                <div class="result-card" style="border-radius:0 0 8px 8px; border-top:none; padding-top:0;">
                    <div class="inner-section-label">H2 Tags &nbsp;·&nbsp; {h2_count} found</div>
                    <div class="tag-container">
                        {render_tag_list(h2_texts, "h2")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            all_rows.append({
                "URL": url,
                "Meta Title": title,
                "Title Length": title_len,
                "Meta Description": description,
                "Description Length": desc_len,
                "H1 Tags": " | ".join(h1_texts),
                "H2 Tags": " | ".join(h2_texts),
                "Error": "",
            })

    progress.progress(1.0, text="Done ✓")

    if all_rows:
        ok   = sum(1 for r in all_rows if not r["Error"])
        fail = len(all_rows) - ok

        st.markdown(
            f"""
            <div class="summary-bar">
                <div class="summary-item">Total&nbsp;&nbsp;<strong>{len(all_rows)}</strong></div>
                <div class="summary-item">✓ Success&nbsp;&nbsp;<strong>{ok}</strong></div>
                <div class="summary-item">✗ Failed&nbsp;&nbsp;<strong>{fail}</strong></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        df = pd.DataFrame(all_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        st.download_button(
            label="↓  Export CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="metascan_results.csv",
            mime="text/csv",
        )

        st.markdown(
            f"""
            <div style="margin-top:2.8rem; margin-bottom:1rem;">
                <div style="font-family:'Syne',sans-serif; font-size:1.15rem; font-weight:700;
                            color:{t['title_color']}; letter-spacing:-0.01em;">SEO Scorecard</div>
                <div style="font-size:0.63rem; letter-spacing:0.14em; text-transform:uppercase;
                            color:{t['text4']}; margin-top:0.25rem;">Per-URL audit · 4 checks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="display:flex;gap:1rem;margin-bottom:1rem;flex-wrap:wrap;">
                <span class="sc-chip chip-ok"  style="font-size:0.63rem;">✓ Pass</span>
                <span class="sc-chip chip-warn" style="font-size:0.63rem;">⚠ Too long</span>
                <span class="sc-chip chip-fail" style="font-size:0.63rem;">✗ Missing / Error</span>
                <span style="font-size:0.63rem;color:{t['text4']};align-self:center;">
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
            h1s  = [x for x in row["H1 Tags"].split(" | ") if x and x != "No H1 tags found"]
            h2s  = [x for x in row["H2 Tags"].split(" | ") if x and x != "No H2 tags found"]

            title_chip = (
                f'<span class="sc-chip chip-ok">✓ Title {tlen}ch</span>'
                if tlen <= 60 else
                f'<span class="sc-chip chip-warn">⚠ Title {tlen}ch</span>'
            )
            desc_chip = (
                f'<span class="sc-chip chip-ok">✓ Desc {dlen}ch</span>'
                if dlen <= 160 else
                f'<span class="sc-chip chip-warn">⚠ Desc {dlen}ch</span>'
            )
            h1_chip = (
                f'<span class="sc-chip chip-ok">✓ {len(h1s)} H1</span>'
                if len(h1s) == 1 else
                f'<span class="sc-chip chip-warn">⚠ {len(h1s)} H1s</span>'
                if len(h1s) > 1 else
                '<span class="sc-chip chip-fail">✗ No H1</span>'
            )
            h2_chip = (
                f'<span class="sc-chip chip-ok">✓ {len(h2s)} H2s</span>'
                if len(h2s) > 0 else
                '<span class="sc-chip chip-fail">✗ No H2</span>'
            )

            issues = sum([tlen > 60, dlen > 160, len(h1s) != 1, len(h2s) == 0])
            score  = 4 - issues
            score_color = "#4ade80" if score == 4 else "#fb923c" if score >= 2 else "#f87171"

            st.markdown(
                f"""
                <div class="scorecard-row">
                    <div class="sc-url">{safe_url}</div>
                    <div class="sc-score" style="color:{score_color};">{score}/4</div>
                    <div class="sc-chips">{title_chip}{desc_chip}{h1_chip}{h2_chip}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

elif run:
    st.markdown(
        "<div style='font-size:0.78rem;color:#ef4444;padding:0.6rem 0;'>"
        "⚠ Please enter at least one URL before scanning."
        "</div>",
        unsafe_allow_html=True,
    )
