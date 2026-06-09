import streamlit as st
import streamlit.components.v1 as components
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
    """Returns health score 0-100 and state label."""
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


def get_leopard_images():
    """Returns correct image per health state."""
    return {
        "pristine": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAwICQsJCAwLCgsODQwOEh4UEhEREiUbHBYeLCcuLisnKyoxN0Y7MTRCNCorPVM+QkhKTk9OLztWXFVMW0ZNTkv/2wBDAQ0ODhIQEiQUFCRLMisyS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0v/wAARCAFAAeADASIAAhEBAxEB/8QAGwABAAIDAQEAAAAAAAAAAAAAAAQFAgMGBwH/xAA/EAABAwMCBAQEBAUDAwMFAAABAAIDBAUREiEGMUFREyJhcRQygZEjobHRFUJSwfAHM+EWYvEkQ3JEU4KSov/EABgBAQEBAQEAAAAAAAAAAAAAAAABAgME/8QAIBEBAQEAAgMBAQEBAQAAAAAAAAERAiESMUEDUXETIv/aAAwDAQACEQMRAD8A8qREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAWTByOAsVlGcHYj2PVBY00MEjR4jGjPqpsFpo5HDMmnPqqtjnA7swPRS42l+7A7GMFGa6Cj4ZpJv9xgIxzDlnNwbRO2jlkYffKo46yqowPDmcNPdSYuKKuMDUfEGdw4KMWcvlarjwlV0pJhzMz0GCPoqiajkgbiaNzR1dpOy7Wi4lgqgGyao3H7Kx8KGvYWlrJA4Hn1RPOz28ve3SeYI6EL4uxuXDEbh4tMSR1aBuufqrVU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",
        "tired":    "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",
        "sick":     "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fMOUka3qQjMf0yUsPMOOfzUBEEz+a3cEd+cHyaP2XF1yw77UrifMriiCQy/ZjbtEh25zggFWsPbHW4AGx3CGAYDdgwqJFNRdtG3ttq2R3hhk92Y/JS6/bmwXAWoWFo/oaOPzWRRTjF5V9Lq9r+z8rP8AqzYa7rmEEfgvy5qnZLUHhzrhjc0cCIHsI+IXzVFn/HPpedfR3ns08Ef6ina0jA2k8PmCuUcfZ6iC6t2jkY0jG0Ma4ke21fPUV4/2nL+n0Iz9l5C19rWLVh/2g0/VtB/8WL1Z1vsrETKYjdlGAwOdI4NHxAC+dorx/s5Nnc7eOyW0qcMTQ3DDsHDy4KB/rvXc5FkD02BZtE4YnKr6Ttnrz85vuGfJjR+ir7GtalZBE12d4PMF6gorxn4m6/XOc45c4k+ZK/ERVBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQf/2Q==",
        "critical": "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",
    }


def render_snow_leopard(all_rows):
    score, state = compute_health(all_rows)
    images = get_leopard_images()
    b64 = images[state]

    # Count issues for mini stats
    total       = len(all_rows)
    perfect_ct  = sum(1 for r in all_rows if "perfect" in get_tags(r))
    issues_ct   = total - perfect_ct
    success_ct  = sum(1 for r in all_rows if not r["Error"])

    cfg = {
        # ── HEALTHY ────────────────────────────────────────────────────────────
        "pristine": {
            "border":"#4ade80","glow":"#4ade80","label":"#4ade80","label_bg":"#14532d",
            "icon":"✦","text":"HEALTHY","msg":"Peak condition — running at full speed!",
            "bar":"#4ade80","pulse":"2s","breathe":"0.7s","breathe_scale":"1.02",
            "img_filter":"brightness(1.12) saturate(1.35) contrast(1.06)",
            "overlay":"rgba(74,222,128,0.08)","vignette":"transparent",
            # Animated background scene — lush forest/mountain
            "scene_bg":"linear-gradient(180deg,#001a08 0%,#002d10 35%,#001408 100%)",
            "scene_stars": True, "scene_color":"#4ade80",
            # Floating SEO metric pills above image
            "metrics":[("Title ✓","#4ade80"),("Desc ✓","#4ade80"),("H1 ✓","#4ade80")],
            "alert_color":"", "alert_text":"",
        },
        # ── TIRED ──────────────────────────────────────────────────────────────
        "tired": {
            "border":"#fbbf24","glow":"#fbbf24","label":"#fbbf24","label_bg":"#451a03",
            "icon":"◎","text":"TIRED","msg":"Slowing down. Minor SEO issues found.",
            "bar":"#fbbf24","pulse":"5s","breathe":"2s","breathe_scale":"1.01",
            "img_filter":"brightness(0.92) saturate(0.85) hue-rotate(8deg)",
            "overlay":"rgba(251,191,36,0.07)","vignette":"rgba(0,0,0,0.25)",
            "scene_bg":"linear-gradient(180deg,#1a1200 0%,#0f0900 50%,#080600 100%)",
            "scene_stars": True, "scene_color":"#fbbf24",
            "metrics":[("Issues","#fbbf24"),("Check","#fbbf24"),("Fix","#fbbf24")],
            "alert_color":"#fbbf24","alert_text":"⚠ Minor Issues",
        },
        # ── SICK ───────────────────────────────────────────────────────────────
        "sick": {
            "border":"#fb923c","glow":"#fb923c","label":"#fb923c","label_bg":"#431407",
            "icon":"◉","text":"SICK","msg":"Limping badly. Multiple SEO problems.",
            "bar":"#fb923c","pulse":"8s","breathe":"6s","breathe_scale":"1.004",
            "img_filter":"brightness(0.75) saturate(0.45) sepia(0.3) hue-rotate(-10deg)",
            "overlay":"rgba(251,146,60,0.15)","vignette":"rgba(0,0,0,0.52)",
            "scene_bg":"linear-gradient(180deg,#1a0800 0%,#100400 50%,#060200 100%)",
            "scene_stars": False,"scene_color":"#fb923c",
            "metrics":[("Errors!","#fb923c"),("Broken","#fb923c"),("Fix Now","#ff4400")],
            "alert_color":"#fb923c","alert_text":"⚠ Multiple Problems",
        },
        # ── CRITICAL ───────────────────────────────────────────────────────────
        "critical": {
            "border":"#f87171","glow":"#f87171","label":"#f87171","label_bg":"#450a0a",
            "icon":"✖","text":"CRITICAL","msg":"Collapsed. Urgent SEO fixes needed!",
            "bar":"#f87171","pulse":"14s","breathe":"12s","breathe_scale":"1.002",
            "img_filter":"brightness(0.48) saturate(0.12) sepia(0.55) hue-rotate(-15deg) contrast(0.85)",
            "overlay":"rgba(248,113,113,0.20)","vignette":"rgba(140,0,0,0.50)",
            "scene_bg":"linear-gradient(180deg,#1a0000 0%,#0d0000 50%,#040000 100%)",
            "scene_stars": False,"scene_color":"#f87171",
            "metrics":[("CRITICAL","#f87171"),("URGENT","#f87171"),("DOWN","#ff0000")],
            "alert_color":"#f87171","alert_text":"✖ CRITICAL — Fix Immediately",
        },
    }
    p   = cfg[state]
    uid = "lp_" + state
    gl  = p["glow"]
    bc  = p["border"]
    sc  = p["scene_color"]

    # ── CSS ────────────────────────────────────────────────────────────────────
    css = """<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent;overflow:hidden;font-family:'DM Mono',monospace}
@keyframes {uid}_pulse{{
  0%,100%{{box-shadow:0 0 20px {gl}55,0 0 45px {gl}22,inset 0 0 20px {gl}08}}
  50%     {{box-shadow:0 0 45px {gl}cc,0 0 80px {gl}55,inset 0 0 30px {gl}14}}
}}
@keyframes {uid}_breathe{{
  0%,100%{{transform:scale(1)}}
  50%     {{transform:scale({bs})}}
}}
@keyframes {uid}_float{{
  0%,100%{{transform:translateY(0px)}}
  50%     {{transform:translateY(-4px)}}
}}
@keyframes {uid}_scan{{
  0%  {{top:-8%}}
  100%{{top:108%}}
}}
@keyframes {uid}_star{{
  0%,100%{{opacity:0.2}} 50%{{opacity:1}}
}}
@keyframes {uid}_flicker{{
  0%,90%,100%{{opacity:1}} 92%,98%{{opacity:0.4}}
}}
@keyframes {uid}_shake{{
  0%,100%{{transform:translateX(0)}}
  20%    {{transform:translateX(-2px)}}
  40%    {{transform:translateX(2px)}}
  60%    {{transform:translateX(-1px)}}
  80%    {{transform:translateX(1px)}}
}}
@keyframes {uid}_ripple{{
  0%  {{transform:scale(0.8);opacity:0.8}}
  100%{{transform:scale(2.2);opacity:0}}
}}
@keyframes {uid}_pulse_ring{{
  0%,100%{{opacity:0.15;transform:scale(1)}}
  50%    {{opacity:0.45;transform:scale(1.04)}}
}}
@keyframes {uid}_bar_glow{{
  0%,100%{{box-shadow:0 0 4px {gl}}}
  50%    {{box-shadow:0 0 12px {gl},0 0 20px {gl}66}}
}}
@keyframes fadeInUp{{
  from{{opacity:0;transform:translateY(8px)}}
  to  {{opacity:1;transform:translateY(0)}}
}}
.metric-pill{{
  display:inline-block;
  font-size:0.52rem;letter-spacing:0.1em;
  padding:0.18rem 0.55rem;border-radius:99px;
  border:1px solid {bc}60;
  background:{sc}14;color:{sc};
  animation:fadeInUp 0.5s ease forwards;
}}
</style>""".replace("{uid}", uid).replace("{gl}", gl).replace("{bc}", bc).replace(
    "{bs}", p["breathe_scale"]).replace("{sc}", sc)

    # ── ANIMATED SCENE BACKGROUND ──────────────────────────────────────────────
    # Stars / particles for background
    star_svg = ""
    if p["scene_stars"]:
        import random
        random.seed(42)
        star_svg = f'<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;" viewBox="0 0 240 340">'
        for i in range(28):
            x   = random.randint(4, 236)
            y   = random.randint(4, 200)
            r   = round(random.uniform(0.6, 2.0), 1)
            dur = round(random.uniform(1.8, 4.5), 1)
            beg = round(random.uniform(0, 3.0), 1)
            star_svg += (
                f'<circle cx="{x}" cy="{y}" r="{r}" fill="{sc}" opacity="0.25">'
                f'<animate attributeName="opacity" values="0.1;0.9;0.1" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/>'
                f'</circle>'
            )
        star_svg += '</svg>'

    # Mountain silhouettes (healthy) / cracked ground (critical)
    scene_deco = ""
    if state == "pristine":
        scene_deco = f"""
<svg style="position:absolute;bottom:0;left:0;width:100%;height:55%;pointer-events:none;z-index:0;" viewBox="0 0 240 120" preserveAspectRatio="none">
  <polygon points="0,120 40,40 80,80 120,20 160,65 200,30 240,70 240,120" fill="{sc}10"/>
  <polygon points="0,120 30,60 70,95 110,35 150,75 190,45 240,80 240,120" fill="{sc}08"/>
  <polygon points="0,120 0,90 60,110 120,85 180,105 240,88 240,120" fill="{sc}0c"/>
</svg>"""
    elif state == "tired":
        scene_deco = f"""
<svg style="position:absolute;bottom:0;left:0;width:100%;height:40%;pointer-events:none;z-index:0;" viewBox="0 0 240 80" preserveAspectRatio="none">
  <polygon points="0,80 50,30 100,55 150,20 200,45 240,25 240,80" fill="{sc}10"/>
  <polygon points="0,80 0,60 80,70 160,58 240,65 240,80" fill="{sc}0a"/>
</svg>"""
    elif state == "sick":
        scene_deco = f"""
<svg style="position:absolute;bottom:0;left:0;width:100%;height:30%;pointer-events:none;z-index:0;" viewBox="0 0 240 60" preserveAspectRatio="none">
  <path d="M0,40 Q30,25 60,38 Q90,50 120,30 Q150,12 180,35 Q210,55 240,38 L240,60 L0,60 Z" fill="{sc}12"/>
  <path d="M20,60 L22,45 M60,60 L63,40 M110,60 L112,48 M170,60 L173,42 M210,60 L212,50" stroke="{sc}" stroke-width="0.8" opacity="0.3"/>
</svg>"""
    elif state == "critical":
        scene_deco = f"""
<svg style="position:absolute;bottom:0;left:0;width:100%;height:35%;pointer-events:none;z-index:0;" viewBox="0 0 240 70" preserveAspectRatio="none">
  <polygon points="0,70 240,70 240,50 0,50" fill="{sc}0a"/>
  <path d="M30,50 L38,35 L42,50 M80,50 L92,28 L98,50 M140,50 L148,38 L152,50 M190,50 L200,30 L205,50" stroke="{sc}" stroke-width="0.8" fill="none" opacity="0.4"/>
  <path d="M0,50 L8,42 L14,50 L20,40 L26,50" stroke="{sc}" stroke-width="0.7" fill="none" opacity="0.3"/>
  <path d="M220,50 L228,44 L234,50" stroke="{sc}" stroke-width="0.7" fill="none" opacity="0.3"/>
</svg>"""

    # ── SCAN LINE (only healthy — speed effect) ────────────────────────────────
    scan_line = ""
    if state == "pristine":
        scan_line = (
            f'<div style="position:absolute;left:0;width:100%;height:3px;'
            f'background:linear-gradient(90deg,transparent,{sc}88,transparent);'
            f'animation:{uid}_scan 1.8s linear infinite;pointer-events:none;z-index:6;"></div>'
        )
    elif state == "critical":
        scan_line = (
            f'<div style="position:absolute;left:0;width:100%;height:2px;'
            f'background:linear-gradient(90deg,transparent,{sc}55,transparent);'
            f'animation:{uid}_scan 6s linear infinite;pointer-events:none;z-index:6;"></div>'
        )

    # ── RIPPLE RINGS (pulse around card) ──────────────────────────────────────
    ripple = (
        f'<div style="position:absolute;inset:-8px;border-radius:22px;'
        f'border:2px solid {sc}30;'
        f'animation:{uid}_pulse_ring {p["pulse"]} ease-in-out infinite;'
        f'pointer-events:none;z-index:0;"></div>'
        f'<div style="position:absolute;inset:-16px;border-radius:26px;'
        f'border:1px solid {sc}18;'
        f'animation:{uid}_pulse_ring {p["pulse"]} ease-in-out infinite 0.5s;'
        f'pointer-events:none;z-index:0;"></div>'
    )

    # ── FLOATING PARTICLES over image ─────────────────────────────────────────
    particle_svg = ""
    if state == "pristine":
        particle_svg = f"""<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;overflow:visible;" viewBox="0 0 240 200">
  <circle cx="210" cy="90" r="4" fill="{sc}" opacity="0"><animate attributeName="cx" values="210;250;280" dur="0.65s" repeatCount="indefinite"/><animate attributeName="cy" values="90;72;58" dur="0.65s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.9;0.4;0" dur="0.65s" repeatCount="indefinite"/><animate attributeName="r" values="4;2;0.4" dur="0.65s" repeatCount="indefinite"/></circle>
  <circle cx="215" cy="115" r="3" fill="{sc}" opacity="0"><animate attributeName="cx" values="215;255;282" dur="0.75s" begin="0.2s" repeatCount="indefinite"/><animate attributeName="cy" values="115;100;90" dur="0.75s" begin="0.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.85;0.3;0" dur="0.75s" begin="0.2s" repeatCount="indefinite"/></circle>
  <circle cx="208" cy="140" r="3.5" fill="{sc}" opacity="0"><animate attributeName="cx" values="208;248;276" dur="0.6s" begin="0.45s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0.25;0" dur="0.6s" begin="0.45s" repeatCount="indefinite"/></circle>
  <ellipse cx="188" cy="178" rx="14" ry="5" fill="{sc}" opacity="0"><animate attributeName="cx" values="188;230;262" dur="0.85s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.45;0.12;0" dur="0.85s" repeatCount="indefinite"/><animate attributeName="ry" values="5;9;3" dur="0.85s" repeatCount="indefinite"/></ellipse>
  <ellipse cx="172" cy="182" rx="9" ry="3.5" fill="{sc}" opacity="0"><animate attributeName="cx" values="172;212;242" dur="0.7s" begin="0.38s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.38;0.1;0" dur="0.7s" begin="0.38s" repeatCount="indefinite"/></ellipse>
  <circle cx="105" cy="45" r="3" fill="{sc}" opacity="0"><animate attributeName="cy" values="45;8;-15" dur="1.3s" begin="0.15s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;0" dur="1.3s" begin="0.15s" repeatCount="indefinite"/><animate attributeName="r" values="3;1.4;0.2" dur="1.3s" begin="0.15s" repeatCount="indefinite"/></circle>
  <circle cx="140" cy="35" r="2.5" fill="{sc}" opacity="0"><animate attributeName="cy" values="35;2;-20" dur="1.5s" begin="0.65s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.9;0" dur="1.5s" begin="0.65s" repeatCount="indefinite"/></circle>
  <circle cx="75" cy="55" r="2" fill="{sc}" opacity="0"><animate attributeName="cy" values="55;18;-5" dur="1.1s" begin="1.1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.8;0" dur="1.1s" begin="1.1s" repeatCount="indefinite"/></circle>
</svg>"""
    elif state == "critical":
        particle_svg = """<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;" viewBox="0 0 240 200">
  <circle cx="148" cy="158" r="3.5" fill="#cc0000" opacity="0"><animate attributeName="cy" values="158;182;198" dur="2.0s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.8;0.35;0" dur="2.0s" repeatCount="indefinite"/></circle>
  <circle cx="162" cy="152" r="2.5" fill="#cc0000" opacity="0"><animate attributeName="cy" values="152;175;192" dur="2.6s" begin="0.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0.28;0" dur="2.6s" begin="0.8s" repeatCount="indefinite"/></circle>
  <circle cx="138" cy="160" r="2" fill="#990000" opacity="0"><animate attributeName="cy" values="160;180;196" dur="2.9s" begin="1.7s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.6;0.20;0" dur="2.9s" begin="1.7s" repeatCount="indefinite"/></circle>
  <circle cx="170" cy="148" r="1.8" fill="#aa0000" opacity="0"><animate attributeName="cy" values="148;170;188" dur="3.2s" begin="0.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.55;0.18;0" dur="3.2s" begin="0.4s" repeatCount="indefinite"/></circle>
</svg>"""
    elif state == "sick":
        particle_svg = f"""<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;" viewBox="0 0 240 200">
  <ellipse cx="155" cy="85" rx="7" ry="3" fill="#8a8a8a" opacity="0"><animate attributeName="cy" values="85;58;35" dur="3.4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.28;0" dur="3.4s" repeatCount="indefinite"/><animate attributeName="rx" values="7;12;18" dur="3.4s" repeatCount="indefinite"/></ellipse>
  <ellipse cx="142" cy="92" rx="5" ry="2.5" fill="#8a8a8a" opacity="0"><animate attributeName="cy" values="92;68;48" dur="4.1s" begin="1.1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.22;0" dur="4.1s" begin="1.1s" repeatCount="indefinite"/></ellipse>
  <ellipse cx="168" cy="80" rx="4" ry="2" fill="#7a7a7a" opacity="0"><animate attributeName="cy" values="80;55;35" dur="3.8s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.18;0" dur="3.8s" begin="2s" repeatCount="indefinite"/></ellipse>
</svg>"""
    elif state == "tired":
        particle_svg = f"""<svg style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:5;" viewBox="0 0 240 200">
  <circle cx="60" cy="60" r="2" fill="{sc}" opacity="0"><animate attributeName="cy" values="60;30;10" dur="3s" begin="0s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.5;0" dur="3s" repeatCount="indefinite"/></circle>
  <circle cx="180" cy="70" r="1.5" fill="{sc}" opacity="0"><animate attributeName="cy" values="70;45;22" dur="3.5s" begin="1.2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;0.4;0" dur="3.5s" begin="1.2s" repeatCount="indefinite"/></circle>
</svg>"""

    # ── ALERT BANNER (non-healthy states) ─────────────────────────────────────
    alert_html = ""
    if p["alert_text"]:
        anim = f"animation:{uid}_flicker 3s infinite;" if state == "critical" else ""
        if state == "critical":
            anim = f"animation:{uid}_shake 0.5s infinite;"
        alert_html = (
            f'<div style="margin:0.4rem 0 0.3rem;padding:0.28rem 0.6rem;border-radius:6px;'
            f'background:{p["alert_color"]}18;border:1px solid {p["alert_color"]}55;'
            f'font-size:0.58rem;color:{p["alert_color"]};letter-spacing:0.08em;{anim}">'
            + p["alert_text"] + '</div>'
        )

    # ── MINI STATS ROW ─────────────────────────────────────────────────────────
    stats_html = (
        '<div style="display:flex;gap:5px;margin:0.4rem 0;justify-content:center;">'
        + f'<div style="flex:1;background:{sc}12;border:1px solid {sc}30;border-radius:6px;padding:0.3rem 0.2rem;">'
        + f'<div style="font-size:0.48rem;color:{sc}99;letter-spacing:0.1em;text-transform:uppercase;">Scanned</div>'
        + f'<div style="font-size:1rem;font-family:Bebas Neue,sans-serif;color:{sc};line-height:1.1;">{total}</div></div>'
        + f'<div style="flex:1;background:#4ade8012;border:1px solid #4ade8030;border-radius:6px;padding:0.3rem 0.2rem;">'
        + f'<div style="font-size:0.48rem;color:#4ade8099;letter-spacing:0.1em;text-transform:uppercase;">Perfect</div>'
        + f'<div style="font-size:1rem;font-family:Bebas Neue,sans-serif;color:#4ade80;line-height:1.1;">{perfect_ct}</div></div>'
        + f'<div style="flex:1;background:#f8717112;border:1px solid #f8717130;border-radius:6px;padding:0.3rem 0.2rem;">'
        + f'<div style="font-size:0.48rem;color:#f8717199;letter-spacing:0.1em;text-transform:uppercase;">Issues</div>'
        + f'<div style="font-size:1rem;font-family:Bebas Neue,sans-serif;color:#f87171;line-height:1.1;">{issues_ct}</div></div>'
        + '</div>'
    )

    # ── HEALTH BAR ─────────────────────────────────────────────────────────────
    filled = round(score / 10)
    bar_segs = []
    for i in range(10):
        if i < filled:
            bar_anim = f"animation:{uid}_bar_glow 2s ease-in-out infinite {i*0.1}s;"
            s = f"background:{p['bar']};opacity:1;{bar_anim}"
        else:
            s = "background:#1e2130;opacity:0.35;"
        bar_segs.append(
            f'<div style="flex:1;height:7px;border-radius:4px;{s}transition:all 0.6s;"></div>'
        )
    bar_html = '<div style="display:flex;gap:3px;margin:0.4rem 0;">' + "".join(bar_segs) + '</div>'

    # ── IMAGE WRAPPER ──────────────────────────────────────────────────────────
    img_wrap = (
        f'<div style="position:relative;border-radius:14px;overflow:hidden;margin-bottom:0.45rem;'
        f'background:{p["scene_bg"]};">'
        # Animated background scene
        + star_svg + scene_deco + scan_line
        # The leopard image
        + f'<img src="data:image/jpeg;base64,{b64}" alt="Snow Leopard"'
        + f' style="width:100%;display:block;position:relative;z-index:2;'
        + f'filter:{p["img_filter"]};'
        + f'animation:{uid}_breathe {p["breathe"]} ease-in-out infinite,'
        + f'{uid}_float {p["pulse"]} ease-in-out infinite;'
        + f'transition:filter 1.2s ease;"/>'
        # Tint overlay
        + f'<div style="position:absolute;inset:0;z-index:3;pointer-events:none;'
        + f'background:{p["overlay"]};'
        + f'animation:{uid}_breathe {p["pulse"]} ease-in-out infinite;"></div>'
        # Vignette
        + f'<div style="position:absolute;inset:0;z-index:4;pointer-events:none;'
        + f'background:radial-gradient(ellipse at center,transparent 28%,{p["vignette"]} 100%);"></div>'
        # Particles
        + particle_svg
        + '</div>'
    )

    # ── SCORE ──────────────────────────────────────────────────────────────────
    score_html = (
        f'<div style="font-family:Bebas Neue,sans-serif;font-size:2.8rem;'
        f'letter-spacing:0.04em;color:{gl};line-height:1;'
        f'text-shadow:0 0 24px {gl}bb;margin:0.15rem 0;">'
        + str(score)
        + f'<span style="font-size:0.88rem;opacity:0.38;font-family:DM Mono,monospace;"> / 100</span></div>'
    )

    # ── BADGE ──────────────────────────────────────────────────────────────────
    badge_html = (
        f'<div style="margin:0.35rem 0 0.25rem;">'
        f'<span style="font-family:Bebas Neue,sans-serif;font-size:0.92rem;letter-spacing:0.18em;'
        f'background:{p["label_bg"]};color:{p["label"]};'
        f'padding:0.25rem 1.1rem;border-radius:6px;'
        f'border:1px solid {bc}88;box-shadow:0 0 14px {gl}66;">'
        + p["icon"] + " " + p["text"] + '</span></div>'
    )

    # ── MESSAGE ─────────────────────────────────────────────────────────────────
    msg_html = (
        f'<div style="font-size:0.58rem;color:#667088;margin-top:0.3rem;'
        f'line-height:1.5;padding:0 0.1rem;">{p["msg"]}</div>'
    )

    # ── LABEL ──────────────────────────────────────────────────────────────────
    label_html = (
        f'<div style="font-size:0.48rem;letter-spacing:0.24em;text-transform:uppercase;'
        f'color:#404655;margin-bottom:0.5rem;font-weight:600;">&#9674; SEO GUARDIAN</div>'
    )

    # ── CARD ───────────────────────────────────────────────────────────────────
    card_style = (
        f"position:relative;overflow:hidden;"
        f"background:linear-gradient(160deg,#08080e,#04040a);"
        f"border:1px solid {bc}66;"
        f"border-radius:18px;padding:1rem 0.85rem 0.9rem;"
        f"text-align:center;"
        f"animation:{uid}_pulse {p['pulse']} ease-in-out infinite;"
        f"transition:border-color 1.2s,box-shadow 1.2s;"
    )

    full_page = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'/>"
        "<link href='https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&display=swap' rel='stylesheet'/>"
        + css
        + "</head><body>"
        + f'<div style="{card_style}">'
        + ripple
        + label_html
        + img_wrap
        + badge_html
        + alert_html
        + bar_html
        + score_html
        + stats_html
        + msg_html
        + "</div></body></html>"
    )

    components.html(full_page, height=580, scrolling=False)


def render_summary(all_rows):
    """Combined end-of-page summary: Grade + Issue Breakdown + Action Plan."""

    total   = len(all_rows)
    if total == 0:
        return

    # ── Pull real colours from current theme FIRST (used in helpers below) ────
    T   = THEMES[st.session_state.get("theme", "Obsidian")]
    bg2 = T["bg2"]
    bg3 = T["bg3"]
    brd = T["border"]
    txt = T["text"]
    tx2 = T["text2"]
    tx3 = T["text3"]
    tx4 = T["text4"]
    hd  = T["heading"]
    acc = T["accent"]

    success = sum(1 for r in all_rows if not r["Error"])
    errors  = total - success

    # ── Compute issue counts ───────────────────────────────────────────────────
    title_issues = desc_issues = heading_issues = fetch_errors = perfect_ct = 0
    title_long = title_missing = desc_long = desc_missing = 0
    no_h1 = multi_h1 = no_h2 = 0

    for row in all_rows:
        if row["Error"]:
            fetch_errors += 1
            continue
        tlen = int(row["Title Length"])
        dlen = int(row["Description Length"])
        h1s  = [x for x in row["H1 Tags"].split(" | ") if x.strip()]
        h2s  = [x for x in row["H2 Tags"].split(" | ") if x.strip()]
        no_t = row["Meta Title"] in ("", "No title found")
        no_d = row["Meta Description"] in ("", "No description found")

        has_title_issue   = no_t or tlen > 60
        has_desc_issue    = no_d or dlen > 160
        has_heading_issue = len(h1s) != 1 or not h2s

        if has_title_issue:   title_issues += 1
        if has_desc_issue:    desc_issues  += 1
        if has_heading_issue: heading_issues += 1
        if no_t: title_missing += 1
        elif tlen > 60: title_long += 1
        if no_d: desc_missing += 1
        elif dlen > 160: desc_long += 1
        if len(h1s) == 0: no_h1 += 1
        elif len(h1s) > 1: multi_h1 += 1
        if not h2s: no_h2 += 1
        if not has_title_issue and not has_desc_issue and not has_heading_issue:
            perfect_ct += 1

    score, state = compute_health(all_rows)

    # ── Grade ──────────────────────────────────────────────────────────────────
    if score >= 90:   grade, grade_color, grade_bg = "A+", "#4ade80", "#14532d"
    elif score >= 80: grade, grade_color, grade_bg = "A",  "#4ade80", "#14532d"
    elif score >= 70: grade, grade_color, grade_bg = "B",  "#86efac", "#166534"
    elif score >= 60: grade, grade_color, grade_bg = "C",  "#fbbf24", "#451a03"
    elif score >= 45: grade, grade_color, grade_bg = "D",  "#fb923c", "#431407"
    elif score >= 25: grade, grade_color, grade_bg = "E",  "#f87171", "#450a0a"
    else:             grade, grade_color, grade_bg = "F",  "#ef4444", "#3d0000"

    state_msg = {
        "pristine": "Your SEO is in excellent shape. Keep it up!",
        "tired":    "A few issues are slowing your SEO down.",
        "sick":     "Multiple problems found — needs attention soon.",
        "critical": "Serious SEO issues detected — fix urgently!",
    }[state]

    # ── Bar widths (as % of total) ─────────────────────────────────────────────
    def pct(n): return round((n / total) * 100) if total > 0 else 0

    title_pct   = pct(title_issues)
    desc_pct    = pct(desc_issues)
    heading_pct = pct(heading_issues)
    error_pct   = pct(fetch_errors)
    perfect_pct = pct(perfect_ct)

    # ── Action plan items ──────────────────────────────────────────────────────
    actions = []
    if fetch_errors:
        actions.append(("🔴", "CRITICAL", f"{fetch_errors} URL(s) couldn't be scanned — check if they're live and accessible.", "#f87171", "#450a0a"))
    if title_missing:
        actions.append(("🔴", "FIX FIRST", f"{title_missing} page(s) have no Meta Title — add a unique title under 60 characters.", "#f87171", "#450a0a"))
    if desc_missing:
        actions.append(("🔴", "FIX FIRST", f"{desc_missing} page(s) have no Meta Description — write a compelling summary under 160 chars.", "#f87171", "#450a0a"))
    if no_h1:
        actions.append(("🟠", "FIX SOON", f"{no_h1} page(s) missing an H1 tag — every page needs exactly one H1 heading.", "#fb923c", "#431407"))
    if multi_h1:
        actions.append(("🟠", "FIX SOON", f"{multi_h1} page(s) have multiple H1 tags — keep it to exactly one H1 per page.", "#fb923c", "#431407"))
    if no_h2:
        actions.append(("🟠", "FIX SOON", f"{no_h2} page(s) have no H2 tags — add subheadings to improve content structure.", "#fb923c", "#431407"))
    if title_long:
        actions.append(("🟡", "IMPROVE", f"{title_long} Meta Title(s) exceed 60 chars — Google truncates long titles in search results.", "#fbbf24", "#451a03"))
    if desc_long:
        actions.append(("🟡", "IMPROVE", f"{desc_long} Meta Description(s) exceed 160 chars — shorten them to avoid truncation.", "#fbbf24", "#451a03"))
    if perfect_ct == total - fetch_errors and fetch_errors == 0:
        actions.append(("✅", "ALL GOOD", "Every scanned page passes all SEO checks. Excellent work!", "#4ade80", "#14532d"))
    elif perfect_ct > 0:
        actions.append(("✅", "KEEP IT UP", f"{perfect_ct} page(s) are already perfect — use them as a template for fixing others.", "#4ade80", "#14532d"))

    # ── Build HTML ─────────────────────────────────────────────────────────────
    def bar_row(label, count, pct_val, color, sub=""):
        sub_html = f'<span style="font-size:0.52rem;color:#666e88;margin-left:0.4rem;">{sub}</span>' if sub else ""
        return (
            f'<div style="margin-bottom:0.9rem;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.28rem;">'
            f'<span style="font-size:0.62rem;color:{tx2};letter-spacing:0.07em;">{label}{sub_html}</span>'
            f'<span style="font-size:0.7rem;font-family:Bebas Neue,sans-serif;color:{color};">{count}/{total}</span>'
            f'</div>'
            f'<div class="bar-track">'
            f'<div class="bar-fill" style="width:{pct_val}%;background:{color};box-shadow:0 0 7px {color}88;"></div>'
            f'</div>'
            f'</div>'
        )

    breakdown_html = (
        bar_row("Meta Title Issues",   title_issues,   title_pct,   "#fbbf24", f"{title_missing} missing · {title_long} too long") +
        bar_row("Meta Desc Issues",    desc_issues,    desc_pct,    "#fb923c", f"{desc_missing} missing · {desc_long} too long") +
        bar_row("Heading Issues",      heading_issues, heading_pct, "#f87171", f"{no_h1} no H1 · {multi_h1} multi H1 · {no_h2} no H2") +
        bar_row("Fetch Errors",        fetch_errors,   error_pct,   "#ef4444") +
        bar_row("✓ Perfect Pages",     perfect_ct,     perfect_pct, "#4ade80")
    )

    action_items_html = ""
    for emoji, priority, text, color, bg in actions:
        action_items_html += (
            f'<div style="display:flex;gap:0.8rem;align-items:flex-start;padding:0.72rem 0.9rem;'
            f'background:{bg}22;border:1px solid {color}40;border-left:3px solid {color};'
            f'border-radius:8px;margin-bottom:0.5rem;">'
            f'<span style="font-size:1rem;flex-shrink:0;">{emoji}</span>'
            f'<div>'
            f'<div style="font-size:0.56rem;font-weight:700;letter-spacing:0.12em;color:{color};margin-bottom:0.18rem;">{priority}</div>'
            f'<div style="font-size:0.64rem;color:{tx2};line-height:1.5;">{text}</div>'
            f'</div></div>'
        )

    total_label = f'{total} URL{"s" if total != 1 else ""} scanned'

    summary_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;font-family:'DM Mono',monospace;color:{txt};overflow-x:hidden}}
.card{{background:{bg2};border:1px solid {brd};border-radius:12px;padding:1.3rem 1.4rem}}
.label{{font-size:0.55rem;letter-spacing:0.18em;text-transform:uppercase;color:{tx3};margin-bottom:0.5rem;font-weight:600}}
.bar-track{{height:8px;background:#1e2130;border-radius:4px;overflow:hidden;margin-top:0.3rem}}
.bar-fill{{height:100%;border-radius:4px;transition:width 0.8s ease}}
.action-item{{display:flex;gap:0.8rem;align-items:flex-start;padding:0.7rem 0.9rem;border-radius:8px;margin-bottom:0.5rem;border-left:3px solid}}
.tip-card{{background:{bg3};border-radius:8px;padding:0.9rem}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}
.grid3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
.fade{{animation:fadeIn 0.6s ease forwards}}
</style>
</head><body>

<!-- HEADER -->
<div style="border-bottom:1px solid {brd};padding-bottom:1rem;margin-bottom:1.8rem;" class="fade">
  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.9rem;letter-spacing:0.06em;color:{hd};">SEO Health Report</div>
  <div style="font-size:0.58rem;letter-spacing:0.15em;text-transform:uppercase;color:{tx4};margin-top:0.3rem;">Full audit summary · {total_label}</div>
</div>

<!-- GRADE + SUMMARY ROW -->
<div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap;" class="fade">

  <!-- Grade -->
  <div style="flex:0 0 auto;background:{bg2};border:1px solid {brd};border-radius:12px;
              padding:1.4rem 2rem;text-align:center;box-shadow:0 0 28px {grade_color}22;">
    <div class="label">Overall Grade</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4.8rem;color:{grade_color};
                line-height:1;text-shadow:0 0 28px {grade_color}88;">{grade}</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.5rem;color:{grade_color};opacity:0.65;margin-top:0.2rem;">{score}/100</div>
  </div>

  <!-- Summary card -->
  <div style="flex:1;min-width:180px;background:{bg2};border:1px solid {brd};border-radius:12px;
              padding:1.2rem 1.4rem;display:flex;flex-direction:column;justify-content:center;">
    <div class="label">Summary</div>
    <div style="font-size:0.84rem;color:{hd};line-height:1.6;font-weight:500;">{state_msg}</div>
    <div style="display:flex;gap:1.2rem;margin-top:1rem;flex-wrap:wrap;">
      <span style="font-size:0.62rem;color:#4ade80;">✓ {perfect_ct} Perfect</span>
      <span style="font-size:0.62rem;color:#fbbf24;">⚠ {title_issues + desc_issues + heading_issues} Issues</span>
      <span style="font-size:0.62rem;color:#f87171;">✗ {fetch_errors} Errors</span>
    </div>
  </div>

</div>

<!-- BREAKDOWN + ACTION PLAN -->
<div class="grid2" style="margin-bottom:1rem;">

  <!-- Issue Breakdown -->
  <div class="card">
    <div class="label" style="margin-bottom:1rem;">Issue Breakdown</div>
    {breakdown_html}
  </div>

  <!-- Action Plan -->
  <div class="card">
    <div class="label" style="margin-bottom:1rem;">Action Plan</div>
    {action_items_html}
  </div>

</div>

<!-- QUICK REFERENCE -->
<div class="card" style="margin-top:1rem;">
  <div class="label" style="margin-bottom:1rem;">SEO Quick Reference</div>
  <div class="grid3">
    <div class="tip-card">
      <div style="font-size:0.58rem;color:#fbbf24;font-weight:700;letter-spacing:0.1em;margin-bottom:0.45rem;">META TITLE</div>
      <div style="font-size:0.62rem;color:{tx2};line-height:1.65;">
        Keep under <strong style="color:{hd};">60 characters</strong>.<br/>
        Include your primary keyword.<br/>
        Make it unique per page.
      </div>
    </div>
    <div class="tip-card">
      <div style="font-size:0.58rem;color:#fb923c;font-weight:700;letter-spacing:0.1em;margin-bottom:0.45rem;">META DESCRIPTION</div>
      <div style="font-size:0.62rem;color:{tx2};line-height:1.65;">
        Keep under <strong style="color:{hd};">160 characters</strong>.<br/>
        Summarise the page clearly.<br/>
        Include a call to action.
      </div>
    </div>
    <div class="tip-card">
      <div style="font-size:0.58rem;color:#f87171;font-weight:700;letter-spacing:0.1em;margin-bottom:0.45rem;">HEADING STRUCTURE</div>
      <div style="font-size:0.62rem;color:{tx2};line-height:1.65;">
        Use <strong style="color:{hd};">exactly one H1</strong> per page.<br/>
        Use H2s to organise sections.<br/>
        Keep a clear heading hierarchy.
      </div>
    </div>
  </div>
</div>

</body></html>"""

    # Estimate height: base 620 + 55 per action item
    est_height = 680 + len(actions) * 62
    components.html(summary_html, height=est_height, scrolling=True)


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
        render_summary(all_rows)


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
