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

# ── Theme definitions ─────────────────────────────────────────────────────────
THEMES = {
    "Obsidian": {
        "bg":           "#0a0b0e",
        "bg2":          "#0d0f16",
        "bg3":          "#0f1117",
        "border":       "#1e2130",
        "border2":      "#2a3050",
        "text":         "#c9cdd6",
        "text2":        "#94a3b8",
        "text3":        "#555c72",
        "text4":        "#404655",
        "accent":       "#3b82f6",
        "accent2":      "#2563eb",
        "heading":      "#f0f2f7",
        "grad_a":       "#0a0b0e",
        "grad_b":       "#0d1020",
        "mesh1":        "rgba(59,130,246,0.06)",
        "mesh2":        "rgba(99,102,241,0.04)",
    },
    "Aurora": {
        "bg":           "#050d12",
        "bg2":          "#071419",
        "bg3":          "#091c22",
        "border":       "#0e3340",
        "border2":      "#155060",
        "text":         "#b8d8d8",
        "text2":        "#7fb3b3",
        "text3":        "#3d7070",
        "text4":        "#2a5050",
        "accent":       "#00e5cc",
        "accent2":      "#00b8a3",
        "heading":      "#e0f7f5",
        "grad_a":       "#050d12",
        "grad_b":       "#071c22",
        "mesh1":        "rgba(0,229,204,0.07)",
        "mesh2":        "rgba(0,150,180,0.04)",
    },
    "Crimson": {
        "bg":           "#0d0608",
        "bg2":          "#130a0c",
        "bg3":          "#170b0e",
        "border":       "#2e1018",
        "border2":      "#4a1828",
        "text":         "#d6b8be",
        "text2":        "#a87a84",
        "text3":        "#6b3d45",
        "text4":        "#4a2830",
        "accent":       "#f43f5e",
        "accent2":      "#e11d48",
        "heading":      "#fdf2f4",
        "grad_a":       "#0d0608",
        "grad_b":       "#180810",
        "mesh1":        "rgba(244,63,94,0.07)",
        "mesh2":        "rgba(200,30,60,0.04)",
    },
    "Solar": {
        "bg":           "#fafaf8",
        "bg2":          "#f4f3ef",
        "bg3":          "#eeecea",
        "border":       "#ddd9d0",
        "border2":      "#c8c3b8",
        "text":         "#3d3830",
        "text2":        "#6b6258",
        "text3":        "#9c9080",
        "text4":        "#b8b0a0",
        "accent":       "#d97706",
        "accent2":      "#b45309",
        "heading":      "#1c1810",
        "grad_a":       "#fafaf8",
        "grad_b":       "#f0ede8",
        "mesh1":        "rgba(217,119,6,0.06)",
        "mesh2":        "rgba(180,83,9,0.04)",
    },
    "Violet": {
        "bg":           "#08060f",
        "bg2":          "#0e0a18",
        "bg3":          "#110d1e",
        "border":       "#211640",
        "border2":      "#362260",
        "text":         "#c4b8e0",
        "text2":        "#9080c0",
        "text3":        "#5040808",
        "text4":        "#3a2860",
        "accent":       "#a855f7",
        "accent2":      "#9333ea",
        "heading":      "#f0eaff",
        "grad_a":       "#08060f",
        "grad_b":       "#100820",
        "mesh1":        "rgba(168,85,247,0.08)",
        "mesh2":        "rgba(99,40,200,0.05)",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "Obsidian"

T = THEMES[st.session_state.theme]

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Clash+Display:wght@400;500;600;700&family=Cabinet+Grotesk:wght@400;500;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&family=DM+Mono:wght@300;400;500&display=swap');

    :root {{
        --bg:      {T['bg']};
        --bg2:     {T['bg2']};
        --bg3:     {T['bg3']};
        --border:  {T['border']};
        --border2: {T['border2']};
        --text:    {T['text']};
        --text2:   {T['text2']};
        --text3:   {T['text3']};
        --text4:   {T['text4']};
        --accent:  {T['accent']};
        --accent2: {T['accent2']};
        --heading: {T['heading']};
        --mesh1:   {T['mesh1']};
        --mesh2:   {T['mesh2']};
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Mono', monospace;
        background-color: var(--bg);
        color: var(--text);
    }}

    .stApp {{
        background:
            radial-gradient(ellipse 80% 50% at 20% -10%, var(--mesh1), transparent),
            radial-gradient(ellipse 60% 40% at 80% 110%, var(--mesh2), transparent),
            linear-gradient(160deg, {T['grad_a']} 0%, {T['grad_b']} 100%);
        min-height: 100vh;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding: 2rem 2.5rem 4rem; max-width: 1280px; }}

    /* ── Hero ── */
    .hero {{
        position: relative;
        padding: 3rem 0 2rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border);
        overflow: hidden;
    }}
    .hero::before {{
        content: 'METASCAN';
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-family: 'Bebas Neue', sans-serif;
        font-size: 9rem;
        color: var(--mesh1);
        letter-spacing: 0.2em;
        white-space: nowrap;
        pointer-events: none;
        opacity: 0.4;
    }}
    .hero-inner {{ position: relative; z-index: 1; display: flex; align-items: flex-end; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }}
    .hero-left {{ display: flex; align-items: center; gap: 1.2rem; }}
    .hero-icon {{
        width: 52px; height: 52px; border-radius: 12px;
        background: linear-gradient(135deg, var(--accent), var(--accent2));
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem;
        box-shadow: 0 0 30px color-mix(in srgb, var(--accent) 40%, transparent);
    }}
    .hero-title {{
        font-family: 'Bebas Neue', sans-serif;
        font-size: 3rem; font-weight: 400; letter-spacing: 0.06em;
        color: var(--heading); margin: 0; line-height: 1;
    }}
    .hero-title span {{ color: var(--accent); }}
    .hero-sub {{
        font-size: 0.65rem; color: var(--text3); letter-spacing: 0.18em;
        text-transform: uppercase; margin-top: 0.3rem;
    }}

    /* ── Theme switcher ── */
    .theme-switcher {{
        display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;
    }}
    .theme-label {{
        font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase;
        color: var(--text3); margin-right: 0.2rem;
    }}
    .theme-dot {{
        width: 22px; height: 22px; border-radius: 50%; cursor: pointer;
        border: 2px solid transparent; transition: all 0.2s;
        display: inline-block;
    }}
    .theme-dot:hover {{ transform: scale(1.15); }}
    .theme-dot.active {{ border-color: var(--heading); box-shadow: 0 0 8px rgba(255,255,255,0.3); }}

    /* ── Input ── */
    .stTextArea textarea {{
        background: var(--bg3) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 0.82rem !important;
        padding: 0.9rem 1rem !important;
        resize: vertical;
        transition: border-color 0.2s;
    }}
    .stTextArea textarea:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 15%, transparent) !important;
    }}
    label[data-testid="stWidgetLabel"] {{
        font-family: 'DM Mono', monospace;
        font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase;
        color: var(--text3) !important;
    }}

    /* ── Scan button ── */
    .stButton > button {{
        background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
        color: #fff !important; border: none !important; border-radius: 6px !important;
        font-family: 'DM Mono', monospace !important; font-size: 0.75rem !important;
        font-weight: 600 !important; letter-spacing: 0.12em !important;
        text-transform: uppercase !important; padding: 0.6rem 1.8rem !important;
        box-shadow: 0 4px 20px color-mix(in srgb, var(--accent) 30%, transparent) !important;
        transition: all 0.2s !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 28px color-mix(in srgb, var(--accent) 45%, transparent) !important;
    }}

    .stDownloadButton > button {{
        background: transparent !important;
        border: 1px solid color-mix(in srgb, var(--accent) 50%, transparent) !important;
        color: var(--accent) !important; border-radius: 6px !important;
        font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important;
        letter-spacing: 0.1em !important; text-transform: uppercase !important;
        padding: 0.5rem 1.4rem !important;
    }}
    .stDownloadButton > button:hover {{
        background: color-mix(in srgb, var(--accent) 10%, transparent) !important;
    }}

    /* ── URL box ── */
    .url-box {{
        background: var(--bg2); border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: 8px; padding: 0.9rem 1.2rem;
        font-size: 0.75rem; color: var(--text2);
        margin-top: 2rem; word-break: break-all;
    }}

    /* ── Meta card ── */
    .meta-card {{
        background: var(--bg2); border: 1px solid var(--border); border-radius: 10px;
        padding: 1.5rem; margin: 0.8rem 0 1rem;
        position: relative; overflow: hidden;
    }}
    .meta-card::after {{
        content: ''; position: absolute; top: 0; right: 0;
        width: 120px; height: 120px;
        background: radial-gradient(circle, var(--mesh1), transparent 70%);
        pointer-events: none;
    }}
    .metric-label {{
        font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase;
        color: var(--text4); margin-bottom: 0.45rem; font-weight: 600;
    }}
    .metric-value {{
        font-family: 'DM Mono', monospace; font-size: 0.95rem; font-weight: 500;
        color: var(--heading); line-height: 1.5; word-break: break-word;
    }}
    .metric-badge {{
        display: inline-block; font-size: 0.58rem; font-family: 'DM Mono', monospace;
        font-weight: 600; letter-spacing: 0.1em; padding: 0.15rem 0.5rem;
        border-radius: 4px; margin-left: 0.5rem; vertical-align: middle;
    }}
    .badge-good {{ background: #14532d30; color: #4ade80; border: 1px solid #4ade8040; }}
    .badge-warn {{ background: #7c280030; color: #f97316; border: 1px solid #f9731640; }}

    .divider {{ border: none; border-top: 1px solid var(--border); margin: 1.2rem 0; }}

    .section-title {{
        font-size: 0.62rem; letter-spacing: 0.18em; text-transform: uppercase;
        color: var(--text3); font-weight: 600; margin: 1.4rem 0 0.6rem;
        display: flex; align-items: center; gap: 0.5rem;
    }}
    .section-title::after {{
        content: ''; flex: 1; height: 1px; background: var(--border);
    }}

    .error-card {{
        background: color-mix(in srgb, #ef4444 5%, var(--bg2));
        border: 1px solid #7f1d1d50; border-left: 3px solid #ef4444;
        border-radius: 8px; padding: 1.2rem 1.5rem;
        font-size: 0.76rem; color: #fca5a5; margin-top: 0.8rem;
    }}

    /* ── Summary bar ── */
    .summary-bar {{
        display: flex; gap: 0; margin: 2rem 0 1.5rem;
        background: var(--bg2); border: 1px solid var(--border);
        border-radius: 10px; overflow: hidden;
    }}
    .summary-item {{
        flex: 1; padding: 1rem 1.4rem;
        border-right: 1px solid var(--border);
        min-width: 0;
    }}
    .summary-item:last-child {{ border-right: none; }}
    .summary-label {{ font-size: 0.58rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text3); }}
    .summary-value {{
        font-family: 'Bebas Neue', sans-serif; font-size: 2rem;
        color: var(--heading); line-height: 1.1; margin-top: 0.2rem;
    }}
    .summary-value.green {{ color: #4ade80; }}
    .summary-value.red   {{ color: #f87171; }}

    /* ── Scorecard ── */
    .scorecard-header {{
        margin-top: 3rem; padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        display: flex; align-items: flex-end; justify-content: space-between; flex-wrap: wrap; gap: 1rem;
    }}
    .scorecard-title {{
        font-family: 'Bebas Neue', sans-serif; font-size: 1.6rem; letter-spacing: 0.06em;
        color: var(--heading);
    }}
    .scorecard-sub {{ font-size: 0.6rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text4); }}

    /* ── Filter pills ── */
    .filter-wrap {{
        display: flex; flex-wrap: wrap; gap: 0.45rem;
        padding: 1rem 0 1.2rem;
    }}
    .filter-pill {{
        display: inline-flex; align-items: center; gap: 0.4rem;
        font-family: 'DM Mono', monospace; font-size: 0.67rem; font-weight: 500;
        letter-spacing: 0.06em; padding: 0.38rem 0.9rem; border-radius: 6px;
        border: 1px solid var(--border); background: var(--bg2);
        color: var(--text2); white-space: nowrap;
        transition: all 0.15s; cursor: default;
    }}
    .pill-active-all         {{ background: var(--accent);  border-color: var(--accent);  color: #fff; box-shadow: 0 2px 12px color-mix(in srgb, var(--accent) 40%, transparent); }}
    .pill-active-perfect     {{ background: #14532d; border-color: #4ade80; color: #86efac; }}
    .pill-active-title       {{ background: #451a03; border-color: #f59e0b; color: #fde68a; }}
    .pill-active-desc        {{ background: #431407; border-color: #fb923c; color: #fed7aa; }}
    .pill-active-heading     {{ background: #450a0a; border-color: #f87171; color: #fca5a5; }}
    .filter-count {{
        background: rgba(255,255,255,0.12); border-radius: 4px;
        padding: 0.05rem 0.35rem; font-size: 0.58rem; font-weight: 700;
    }}

    /* ── Scorecard rows ── */
    .scorecard-row {{
        display: grid;
        grid-template-columns: 1fr auto auto;
        align-items: center; gap: 1rem;
        padding: 0.9rem 1.2rem;
        background: var(--bg2); border: 1px solid var(--border);
        border-radius: 8px; margin-bottom: 0.45rem;
        transition: border-color 0.15s;
    }}
    .scorecard-row:hover {{ border-color: var(--border2); }}
    .scorecard-row.error-row {{ border-left: 3px solid #ef4444; }}
    .sc-url {{
        font-size: 0.7rem; color: var(--text2);
        word-break: break-all; min-width: 0;
    }}
    .sc-score {{
        font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem;
        min-width: 48px; text-align: center; letter-spacing: 0.05em;
    }}
    .sc-chips {{ display: flex; flex-wrap: wrap; gap: 0.3rem; justify-content: flex-end; }}
    .sc-chip {{
        font-size: 0.6rem; font-family: 'DM Mono', monospace; font-weight: 600;
        letter-spacing: 0.07em; padding: 0.18rem 0.55rem; border-radius: 4px;
        white-space: nowrap;
    }}
    .chip-ok   {{ background: #14532d25; color: #4ade80; border: 1px solid #4ade8035; }}
    .chip-warn {{ background: #7c280025; color: #fb923c; border: 1px solid #fb923c35; }}
    .chip-fail {{ background: #450a0a25; color: #f87171; border: 1px solid #f8717135; }}

    /* ── Clear filter button ── */
    [data-testid="stButton"] button[kind="secondary"],
    div[data-testid="column"] button:has(+ *) {{
        /* fallback — the key-specific override below handles it */
    }}
    /* Target clear_filter button by surrounding it differently via wrapper */
    .clear-filter-btn > div > button, .clear-filter-btn button {{
        background: transparent !important;
        border: 1px solid color-mix(in srgb, var(--accent) 40%, transparent) !important;
        color: var(--accent) !important;
        box-shadow: none !important;
        font-size: 0.68rem !important;
        padding: 0.52rem 0.8rem !important;
        letter-spacing: 0.08em !important;
    }}
    .clear-filter-btn button:hover {{
        background: color-mix(in srgb, var(--accent) 10%, transparent) !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    .no-results-card {{
        background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
        padding: 2.5rem; text-align: center; color: var(--text3);
        font-size: 0.76rem; letter-spacing: 0.08em;
    }}

    .stDataFrame {{ border-radius: 8px; overflow: hidden; }}
    [data-testid="stDataFrameResizable"] {{ border: 1px solid var(--border) !important; border-radius: 8px !important; }}
    .stProgress > div > div {{ background: var(--accent) !important; }}

    @media (max-width: 768px) {{
        .block-container {{ padding: 1rem 1rem 3rem; }}
        .hero-title {{ font-size: 2.2rem; }}
        .hero::before {{ font-size: 5rem; }}
        .scorecard-row {{ grid-template-columns: 1fr; gap: 0.5rem; }}
        .sc-chips {{ justify-content: flex-start; }}
        .filter-wrap {{ gap: 0.35rem; }}
        .filter-pill {{ font-size: 0.62rem; padding: 0.32rem 0.7rem; }}
        .summary-bar {{ flex-direction: column; }}
        .summary-item {{ border-right: none; border-bottom: 1px solid var(--border); }}
        .summary-item:last-child {{ border-bottom: none; }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Hero + Theme switcher ─────────────────────────────────────────────────────
THEME_ACCENTS = {
    "Obsidian": "#3b82f6",
    "Aurora":   "#00e5cc",
    "Crimson":  "#f43f5e",
    "Solar":    "#d97706",
    "Violet":   "#a855f7",
}

dots_html = ""
for name, color in THEME_ACCENTS.items():
    active = "active" if name == st.session_state.theme else ""
    dots_html += f'<span class="theme-dot {active}" style="background:{color};" title="{name}"></span>'

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-inner">
            <div class="hero-left">
                <div class="hero-icon">🔍</div>
                <div>
                    <div class="hero-title">Meta<span>Scan</span></div>
                    <div class="hero-sub">SEO Metadata Inspector · v3.0</div>
                </div>
            </div>
            <div class="theme-switcher">
                <span class="theme-label">Theme</span>
                {dots_html}
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Theme selector (real Streamlit widget, hidden visually under the dots)
theme_pick = st.selectbox(
    "Choose theme",
    list(THEMES.keys()),
    index=list(THEMES.keys()).index(st.session_state.theme),
    key="theme_select",
    label_visibility="collapsed",
)
if theme_pick != st.session_state.theme:
    st.session_state.theme = theme_pick
    st.rerun()

# ── Input ─────────────────────────────────────────────────────────────────────
url_input = st.text_area(
    "Target URLs",
    placeholder="https://example.com\nhttps://another-site.com",
    height=100,
)
col_btn, col_tip = st.columns([1, 5])
with col_btn:
    run = st.button("⚡  Scan URLs")
with col_tip:
    st.caption("One URL per line, or separate with spaces")


# ── Helpers ───────────────────────────────────────────────────────────────────
def normalize_url(url):
    url = url.strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def error_result(message):
    return {"title": "", "title_len": None, "description": "", "desc_len": None,
            "h1_texts": [], "h2_texts": [], "error": message}


def get_meta_data(url):
    try:
        headers = {
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }
        r = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")
        page_text = soup.get_text(" ", strip=True).lower()

        title_tag = soup.find("title")
        title = (title_tag.get_text(strip=True) if title_tag else "") or "No title found"
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = (desc_tag.get("content", "").strip() if desc_tag else "") or "No description found"
        h1s = [t.get_text(strip=True) for t in soup.find_all("h1") if t.get_text(strip=True)]
        h2s = [t.get_text(strip=True) for t in soup.find_all("h2") if t.get_text(strip=True)]

        js_phrases = ["javascript is disabled", "enable javascript", "requires javascript", "javascript required"]
        if any(p in page_text for p in js_phrases) and not (title != "No title found" or description != "No description found" or h1s or h2s):
            return error_result("JavaScript required: page does not expose SEO content in raw HTML.")

        return {"title": title, "title_len": len(title), "description": description,
                "desc_len": len(description), "h1_texts": h1s, "h2_texts": h2s, "error": ""}

    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else ""
        if code == 403:
            return error_result("403 Forbidden — site blocked automated scanning (Cloudflare / bot protection).")
        return error_result(str(e))
    except requests.exceptions.RequestException as e:
        return error_result(str(e))
    except Exception as e:
        return error_result(f"Unexpected error: {e}")


def badge(length, limit):
    if length is None:
        return '<span class="metric-badge badge-warn">⚠ N/A</span>'
    cls = "badge-good" if length <= limit else "badge-warn"
    icon = "✓" if length <= limit else "⚠"
    return f'<span class="metric-badge {cls}">{icon} {length} chars</span>'


def make_tag_df(tags, col):
    if not tags:
        return pd.DataFrame({"No.": [], col: []})
    return pd.DataFrame({"No.": [f"{i:02d}" for i in range(1, len(tags)+1)], col: tags})


def prepare_df(rows):
    df = pd.DataFrame(rows)
    for c in ["Title Length", "Description Length"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    for c in ["URL", "Meta Title", "Meta Description", "H1 Tags", "H2 Tags", "Error"]:
        df[c] = df[c].fillna("").astype(str)
    return df


def render_meta_card(title, tlen, desc, dlen):
    st.markdown(
        f"""
        <div class="meta-card">
            <div class="metric-label">Meta Title {badge(tlen, 60)}</div>
            <div class="metric-value">{html_lib.escape(title)}</div>
            <hr class="divider">
            <div class="metric-label">Meta Description {badge(dlen, 160)}</div>
            <div class="metric-value">{html_lib.escape(desc)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Filter definitions (4 only) ───────────────────────────────────────────────
# key, label, active pill class, description
FILTERS = [
    ("all",     "All URLs",          "pill-active-all",     "Every scanned URL"),
    ("perfect", "✓ Perfect",         "pill-active-perfect", "All checks pass — title, desc, H1, H2"),
    ("title",   "⚠ Meta Title",      "pill-active-title",   "Title missing or > 60 chars"),
    ("desc",    "⚠ Meta Description","pill-active-desc",    "Description missing or > 160 chars"),
    ("heading", "✗ Heading Issue",   "pill-active-heading", "No H1, multiple H1s, or no H2 tags"),
]


def get_tags(row):
    tags = set()
    if row["Error"]:
        tags.add("heading")   # counts as heading issue in absence of data
        return tags

    tlen = int(row["Title Length"])
    dlen = int(row["Description Length"])
    h1s  = [x for x in row["H1 Tags"].split(" | ") if x.strip()]
    h2s  = [x for x in row["H2 Tags"].split(" | ") if x.strip()]

    title_ok   = (tlen <= 60) and (row["Meta Title"] not in ("", "No title found"))
    desc_ok    = (dlen <= 160) and (row["Meta Description"] not in ("", "No description found"))
    heading_ok = (len(h1s) == 1) and (len(h2s) > 0)

    if not title_ok:
        tags.add("title")
    if not desc_ok:
        tags.add("desc")
    if not heading_ok:
        tags.add("heading")
    if not tags:
        tags.add("perfect")

    return tags


def render_scorecard(all_rows):
    st.markdown(
        """
        <div class="scorecard-header">
            <div>
                <div class="scorecard-title">SEO Scorecard</div>
                <div class="scorecard-sub">Per-URL audit · title · description · heading structure</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Counts
    tag_counts = {k: 0 for k, *_ in FILTERS}
    tag_counts["all"] = len(all_rows)
    row_tags = {}
    for row in all_rows:
        tags = get_tags(row)
        row_tags[row["URL"]] = tags
        for t in tags:
            if t in tag_counts:
                tag_counts[t] += 1

    if "sc_filter" not in st.session_state:
        st.session_state.sc_filter = "all"

    # Pills (display only)
    pills_html = '<div class="filter-wrap">'
    for key, label, active_cls, desc in FILTERS:
        is_active = st.session_state.sc_filter == key
        cls = active_cls if is_active else ""
        count = tag_counts.get(key, 0)
        pills_html += (
            f'<span class="filter-pill {cls}" title="{desc}">'
            f'{label} <span class="filter-count">{count}</span></span>'
        )
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)

    # Clickable filter buttons
    btn_cols = st.columns(len(FILTERS))
    for i, (key, label, _, desc) in enumerate(FILTERS):
        with btn_cols[i]:
            if st.button(label, key=f"f_{key}", help=desc, use_container_width=True):
                st.session_state.sc_filter = key
                st.rerun()

    # ── Active filter banner + clear button ──────────────────────────────────
    active = st.session_state.sc_filter

    if active != "all":
        active_label = next(label for key, label, *_ in FILTERS if key == active)
        filtered_count = sum(1 for r in all_rows if active in row_tags.get(r["URL"], set()))

        banner_col, clear_col = st.columns([5, 1])
        with banner_col:
            st.markdown(
                f"""
                <div style="
                    display:flex; align-items:center; gap:0.8rem;
                    background:color-mix(in srgb, var(--accent) 8%, var(--bg2));
                    border:1px solid color-mix(in srgb, var(--accent) 30%, transparent);
                    border-radius:8px; padding:0.65rem 1rem; margin-top:0.5rem;
                ">
                    <span style="font-size:0.62rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--text3);">
                        Filtering by
                    </span>
                    <span style="
                        font-family:'DM Mono',monospace; font-size:0.72rem; font-weight:600;
                        color:var(--accent); background:color-mix(in srgb,var(--accent) 12%,transparent);
                        padding:0.2rem 0.7rem; border-radius:5px;
                        border:1px solid color-mix(in srgb,var(--accent) 30%,transparent);
                    ">{active_label}</span>
                    <span style="font-size:0.62rem;color:var(--text3);">
                        — showing <strong style="color:var(--heading);">{filtered_count}</strong> of
                        <strong style="color:var(--heading);">{len(all_rows)}</strong> URLs
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with clear_col:
            st.markdown("<div class='clear-filter-btn' style='margin-top:0.5rem;'>", unsafe_allow_html=True)
            if st.button("✕  Clear Filter", key="clear_filter", use_container_width=True,
                         help="Remove filter and show all results"):
                st.session_state.sc_filter = "all"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Legend
    st.markdown(
        """
        <div style="display:flex;gap:0.8rem;margin:0.8rem 0 1rem;flex-wrap:wrap;align-items:center;">
            <span class="sc-chip chip-ok">✓ Pass</span>
            <span class="sc-chip chip-warn">⚠ Too long</span>
            <span class="sc-chip chip-fail">✗ Missing</span>
            <span style="font-size:0.6rem;color:var(--text3);">
                Title ≤60ch · Desc ≤160ch · Exactly 1 H1 · H2s present
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    filtered = all_rows if active == "all" else [r for r in all_rows if active in row_tags.get(r["URL"], set())]

    if not filtered:
        st.markdown(
            f'<div class="no-results-card">No URLs match the <strong>{active}</strong> filter.</div>',
            unsafe_allow_html=True,
        )
        return

    for row in filtered:
        safe_url = html_lib.escape(row["URL"])

        if row["Error"]:
            st.markdown(
                f"""
                <div class="scorecard-row error-row">
                    <div class="sc-url">{safe_url}</div>
                    <div class="sc-score" style="color:#f87171;">–/3</div>
                    <div class="sc-chips"><span class="sc-chip chip-fail">✗ Fetch Error</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            continue

        tlen = int(row["Title Length"])
        dlen = int(row["Description Length"])
        h1s  = [x for x in row["H1 Tags"].split(" | ") if x.strip()]
        h2s  = [x for x in row["H2 Tags"].split(" | ") if x.strip()]
        no_title = row["Meta Title"] in ("", "No title found")
        no_desc  = row["Meta Description"] in ("", "No description found")

        title_chip = ('<span class="sc-chip chip-fail">✗ No Title</span>'   if no_title
                      else f'<span class="sc-chip chip-warn">⚠ Title {tlen}ch</span>' if tlen > 60
                      else f'<span class="sc-chip chip-ok">✓ Title {tlen}ch</span>')
        desc_chip  = ('<span class="sc-chip chip-fail">✗ No Desc</span>'    if no_desc
                      else f'<span class="sc-chip chip-warn">⚠ Desc {dlen}ch</span>' if dlen > 160
                      else f'<span class="sc-chip chip-ok">✓ Desc {dlen}ch</span>')
        h1_chip    = ('<span class="sc-chip chip-fail">✗ No H1</span>'      if len(h1s) == 0
                      else f'<span class="sc-chip chip-warn">⚠ {len(h1s)} H1s</span>' if len(h1s) > 1
                      else f'<span class="sc-chip chip-ok">✓ 1 H1</span>')
        h2_chip    = ('<span class="sc-chip chip-fail">✗ No H2</span>'      if not h2s
                      else f'<span class="sc-chip chip-ok">✓ {len(h2s)} H2s</span>')

        issues = sum([no_title or tlen > 60, no_desc or dlen > 160,
                      len(h1s) != 1 or not h2s])
        score  = 3 - issues
        score_color = "#4ade80" if score == 3 else "#fb923c" if score == 2 else "#f87171"

        st.markdown(
            f"""
            <div class="scorecard-row">
                <div class="sc-url">{safe_url}</div>
                <div class="sc-score" style="color:{score_color};">{score}/3</div>
                <div class="sc-chips">{title_chip}{desc_chip}{h1_chip}{h2_chip}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── Scan ──────────────────────────────────────────────────────────────────────
def run_scan(urls):
    rows = []
    progress = st.progress(0)
    for i, url in enumerate(urls):
        progress.progress(i / len(urls), text=f"Scanning {i+1}/{len(urls)}…")
        st.markdown(f'<div class="url-box">↗ {html_lib.escape(url)}</div>', unsafe_allow_html=True)
        with st.spinner("Fetching page…"):
            result = get_meta_data(url)

        if result["error"]:
            st.markdown(
                f'<div class="error-card"><strong>Request Failed</strong><br><br>{html_lib.escape(result["error"])}</div>',
                unsafe_allow_html=True,
            )
            rows.append({"URL": url, "Meta Title": "", "Title Length": None,
                         "Meta Description": "", "Description Length": None,
                         "H1 Tags": "", "H2 Tags": "", "Error": result["error"]})
            continue

        render_meta_card(result["title"], result["title_len"], result["description"], result["desc_len"])

        st.markdown(f'<div class="section-title">H1 Tags · {len(result["h1_texts"])} found</div>', unsafe_allow_html=True)
        if result["h1_texts"]:
            st.dataframe(make_tag_df(result["h1_texts"], "H1 Tag"), use_container_width=True, hide_index=True)
        else:
            st.info("No H1 tags found on this page.")

        st.markdown(f'<div class="section-title">H2 Tags · {len(result["h2_texts"])} found</div>', unsafe_allow_html=True)
        if result["h2_texts"]:
            st.dataframe(make_tag_df(result["h2_texts"], "H2 Tag"), use_container_width=True, hide_index=True)
        else:
            st.info("No H2 tags found on this page.")

        rows.append({
            "URL": url, "Meta Title": result["title"], "Title Length": result["title_len"],
            "Meta Description": result["description"], "Description Length": result["desc_len"],
            "H1 Tags": " | ".join(result["h1_texts"]), "H2 Tags": " | ".join(result["h2_texts"]), "Error": "",
        })

    progress.progress(1.0, text="Done ✓")
    return rows


def compute_health(all_rows):
    """Returns health score 0-100 and state label based on overall SEO quality."""
    if not all_rows:
        return 100, "pristine"
    total = len(all_rows)
    issue_points = 0
    for row in all_rows:
        tags = get_tags(row)
        if "perfect" in tags:
            issue_points += 0
        elif row["Error"]:
            issue_points += 3
        else:
            issue_points += len(tags)
    max_points = total * 3
    score = max(0, round(100 - (issue_points / max_points) * 100))
    if score >= 85:   state = "pristine"
    elif score >= 60: state = "tired"
    elif score >= 30: state = "sick"
    else:             state = "critical"
    return score, state


def get_leopard_b64():
    return "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"


def render_snow_leopard(all_rows):
    score, state = compute_health(all_rows)
    b64 = get_leopard_b64()

    # ── Per-state config ──────────────────────────────────────────────────────
    states_cfg = {
        "pristine": {
            "border": "#4ade80", "glow": "#4ade80", "label": "#4ade80",
            "label_bg": "#14532d", "icon": "✦", "text": "HEALTHY",
            "msg": "Peak condition. Every page is SEO perfect.",
            # Image: vivid, bright, teal-green — full life
            "img_filter": "brightness(1.2) saturate(1.6) hue-rotate(110deg) contrast(1.05)",
            # Overlay tint on top of image
            "overlay_color": "rgba(74,222,128,0.12)",
            # Card background
            "card_bg": "linear-gradient(160deg,#071a0f,#050d08)",
            # Health bar color
            "bar_color": "#4ade80",
            # Wound marks (SVG scars drawn over image) — none for healthy
            "wounds": "",
            # Vignette (dark edge fade) — light for healthy
            "vignette": "rgba(0,0,0,0.1)",
            # Animation speed
            "breathe_dur": "3s",
            "pulse_dur": "3s",
        },
        "tired": {
            "border": "#fbbf24", "glow": "#fbbf24", "label": "#fbbf24",
            "label_bg": "#451a03", "icon": "◎", "text": "TIRED",
            "msg": "A few rough patches. Minor fixes needed.",
            "img_filter": "brightness(0.95) saturate(0.85) hue-rotate(15deg) contrast(0.95)",
            "overlay_color": "rgba(251,191,36,0.10)",
            "card_bg": "linear-gradient(160deg,#1a1200,#0d0a00)",
            "bar_color": "#fbbf24",
            "wounds": "",
            "vignette": "rgba(0,0,0,0.25)",
            "breathe_dur": "5s",
            "pulse_dur": "5s",
        },
        "sick": {
            "border": "#fb923c", "glow": "#fb923c", "label": "#fb923c",
            "label_bg": "#431407", "icon": "◉", "text": "SICK",
            "msg": "Multiple SEO issues found. Needs attention.",
            # Desaturated, darker, warm sick tone
            "img_filter": "brightness(0.72) saturate(0.35) sepia(0.45) contrast(0.9) hue-rotate(-10deg)",
            "overlay_color": "rgba(251,146,60,0.18)",
            "card_bg": "linear-gradient(160deg,#1a0800,#0d0500)",
            "bar_color": "#fb923c",
            # Scratch marks drawn as SVG lines over the image
            "wounds": (
                '<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;" '
                'viewBox="0 0 100 60" preserveAspectRatio="none">'
                '<line x1="30" y1="5" x2="38" y2="25" stroke="#ff6b3580" stroke-width="1.2" stroke-linecap="round"/>'
                '<line x1="33" y1="5" x2="41" y2="25" stroke="#ff6b3560" stroke-width="0.8" stroke-linecap="round"/>'
                '<line x1="36" y1="6" x2="43" y2="24" stroke="#ff6b3540" stroke-width="0.6" stroke-linecap="round"/>'
                '</svg>'
            ),
            "vignette": "rgba(0,0,0,0.45)",
            "breathe_dur": "8s",
            "pulse_dur": "8s",
        },
        "critical": {
            "border": "#f87171", "glow": "#f87171", "label": "#f87171",
            "label_bg": "#450a0a", "icon": "✖", "text": "CRITICAL",
            "msg": "Serious SEO problems everywhere. Urgent care needed.",
            # Nearly grayscale, very dark, low contrast
            "img_filter": "brightness(0.45) saturate(0.08) sepia(0.6) contrast(0.85) hue-rotate(-15deg)",
            "overlay_color": "rgba(248,113,113,0.22)",
            "card_bg": "linear-gradient(160deg,#1a0000,#0d0000)",
            "bar_color": "#f87171",
            # Multiple deep wound marks
            "wounds": (
                '<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;" '
                'viewBox="0 0 100 60" preserveAspectRatio="none">'
                '<line x1="28" y1="4"  x2="37" y2="26" stroke="#ff4040a0" stroke-width="1.5" stroke-linecap="round"/>'
                '<line x1="31" y1="4"  x2="40" y2="26" stroke="#ff404080" stroke-width="1.0" stroke-linecap="round"/>'
                '<line x1="34" y1="5"  x2="42" y2="24" stroke="#ff404060" stroke-width="0.7" stroke-linecap="round"/>'
                '<line x1="55" y1="10" x2="62" y2="28" stroke="#ff4040a0" stroke-width="1.3" stroke-linecap="round"/>'
                '<line x1="57" y1="10" x2="64" y2="28" stroke="#ff404070" stroke-width="0.8" stroke-linecap="round"/>'
                '<line x1="70" y1="30" x2="80" y2="50" stroke="#ff404090" stroke-width="1.2" stroke-linecap="round"/>'
                '<line x1="72" y1="30" x2="82" y2="50" stroke="#ff404060" stroke-width="0.7" stroke-linecap="round"/>'
                '</svg>'
            ),
            "vignette": "rgba(0,0,0,0.65)",
            "breathe_dur": "14s",
            "pulse_dur": "14s",
        },
    }
    p = states_cfg[state]

    # ── Health bar (10 segments) ──────────────────────────────────────────────
    filled_segs = round(score / 10)
    bar_html = '<div style="display:flex;gap:3px;margin:0.6rem 0;">'
    for i in range(10):
        if i < filled_segs:
            seg_color = p["bar_color"]
            seg_shadow = "0 0 6px " + p["bar_color"]
            seg_opacity = "1"
        else:
            seg_color = "#1e2130"
            seg_shadow = "none"
            seg_opacity = "0.6"
        bar_html += (
            '<div style="flex:1;height:6px;border-radius:3px;'
            'background:' + seg_color + ';'
            'box-shadow:' + seg_shadow + ';'
            'opacity:' + seg_opacity + ';'
            'transition:all 0.4s ease;"></div>'
        )
    bar_html += '</div>'

    # ── Unique animation keyframe name per state (avoid class reuse bugs) ────
    uid = "leo_" + state

    css = (
        "<style>\n"
        "@keyframes " + uid + "_pulse {\n"
        "  0%,100% { box-shadow: 0 0 20px " + p["glow"] + "55, 0 0 40px " + p["glow"] + "22; }\n"
        "  50%      { box-shadow: 0 0 40px " + p["glow"] + "88, 0 0 70px " + p["glow"] + "44; }\n"
        "}\n"
        "@keyframes " + uid + "_breathe {\n"
        "  0%,100% { transform: scale(1);   opacity: 1.0; }\n"
        "  50%      { transform: scale(1.015); opacity: 0.92; }\n"
        "}\n"
        "@keyframes " + uid + "_vignette {\n"
        "  0%,100% { opacity: 0.7; }\n"
        "  50%      { opacity: 1.0; }\n"
        "}\n"
        "</style>\n"
    )

    # ── Card wrapper (inline style — no shared class) ─────────────────────────
    card_style = (
        "position:sticky;top:1.5rem;"
        "background:" + p["card_bg"] + ";"
        "border:1px solid " + p["border"] + "55;"
        "border-radius:18px;"
        "padding:1.2rem 0.9rem 1.1rem;"
        "text-align:center;"
        "animation:" + uid + "_pulse " + p["pulse_dur"] + " ease-in-out infinite;"
        "transition:all 0.8s ease;"
    )

    # ── Image wrapper with all overlays ──────────────────────────────────────
    img_wrap = (
        '<div style="position:relative;border-radius:12px;overflow:hidden;margin-bottom:0.5rem;">'
        # The actual image with CSS filter
        '<img src="data:image/jpeg;base64,' + b64 + '" alt="Snow Leopard" '
        'style="width:100%;display:block;border-radius:12px;'
        'filter:' + p["img_filter"] + ';'
        'animation:' + uid + '_breathe ' + p["breathe_dur"] + ' ease-in-out infinite;'
        'transition:filter 1s ease;"/>'
        # Color tint overlay
        '<div style="position:absolute;inset:0;border-radius:12px;'
        'background:' + p["overlay_color"] + ';pointer-events:none;"></div>'
        # Vignette overlay (darkens edges — more intense when sick/critical)
        '<div style="position:absolute;inset:0;border-radius:12px;'
        'background:radial-gradient(ellipse at center, transparent 40%, ' + p["vignette"] + ' 100%);'
        'animation:' + uid + '_vignette ' + p["breathe_dur"] + ' ease-in-out infinite;'
        'pointer-events:none;"></div>'
        # Wound scratch marks (SVG)
        + p["wounds"] +
        '</div>'
    )

    # ── Score number ──────────────────────────────────────────────────────────
    score_html = (
        '<div style="font-family:\'Bebas Neue\',sans-serif;font-size:2.8rem;'
        'letter-spacing:0.02em;color:' + p["label"] + ';line-height:1;'
        'text-shadow:0 0 20px ' + p["glow"] + '88;margin:0.3rem 0 0;">'
        + str(score) +
        '<span style="font-size:0.95rem;opacity:0.45;'
        'font-family:\'DM Mono\',monospace;"> / 100</span></div>'
    )

    # ── Status badge ──────────────────────────────────────────────────────────
    badge_html = (
        '<div style="margin:0.5rem 0 0.3rem;">'
        '<span style="font-family:\'Bebas Neue\',sans-serif;font-size:0.9rem;'
        'letter-spacing:0.18em;'
        'background:' + p["label_bg"] + ';color:' + p["label"] + ';'
        'padding:0.25rem 1.1rem;border-radius:5px;'
        'border:1px solid ' + p["border"] + '70;'
        'box-shadow:0 0 12px ' + p["glow"] + '44;">'
        + p["icon"] + " " + p["text"] +
        '</span></div>'
    )

    msg_html = (
        '<div style="font-size:0.6rem;color:#666e88;margin-top:0.5rem;'
        'line-height:1.6;padding:0 0.2rem;">'
        + p["msg"] + '</div>'
    )

    label_html = (
        '<div style="font-size:0.52rem;letter-spacing:0.22em;text-transform:uppercase;'
        'color:#404655;margin-bottom:0.8rem;font-weight:600;">◈ SEO GUARDIAN</div>'
    )

    full_html = (
        css +
        '<div style="' + card_style + '">' +
        label_html +
        img_wrap +
        badge_html +
        bar_html +
        score_html +
        msg_html +
        '</div>'
    )

    st.markdown(full_html, unsafe_allow_html=True)


def render_results(all_rows):
    success = sum(1 for r in all_rows if not r["Error"])
    failed  = len(all_rows) - success
    perfect = sum(1 for r in all_rows if not get_tags(r) - {"perfect"} and not r["Error"])

    # Two-column layout: main content (left) + snow leopard (right)
    main_col, leo_col = st.columns([3, 1], gap="large")

    with leo_col:
        render_snow_leopard(all_rows)

    with main_col:
        st.markdown(
            f"""
            <div class="summary-bar">
                <div class="summary-item">
                    <div class="summary-label">Total Scanned</div>
                    <div class="summary-value">{len(all_rows)}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Success</div>
                    <div class="summary-value green">{success}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Failed</div>
                    <div class="summary-value red">{failed}</div>
                </div>
                <div class="summary-item">
                    <div class="summary-label">Perfect Score</div>
                    <div class="summary-value" style="color:var(--accent);">{perfect}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        df = prepare_df(all_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="↓  Export CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="metascan_results.csv",
            mime="text/csv",
        )
        render_scorecard(all_rows)


# ── Entry ─────────────────────────────────────────────────────────────────────
if run and url_input.strip():
    urls = [normalize_url(u) for u in url_input.split() if normalize_url(u)]
    all_rows = run_scan(urls)
    if all_rows:
        st.session_state.scan_results = all_rows
        st.session_state.sc_filter = "all"
        render_results(all_rows)
elif run:
    st.error("Please enter at least one URL before scanning.")
elif "scan_results" in st.session_state:
    render_results(st.session_state.scan_results)
