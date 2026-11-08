"""Tampilan bersama: CSS, navigasi atas, dan komponen kecil (gaya 'company profile')."""
import streamlit as st

BRAND = "StayCheck"          # ganti sesuai nama proyek kelompok
TAGLINE = "Prediksi pembatalan booking hotel"

# Edit sebelum dikumpulkan: nama, NIM, dan peran masing-masing anggota
TEAM = [
    {"nama": "Anggota 1", "nim": "NIM", "peran": "Data: dataset, EDA, preprocessing"},
    {"nama": "Anggota 2", "nim": "NIM", "peran": "Model: training, tuning, evaluasi"},
    {"nama": "Anggota 3", "nim": "NIM", "peran": "Aplikasi: Streamlit dan dokumentasi"},
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');
:root{--ink:#10233A;--lagoon:#1D7A8C;--mist:#EAF1F6;--line:#D3E0E9;--brass:#E8A317;--paper:#FFFFFF;--risk:#B4410B;--muted:#4A5B6D;}
.stApp{font-family:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);}
.stApp h1,.stApp h2,.stApp h3,.brand,.display{font-family:'Bricolage Grotesque','Figtree',system-ui,sans-serif;letter-spacing:-0.02em;color:var(--ink);}
.stApp h2{font-size:1.9rem;font-weight:700;margin-top:2.4rem;}
.stApp h3{font-size:1.25rem;font-weight:700;}
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"],[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapseButton"]{display:none;}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}
.block-container{max-width:1120px;padding-top:1rem;padding-bottom:4rem;}
a:focus-visible,button:focus-visible{outline:3px solid var(--brass);outline-offset:2px;}

.brand{font-size:1.5rem;font-weight:800;line-height:1.1;margin:.2rem 0 0;}
.brand small{display:block;font-family:'Figtree',sans-serif;font-weight:500;font-size:.8rem;color:var(--muted);letter-spacing:0;}
[data-testid="stPageLink"] a{border-radius:999px;padding:.35rem .9rem;font-weight:600;}
[data-testid="stPageLink"] a[aria-current="page"]{background:var(--ink);}
[data-testid="stPageLink"] a[aria-current="page"] p{color:#fff;}

.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:3rem;align-items:center;padding:2.6rem 0 1.4rem;}
.hero h1{font-size:3.6rem;line-height:1.03;font-weight:800;margin:0 0 1rem;}
.hero p.lead{font-size:1.15rem;line-height:1.6;color:var(--muted);max-width:34rem;margin:0 0 1.6rem;}
.stApp .cta,.stApp .ghost{text-decoration:none!important;}
.cta,.ghost{display:inline-block;border-radius:999px;padding:.75rem 1.4rem;font-weight:600;text-decoration:none;margin-right:.6rem;}
.cta{background:var(--brass);color:var(--ink)!important;}
.ghost{border:2px solid var(--ink);color:var(--ink)!important;}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:7px;width:min(100%,380px);}
.dots i{aspect-ratio:1;border-radius:6px;background:var(--line);display:block;}
.dots i.on{background:var(--brass);}
.viz-cap{margin:1rem 0 0;font-size:1.05rem;line-height:1.5;}
.viz-cap b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.5rem;}
.viz-note{color:var(--muted);font-size:.85rem;}

.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6rem;margin-top:1rem;}
.step{border-top:4px solid var(--brass);padding-top:.8rem;}
.step h4{font-family:'Bricolage Grotesque',sans-serif;font-size:1.2rem;margin:0 0 .35rem;}
.step p{margin:0;color:var(--muted);line-height:1.55;}

.band{background:var(--ink);color:#fff;border-radius:22px;padding:2rem 2.2rem;margin-top:1rem;}
.band h2,.band h3{color:#fff!important;margin-top:0;}
.band .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:1rem;}
.band .num{font-family:'Bricolage Grotesque',sans-serif;font-size:2.8rem;font-weight:800;color:var(--brass);line-height:1;}
.band p{color:#D7E3EB;line-height:1.5;margin:.4rem 0 0;}
.band>p{margin-top:1.6rem;}

.team{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-top:1rem;}
.member{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:1.1rem 1.2rem;}
.member b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.15rem;}
.member span{display:block;color:var(--muted);font-size:.92rem;margin-top:.2rem;}

.panel-empty{border:2px dashed var(--line);border-radius:18px;padding:2rem 1.6rem;color:var(--muted);line-height:1.6;}
.panel-empty b{color:var(--ink);font-family:'Bricolage Grotesque',sans-serif;font-size:1.3rem;display:block;margin-bottom:.4rem;}
.result{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:1.5rem 1.6rem;}
.result.warn{border-left:10px solid var(--risk);}
.result.ok{border-left:10px solid var(--lagoon);}
.r-tag{font-family:'Bricolage Grotesque',sans-serif;font-size:1.45rem;font-weight:700;}
.result.warn .r-tag{color:var(--risk);}
.result.ok .r-tag{color:var(--lagoon);}
.r-num{font-family:'Bricolage Grotesque',sans-serif;font-size:4rem;font-weight:800;line-height:1;margin-top:.6rem;}
.r-num span{font-size:2rem;}
.r-sub{color:var(--muted);margin-top:.2rem;}
.gauge{position:relative;height:14px;border-radius:7px;background:var(--mist);margin:1.1rem 0 .5rem;}
.gauge .fill{height:100%;border-radius:7px;background:var(--lagoon);transition:width .6s ease;}
.result.warn .gauge .fill{background:var(--risk);}
.gauge .tick{position:absolute;top:-6px;bottom:-6px;width:4px;border-radius:2px;background:var(--brass);}
.g-note{color:var(--muted);font-size:.88rem;}
.r-text{margin:1rem 0 0;line-height:1.6;}
.fine{color:var(--muted);font-size:.85rem;line-height:1.5;}

.st-key-topbar [data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;align-items:center;gap:.5rem;}
.st-key-topbar [data-testid="stColumn"]{min-width:0!important;}
.st-key-topbar [data-testid="stColumn"]:first-child{flex:1 1 auto!important;width:auto!important;}
.st-key-topbar [data-testid="stColumn"]:last-child{flex:0 0 auto!important;width:auto!important;}
.st-key-nav_desktop{flex-direction:row!important;gap:.3rem!important;justify-content:flex-end;align-items:center;}
.st-key-nav_desktop>div{width:auto!important;}
.st-key-nav_mobile{display:none!important;}
.st-key-nav_mobile button{border-radius:999px;font-size:1.35rem;line-height:1;padding:.35rem .9rem;}
[data-testid="stMetricValue"],[data-testid="stMetricValue"] *{font-size:1.7rem!important;white-space:normal!important;overflow:visible!important;text-overflow:clip!important;line-height:1.2;}

@media (max-width:820px){
 .st-key-nav_desktop{display:none!important;}
 .st-key-nav_mobile{display:flex!important;justify-content:flex-end;}
 .block-container{padding-left:1.1rem;padding-right:1.1rem;}
 .brand{font-size:1.3rem;}
 .brand small{font-size:.75rem;}
 .hero{grid-template-columns:1fr;gap:1.6rem;padding:1.4rem 0 .6rem;}
 .hero h1{font-size:2.15rem;line-height:1.08;margin-bottom:.7rem;}
 .hero p.lead{font-size:1rem;line-height:1.55;margin-bottom:1.2rem;}
 .hero-cta{display:flex;flex-direction:column;gap:.6rem;}
 .hero-cta .cta,.hero-cta .ghost{display:block;text-align:center;margin:0;padding:.8rem 1rem;}
 .dots{width:min(100%,280px);gap:5px;}
 .viz-cap{font-size:.98rem;}
 .stApp h2{font-size:1.5rem;margin-top:1.8rem;}
 .steps,.band .grid,.team{grid-template-columns:1fr;}
 .band{padding:1.4rem 1.3rem;}
 .band .num{font-size:2.2rem;}
 .r-num{font-size:3.2rem;}
}
@media (prefers-reduced-motion:reduce){.gauge .fill{transition:none;}}
"""


def inject_css():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def html(s: str):
    """Render HTML tanpa baris kosong/indentasi (markdown memotong blok HTML pada baris kosong)."""
    st.markdown("\n".join(line.strip() for line in s.strip().splitlines() if line.strip()), unsafe_allow_html=True)


NAV = [("app.py", "Beranda"), ("pages/1_Model_Evaluation.py", "Evaluasi model"),
       ("pages/2_About_Project.py", "Tentang proyek")]


def _links():
    for path, label in NAV:
        try:
            st.page_link(path, label=label)
        except Exception:
            st.write(label)


def top_nav():
    """Desktop: tautan sejajar di kanan. Layar kecil: tombol burger (popover) berisi tautan yang sama."""
    with st.container(key="topbar"):
        c0, c1 = st.columns([1, 1])
        c0.markdown(f'<div class="brand">{BRAND}<small>{TAGLINE}</small></div>', unsafe_allow_html=True)
        with c1:
            with st.container(key="nav_desktop"):
                _links()
            with st.container(key="nav_mobile"):
                try:
                    with st.popover("☰"):
                        _links()
                except Exception:
                    _links()


def team_html():
    cards = "".join(f'<div class="member"><b>{m["nama"]}</b><span>{m["nim"]}</span><span>{m["peran"]}</span></div>'
                    for m in TEAM)
    return f'<div class="team">{cards}</div>'
