"""Tampilan bersama: CSS, navigasi atas, dan komponen kecil (gaya 'company profile')."""
import streamlit as st

BRAND = "StayCheck"          # ganti sesuai nama proyek kelompok
TAGLINE = "Prediksi pembatalan booking hotel"
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0F172A"/><path d="M16 48V22a6 6 0 0 1 6-6h20a6 6 0 0 1 6 6v26" fill="#0284C7"/><rect x="22" y="22" width="7" height="7" rx="2" fill="#E0F2FE"/><rect x="35" y="22" width="7" height="7" rx="2" fill="#E0F2FE"/><rect x="22" y="33" width="7" height="7" rx="2" fill="#E0F2FE"/><rect x="35" y="33" width="7" height="7" rx="2" fill="#38BDF8"/><rect x="28" y="42" width="8" height="6" rx="1.5" fill="#F8FAFC"/></svg>"""

# Edit sebelum dikumpulkan: nama, NIM, dan peran masing-masing anggota
TEAM = [
    {"nama": "Anggota 1", "nim": "NIM", "peran": "Data: dataset, EDA, preprocessing"},
    {"nama": "Anggota 2", "nim": "NIM", "peran": "Model: training, tuning, evaluasi"},
    {"nama": "Anggota 3", "nim": "NIM", "peran": "Aplikasi: Streamlit dan dokumentasi"},
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');
:root{--ink:#0F172A;--lagoon:#10B981;--accent:#0284C7;--mist:#E2E8F0;--line:#CBD5E1;--brass:#0EA5E9;--paper:#FFFFFF;--risk:#EF4444;--muted:#475569;--ice:#F1F5F9;}
.stApp{font-family:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:linear-gradient(180deg,#E2E8F0 0%,#F1F5F9 320px,#F1F5F9 100%);}
.stApp h1,.stApp h2,.stApp h3,.brand,.display{font-family:'Bricolage Grotesque','Figtree',system-ui,sans-serif;letter-spacing:-0.02em;color:var(--ink);}
.stApp h2{font-size:1.9rem;font-weight:700;margin-top:2.4rem;}
.stApp h3{font-size:1.25rem;font-weight:700;}
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"],[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapseButton"]{display:none;}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}
.block-container{max-width:1120px;padding-top:4.4rem;padding-bottom:4rem;}
.st-key-topbar{position:relative;z-index:1000001;}
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
.cta,.ghost{display:inline-block;border-radius:999px;padding:.75rem 1.4rem;font-weight:600;text-decoration:none;margin-right:.6rem;transition:transform .15s ease,box-shadow .15s ease;}
.cta{background:var(--accent);color:#FFFFFF!important;box-shadow:0 6px 18px rgba(2,132,199,.25);}
.cta:hover{background:#0369A1;}
.ghost{border:2px solid var(--ink);color:var(--ink)!important;background:rgba(255,255,255,.65);}
.hero-card{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:1.25rem 1.35rem;box-shadow:0 12px 32px rgba(15,23,42,.06);}
.hero-photo{position:relative;border-radius:14px;overflow:hidden;height:155px;margin-bottom:1rem;background:#0F172A;}
.hero-photo img{width:100%;height:100%;object-fit:cover;display:block;opacity:.88;}
.hero-photo .badge{position:absolute;bottom:10px;left:12px;background:rgba(15,23,42,.82);color:#F8FAFC;font-size:.78rem;font-weight:600;padding:.28rem .7rem;border-radius:999px;backdrop-filter:blur(4px);border:1px solid rgba(56,189,248,.35);}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:6px;width:100%;}
.dots i{aspect-ratio:1;border-radius:5px;background:var(--mist);display:block;}
.dots i.on{background:var(--brass);}
.viz-cap{margin:.85rem 0 0;font-size:1.02rem;line-height:1.45;}
.viz-cap b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.4rem;color:var(--accent);}
.viz-note{color:var(--muted);font-size:.82rem;margin:.25rem 0 0;}

.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem;margin-top:1rem;}
.step{background:var(--paper);border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:14px;padding:1.1rem 1.25rem;box-shadow:0 4px 14px rgba(15,23,42,.03);}
.step h4{font-family:'Bricolage Grotesque',sans-serif;font-size:1.18rem;margin:0 0 .35rem;}
.step p{margin:0;color:var(--muted);line-height:1.55;}

.band{background:linear-gradient(135deg,#0F172A 0%,#1E293B 100%);color:#fff;border-radius:22px;padding:2rem 2.2rem;margin-top:1rem;box-shadow:0 14px 34px rgba(15,23,42,.14);}
.band h2,.band h3{color:#fff!important;margin-top:0;}
.band .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:1rem;}
.band .num{font-family:'Bricolage Grotesque',sans-serif;font-size:2.8rem;font-weight:800;color:#38BDF8;line-height:1;}
.band p{color:#CBD5E1;line-height:1.5;margin:.4rem 0 0;}
.band>p{margin-top:1.6rem;}

.photo-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.4rem;margin-top:1rem;}
.photo-card{background:var(--paper);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 6px 20px rgba(15,23,42,.05);}
.photo-card img{width:100%;height:190px;object-fit:cover;display:block;}
.photo-card .pc-body{padding:1.1rem 1.3rem;}
.photo-card .pc-tag{display:inline-block;font-size:.76rem;font-weight:600;padding:.2rem .65rem;border-radius:999px;background:#E0F2FE;color:#0369A1;margin-bottom:.45rem;}
.photo-card h4{font-family:'Bricolage Grotesque',sans-serif;font-size:1.22rem;margin:0 0 .35rem;color:var(--ink);}
.photo-card p{margin:0;color:var(--muted);font-size:.92rem;line-height:1.55;}

.team{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-top:1rem;}
.member{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:1.1rem 1.2rem;box-shadow:0 4px 12px rgba(15,23,42,.03);}
.member b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.15rem;}
.member span{display:block;color:var(--muted);font-size:.92rem;margin-top:.2rem;}

.panel-empty{background:rgba(255,255,255,.7);border:2px dashed var(--line);border-radius:18px;padding:2rem 1.6rem;color:var(--muted);line-height:1.6;}
.panel-empty b{color:var(--ink);font-family:'Bricolage Grotesque',sans-serif;font-size:1.3rem;display:block;margin-bottom:.4rem;}
.result{background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:1.5rem 1.6rem;box-shadow:0 10px 28px rgba(15,23,42,.06);}
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
.gauge .tick{position:absolute;top:-6px;bottom:-6px;width:4px;border-radius:2px;background:#F59E0B;}
.g-note{color:var(--muted);font-size:.88rem;}
.r-text{margin:1rem 0 0;line-height:1.6;}
.r-zone{display:inline-block;margin-top:.55rem;padding:.22rem .7rem;border-radius:999px;font-size:.82rem;font-weight:600;background:var(--mist);color:var(--ink);}
.result.warn .r-zone{background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;}
.result.ok .r-zone{background:#ECFDF5;color:#059669;border:1px solid #A7F3D0;}
.r-zone.near{background:#FFFBEB;color:#B45309;border:1px solid #FDE68A;}
.r-drivers{margin-top:1.1rem;padding-top:.9rem;border-top:1px solid var(--line);}
.r-drivers h4{font-family:'Bricolage Grotesque',sans-serif;font-size:1.02rem;margin:0 0 .45rem;}
.r-drivers ul{list-style:none;padding:0;margin:0;display:grid;gap:.35rem;}
.r-drivers li{display:flex;justify-content:space-between;align-items:baseline;gap:.75rem;font-size:.88rem;padding:.35rem .65rem;border-radius:10px;background:#F8FAFC;border:1px solid #E2E8F0;}
.r-drivers li b{font-weight:600;color:var(--ink);}
.r-drivers .d-up{color:#DC2626;font-weight:600;white-space:nowrap;}
.r-drivers .d-down{color:#059669;font-weight:600;white-space:nowrap;}
.r-drivers .d-flat{color:var(--muted);white-space:nowrap;}
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
 .steps,.band .grid,.team,.photo-grid{grid-template-columns:1fr;}
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
