"""Tampilan bersama: CSS, navigasi atas, dan komponen kecil (gaya 'company profile')."""
import base64
import mimetypes
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
TEAM_DIR = BASE_DIR / "assets" / "team"

BRAND = "StayCheck"          # ganti sesuai nama proyek kelompok
TAGLINE = "Prediksi pembatalan booking hotel"
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0F172A"/><path d="M16 48V22a6 6 0 0 1 6-6h20a6 6 0 0 1 6 6v26" fill="#0284C7"/><rect x="22" y="22" width="7" height="7" rx="2" fill="#E0F2FE"/><rect x="35" y="22" width="7" height="7" rx="2" fill="#E0F2FE"/><rect x="22" y="33" width="7" height="7" rx="2" fill="#E0F2FE"/><rect x="35" y="33" width="7" height="7" rx="2" fill="#38BDF8"/><rect x="28" y="42" width="8" height="6" rx="1.5" fill="#F8FAFC"/></svg>"""

# Cara ganti foto anggota:
# 1) Taruh file foto di folder `assets/team/` dengan nama `nala.jpg`/`nala.png`, `ammar.jpg`/`ammar.png`,
#    atau `deandra.jpg`/`deandra.png` (otomatis menggantikan placeholder SVG), ATAU
# 2) Ubah nilai `"foto"` di bawah ke path file lokal (misal `"assets/team/foto_nala.jpg"`) atau URL gambar.
TEAM = [
    {
        "nama": "Nala Arham Rozana",
        "nim": "J0404241077",
        "peran": "Data: dataset, EDA, preprocessing",
        "foto": "assets/team/nala.svg",
    },
    {
        "nama": "Ammar Hudzafah",
        "nim": "J0404241026",
        "peran": "Model: training, tuning, evaluasi",
        "foto": "assets/team/ammar.svg",
    },
    {
        "nama": "Deandra Aidila Hidayat",
        "nim": "J0404241146",
        "peran": "Aplikasi: Streamlit dan dokumentasi",
        "foto": "assets/team/deandra.svg",
    },
]


def resolve_photo(foto_path: str) -> str:
    """Mendukung path file lokal (JPG/PNG/WEBP/SVG) maupun URL http(s).
    Jika ada file foto asli (.jpg/.jpeg/.png/.webp) dengan nama yang sama di `assets/team/`,
    file foto asli tersebut otomatis diprioritaskan di atas placeholder .svg.
    """
    if not foto_path:
        return ""
    if foto_path.startswith(("http://", "https://", "data:")):
        return foto_path
    p = Path(foto_path)
    if not p.is_absolute():
        p = BASE_DIR / p
    # Prioritaskan foto asli (.jpg/.jpeg/.png/.webp) bila pengguna menaruhnya di folder yang sama
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        cand = p.with_suffix(ext)
        if cand.exists():
            p = cand
            break
    if not p.exists():
        return foto_path
    mime, _ = mimetypes.guess_type(str(p))
    if p.suffix.lower() == ".svg":
        mime = "image/svg+xml"
    elif not mime:
        mime = "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');
:root{--ink:#0F172A;--lagoon:#10B981;--accent:#0284C7;--mist:#CFDFEE;--line:#94A3B8;--brass:#0EA5E9;--paper:rgba(244,248,252,.92);--risk:#EF4444;--muted:#334155;--ice:#DCE6F2;}
@keyframes bgDrift{0%{background-position:0% 0%,100% 0%,0% 0%;}50%{background-position:100% 60%,0% 100%,0% 0%;}100%{background-position:0% 0%,100% 0%,0% 0%;}}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px);}to{opacity:1;transform:translateY(0);}}
@keyframes pulseDot{0%,100%{transform:scale(1);opacity:1;}50%{transform:scale(1.08);opacity:.82;}}
@keyframes slideShow4{
  0%,20%{opacity:1;transform:scale(1);}
  25%,95%{opacity:0;transform:scale(1.05);}
  100%{opacity:1;transform:scale(1);}
}
@keyframes dotActive4{
  0%,20%{background:#38BDF8;width:22px;}
  25%,100%{background:rgba(255,255,255,.45);width:7px;}
}
.stApp{font-family:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background-color:#DCE6F2;background-image:linear-gradient(rgba(15,23,42,.032) 1px,transparent 1px),linear-gradient(90deg,rgba(15,23,42,.032) 1px,transparent 1px),radial-gradient(circle at 12% 14%,rgba(56,189,248,.22),transparent 38%),radial-gradient(circle at 88% 26%,rgba(99,102,241,.16),transparent 42%),linear-gradient(145deg,#CBD8E8 0%,#DCE6F2 48%,#C9DBEE 100%);background-size:36px 36px,36px 36px,160% 160%,160% 160%,100% 100%;}
[data-testid="stVerticalBlockBorderWrapper"]{background:var(--paper);border:1px solid rgba(148,163,184,.55)!important;border-radius:18px!important;box-shadow:0 10px 26px rgba(15,23,42,.06);backdrop-filter:blur(8px);}
.stApp h1,.stApp h2,.stApp h3,.brand,.display{font-family:'Bricolage Grotesque','Figtree',system-ui,sans-serif;letter-spacing:-0.02em;color:var(--ink);}
.stApp h2{font-size:1.9rem;font-weight:700;margin-top:2.2rem;}
.stApp h3{font-size:1.25rem;font-weight:700;}
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"],[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapseButton"]{display:none;}
#MainMenu,footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;height:1.5rem;}
.block-container{max-width:1120px;padding-top:1.8rem;padding-bottom:4rem;}
.st-key-topbar{position:relative;z-index:1000001;padding-bottom:.4rem;border-bottom:1px solid rgba(148,163,184,.35);margin-bottom:.4rem;}
a:focus-visible,button:focus-visible{outline:3px solid var(--brass);outline-offset:2px;}

.brand{font-size:1.5rem;font-weight:800;line-height:1.1;margin:.2rem 0 0;}
.brand small{display:block;font-family:'Figtree',sans-serif;font-weight:500;font-size:.8rem;color:var(--muted);letter-spacing:0;}
[data-testid="stPageLink"] a{border-radius:999px;padding:.35rem .9rem;font-weight:600;}
[data-testid="stPageLink"] a[aria-current="page"]{background:var(--ink);}
[data-testid="stPageLink"] a[aria-current="page"] p{color:#fff;}

.hero{display:grid;grid-template-columns:1.12fr .88fr;gap:2.4rem;align-items:center;padding:1.1rem 0 1.2rem;animation:fadeUp .55s ease-out both;}
.hero-kicker{display:inline-flex;align-items:center;background:#E2E8F0;color:#0F172A;font-size:.78rem;font-weight:600;padding:.32rem .85rem;border-radius:999px;margin-bottom:.85rem;border:1px solid #CBD5E1;}
.hero h1{font-size:3.35rem;line-height:1.04;font-weight:800;margin:0 0 .85rem;}
.hero p.lead{font-size:1.1rem;line-height:1.6;color:var(--muted);max-width:34rem;margin:0 0 1.3rem;}
.stApp .cta,.stApp .ghost{text-decoration:none!important;}
.cta,.ghost{display:inline-block;border-radius:999px;padding:.72rem 1.35rem;font-weight:600;text-decoration:none;margin-right:.55rem;transition:transform .2s cubic-bezier(.22,1,.36,1),box-shadow .2s ease,background .2s ease;}
.cta{background:var(--accent);color:#FFFFFF!important;box-shadow:0 6px 18px rgba(2,132,199,.22);}
.cta:hover{background:#0369A1;transform:translateY(-2px);box-shadow:0 10px 24px rgba(2,132,199,.3);}
.ghost{border:2px solid var(--ink);color:var(--ink)!important;background:rgba(241,245,249,.75);}
.ghost:hover{background:var(--ink);color:#FFFFFF!important;transform:translateY(-2px);}
.hero-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin-top:1.35rem;padding-top:1.1rem;border-top:1px solid rgba(148,163,184,.45);}
.h-stat{background:rgba(255,255,255,.62);border:1px solid rgba(148,163,184,.5);border-radius:13px;padding:.6rem .8rem;backdrop-filter:blur(6px);}
.h-stat b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:1.25rem;color:var(--ink);line-height:1.1;}
.h-stat span{display:block;font-size:.76rem;color:var(--muted);margin-top:.15rem;}

.hero-card{background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:1.2rem 1.3rem;box-shadow:0 14px 34px rgba(15,23,42,.1);backdrop-filter:blur(10px);transition:transform .25s ease,box-shadow .25s ease;}
.hero-card:hover{transform:translateY(-4px);box-shadow:0 20px 42px rgba(15,23,42,.14);}
.hero-carousel{position:relative;border-radius:15px;overflow:hidden;height:185px;margin-bottom:1rem;background:#0F172A;}
.hero-carousel .c-slide{position:absolute;inset:0;opacity:0;animation:slideShow4 20s infinite;}
.hero-carousel .c-slide:nth-child(1){animation-delay:0s;}
.hero-carousel .c-slide:nth-child(2){animation-delay:5s;}
.hero-carousel .c-slide:nth-child(3){animation-delay:10s;}
.hero-carousel .c-slide:nth-child(4){animation-delay:15s;}
.hero-carousel .c-slide img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.9);}
.hero-carousel .c-slide::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(15,23,42,.82) 100%);}
.hero-carousel .c-cap{position:absolute;bottom:11px;left:12px;right:78px;z-index:2;color:#F8FAFC;font-size:.78rem;font-weight:600;line-height:1.3;text-shadow:0 1px 4px rgba(0,0,0,.5);}
.hero-carousel .c-cap small{display:block;color:#BAE6FD;font-size:.7rem;font-weight:500;}
.hero-carousel .c-dots{position:absolute;bottom:14px;right:12px;z-index:3;display:flex;gap:5px;align-items:center;}
.hero-carousel .c-dots i{height:7px;width:7px;border-radius:999px;background:rgba(255,255,255,.45);display:block;animation:dotActive4 20s infinite;transition:width .3s ease;}
.hero-carousel .c-dots i:nth-child(1){animation-delay:0s;}
.hero-carousel .c-dots i:nth-child(2){animation-delay:5s;}
.hero-carousel .c-dots i:nth-child(3){animation-delay:10s;}
.hero-carousel .c-dots i:nth-child(4){animation-delay:15s;}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:6px;width:100%;}
.dots i{aspect-ratio:1;border-radius:5px;background:rgba(148,163,184,.38);display:block;transition:transform .2s ease;}
.dots i.on{background:var(--accent);}
.dots i:hover{transform:scale(1.15);}
.viz-cap{margin:.85rem 0 0;font-size:1.02rem;line-height:1.45;}
.viz-cap b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.4rem;color:var(--accent);}
.viz-note{color:var(--muted);font-size:.82rem;margin:.25rem 0 0;}

/* Alur kerja editorial asimetris (bukan 3 kotak rata) */
.how-wrap{display:grid;grid-template-columns:.88fr 1.12fr;gap:1.6rem;align-items:stretch;margin-top:1rem;}
.how-side{background:#0F172A;color:#F8FAFC;border-radius:20px;padding:1.6rem 1.65rem;display:flex;flex-direction:column;justify-content:space-between;box-shadow:0 12px 28px rgba(15,23,42,.12);}
.how-side .hs-kicker{display:inline-block;font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:#E0F2FE;background:#1E293B;padding:.24rem .65rem;border-radius:999px;width:fit-content;margin-bottom:.7rem;}
.how-side h3{color:#FFFFFF!important;font-size:1.55rem;line-height:1.2;margin:0 0 .6rem;}
.how-side p{color:#CBD5E1;font-size:.94rem;line-height:1.55;margin:0;}
.how-side .hs-chips{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1.2rem;}
.how-side .hs-chips span{font-size:.76rem;font-weight:600;color:#E0F2FE;background:#1E293B;border:1px solid #334155;padding:.24rem .65rem;border-radius:999px;}
.how-list{display:flex;flex-direction:column;gap:.85rem;position:relative;}
.how-row{display:grid;grid-template-columns:52px 1fr auto;gap:1rem;align-items:center;background:rgba(255,255,255,.88);border:1px solid rgba(148,163,184,.65);border-radius:16px;padding:1rem 1.25rem;box-shadow:0 6px 16px rgba(15,23,42,.05);transition:transform .25s cubic-bezier(.22,1,.36,1),box-shadow .25s ease,background .25s ease,border-color .25s ease;}
.how-row:hover{transform:translateX(6px);background:#FFFFFF;border-color:var(--accent);box-shadow:0 12px 24px rgba(15,23,42,.1);}
.how-num{width:46px;height:46px;border-radius:13px;background:#0F172A;color:#FFFFFF;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:1.05rem;display:flex;align-items:center;justify-content:center;transition:background .25s ease,transform .25s ease;}
.how-row:hover .how-num{background:var(--accent);transform:scale(1.05);}
.how-body h4{font-family:'Bricolage Grotesque',sans-serif;font-size:1.12rem;margin:0 0 .2rem;color:var(--ink);}
.how-body p{margin:0;color:var(--muted);font-size:.9rem;line-height:1.5;}
.how-pill{font-size:.74rem;font-weight:700;color:#0369A1;background:#E0F2FE;padding:.24rem .65rem;border-radius:999px;white-space:nowrap;}

/* Preset bar rapat */
.st-key-preset_bar [data-testid="stHorizontalBlock"]{gap:.45rem!important;flex-wrap:wrap!important;}
.st-key-preset_bar [data-testid="stColumn"]{flex:0 0 auto!important;width:auto!important;min-width:0!important;}
.st-key-preset_bar button{border-radius:999px!important;padding:.32rem .85rem!important;font-size:.86rem!important;font-weight:600!important;background:rgba(255,255,255,.84)!important;border:1px solid rgba(148,163,184,.75)!important;color:var(--ink)!important;transition:all .2s ease!important;box-shadow:0 2px 6px rgba(15,23,42,.04)!important;}
.st-key-preset_bar button:hover{background:var(--ink)!important;color:#FFFFFF!important;border-color:var(--ink)!important;transform:translateY(-2px)!important;box-shadow:0 6px 14px rgba(15,23,42,.14)!important;}

/* Form utama dibuat kontras & bersih tanpa strip warna-warni */
.st-key-form_box{background:#FFFFFF!important;border:1.5px solid #94A3B8!important;border-radius:20px!important;padding:1.35rem 1.45rem 1.4rem!important;box-shadow:0 18px 40px rgba(15,23,42,.12)!important;}
.form-banner{display:flex;align-items:center;justify-content:space-between;padding:0 0 .85rem;margin-bottom:1rem;border-bottom:1px solid #E2E8F0;}
.form-banner b{font-family:'Bricolage Grotesque',sans-serif;font-size:1.15rem;color:var(--ink);letter-spacing:-.01em;}
.form-banner span{font-size:.76rem;background:#E2E8F0;color:#334155;padding:.2rem .6rem;border-radius:999px;font-weight:600;}
.st-key-form_box [data-baseweb="select"]>div{background:#F8FAFC!important;border:1.5px solid #94A3B8!important;border-radius:10px!important;}
.st-key-form_box [data-baseweb="select"]>div:focus-within{border-color:#0284C7!important;background:#FFFFFF!important;}

.band{background:linear-gradient(135deg,#0F172A 0%,#1E293B 100%);color:#fff;border-radius:22px;padding:2rem 2.2rem;margin-top:1rem;box-shadow:0 14px 34px rgba(15,23,42,.14);}
.band h2,.band h3{color:#fff!important;margin-top:0;}
.band .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:1rem;}
.band .num{font-family:'Bricolage Grotesque',sans-serif;font-size:2.8rem;font-weight:800;color:#38BDF8;line-height:1;}
.band p{color:#CBD5E1;line-height:1.5;margin:.4rem 0 0;}
.band>p{margin-top:1.6rem;}

.photo-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.4rem;margin-top:1rem;}
.photo-card{background:var(--paper);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:0 6px 20px rgba(15,23,42,.06);transition:transform .28s ease,box-shadow .28s ease;}
.photo-card:hover{transform:translateY(-5px);box-shadow:0 14px 30px rgba(15,23,42,.12);}
.photo-card img{width:100%;height:190px;object-fit:cover;display:block;transition:transform .45s ease;}
.photo-card:hover img{transform:scale(1.04);}
.photo-card .pc-body{padding:1.1rem 1.3rem;}
.photo-card .pc-tag{display:inline-block;font-size:.76rem;font-weight:600;padding:.2rem .65rem;border-radius:999px;background:#E0F2FE;color:#0369A1;margin-bottom:.45rem;}
.photo-card h4{font-family:'Bricolage Grotesque',sans-serif;font-size:1.22rem;margin:0 0 .35rem;color:var(--ink);}
.photo-card p{margin:0;color:var(--muted);font-size:.92rem;line-height:1.55;}

.team{display:grid;grid-template-columns:repeat(3,1fr);gap:1.3rem;margin-top:1rem;}
.member{display:flex;align-items:center;gap:1rem;background:#FFFFFF;border:1.5px solid var(--line);border-radius:18px;padding:1.15rem 1.25rem;box-shadow:0 8px 20px rgba(15,23,42,.06);transition:transform .25s cubic-bezier(.22,1,.36,1),box-shadow .25s ease,border-color .25s ease;}
.member:hover{transform:translateY(-5px);border-color:var(--accent);box-shadow:0 14px 28px rgba(2,132,199,.16);}
.member img.m-avatar{width:72px;height:72px;border-radius:16px;object-fit:cover;flex-shrink:0;border:1.5px solid #CBD5E1;background:#E0F2FE;transition:transform .25s ease;}
.member:hover img.m-avatar{transform:scale(1.06) rotate(-2deg);}
.member .m-info{min-width:0;}
.member b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:1.12rem;color:var(--ink);line-height:1.25;}
.member .m-nim{display:inline-block;font-size:.78rem;font-weight:600;color:#0369A1;background:#E0F2FE;padding:.12rem .55rem;border-radius:999px;margin-top:.28rem;}
.member .m-role{display:block;color:var(--muted);font-size:.88rem;margin-top:.32rem;line-height:1.4;}

.panel-empty{background:rgba(255,255,255,.78);border:2px dashed #64748B;border-radius:20px;padding:2.2rem 1.6rem;color:var(--muted);line-height:1.6;backdrop-filter:blur(6px);}
.panel-empty b{color:var(--ink);font-family:'Bricolage Grotesque',sans-serif;font-size:1.3rem;display:block;margin-bottom:.4rem;}
.result{background:#FFFFFF;border:1.5px solid var(--line);border-radius:18px;padding:1.15rem 1.3rem;margin-bottom:.85rem;box-shadow:0 12px 28px rgba(15,23,42,.08);animation:fadeUp .35s ease-out both;}
.result.warn{border-color:#FCA5A5;}
.result.ok{border-color:#6EE7B7;}
.r-head{display:flex;align-items:center;justify-content:space-between;gap:.6rem;flex-wrap:wrap;}
.r-tag{font-family:'Bricolage Grotesque',sans-serif;font-size:1.3rem;font-weight:700;}
.result.warn .r-tag{color:var(--risk);}
.result.ok .r-tag{color:var(--lagoon);}
.r-stamp{font-family:'Bricolage Grotesque',sans-serif;font-size:.68rem;font-weight:800;letter-spacing:.06em;padding:.2rem .55rem;border-radius:6px;border:1.5px solid currentColor;text-transform:uppercase;}
.r-stamp.stamp-risk{color:#DC2626;background:#FEF2F2;}
.r-stamp.stamp-watch{color:#B45309;background:#FFFBEB;}
.r-stamp.stamp-safe{color:#059669;background:#ECFDF5;}
.r-score-row{display:flex;align-items:baseline;justify-content:space-between;gap:.75rem;flex-wrap:wrap;margin-top:.35rem;}
.r-num{font-family:'Bricolage Grotesque',sans-serif;font-size:3.1rem;font-weight:800;line-height:1;margin:0;}
.r-num span{font-size:1.6rem;}
.r-sub{color:var(--muted);font-size:.84rem;margin-top:.1rem;}
.gauge{position:relative;height:11px;border-radius:6px;background:var(--mist);margin:.75rem 0 .35rem;}
.gauge .fill{height:100%;border-radius:6px;background:var(--lagoon);transition:width .6s ease;}
.result.warn .gauge .fill{background:var(--risk);}
.gauge .tick{position:absolute;top:-5px;bottom:-5px;width:3.5px;border-radius:2px;background:#F59E0B;}
.g-note{color:var(--muted);font-size:.8rem;line-height:1.4;}
.r-text{margin:.65rem 0 0;font-size:.9rem;line-height:1.48;}
.r-zone{display:inline-block;padding:.18rem .6rem;border-radius:999px;font-size:.78rem;font-weight:600;background:var(--mist);color:var(--ink);}
.result.warn .r-zone{background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;}
.result.ok .r-zone{background:#ECFDF5;color:#059669;border:1px solid #A7F3D0;}
.r-zone.near{background:#FFFBEB;color:#B45309;border:1px solid #FDE68A;}
.r-drivers{margin-top:.8rem;padding-top:.7rem;border-top:1px solid #E2E8F0;}
.r-drivers h4{font-family:'Bricolage Grotesque',sans-serif;font-size:.95rem;margin:0 0 .35rem;}
.r-drivers ul{list-style:none;padding:0;margin:0;display:grid;gap:.28rem;}
.r-drivers li{display:flex;justify-content:space-between;align-items:baseline;gap:.6rem;font-size:.83rem;padding:.28rem .55rem;border-radius:8px;background:#F8FAFC;border:1px solid #E2E8F0;}
.r-drivers li b{font-weight:600;color:var(--ink);}
.r-drivers .d-up{color:#DC2626;font-weight:600;white-space:nowrap;}
.r-drivers .d-down{color:#059669;font-weight:600;white-space:nowrap;}
.r-drivers .d-flat{color:var(--muted);white-space:nowrap;}
.r-actions{margin-top:.75rem;padding-top:.65rem;border-top:1px solid #E2E8F0;}
.r-actions h4{font-family:'Bricolage Grotesque',sans-serif;font-size:.95rem;margin:0 0 .3rem;}
.r-actions ol{margin:0;padding-left:1.1rem;display:grid;gap:.22rem;font-size:.83rem;color:var(--ink);line-height:1.38;}
.fin-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin:.2rem 0 .85rem;}
.fin-card{background:#FFFFFF;border:1px solid #CBD5E1;border-radius:13px;padding:.7rem .9rem;box-shadow:0 4px 12px rgba(15,23,42,.04);}
.fin-card small{display:block;font-size:.72rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.03em;}
.fin-card b{display:block;font-family:'Bricolage Grotesque',sans-serif;font-size:1.22rem;color:var(--ink);margin-top:.12rem;line-height:1.2;}
.fin-card span{display:block;font-size:.76rem;color:var(--muted);margin-top:.1rem;}
.whatif-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.65rem;margin:.2rem 0 .85rem;}
.whatif-item{background:#FFFFFF;border:1px solid #CBD5E1;border-radius:12px;padding:.65rem .85rem;display:flex;justify-content:space-between;align-items:center;gap:.65rem;box-shadow:0 4px 12px rgba(15,23,42,.04);}
.whatif-item b{display:block;font-size:.84rem;color:var(--ink);line-height:1.3;}
.whatif-item small{color:var(--muted);font-size:.75rem;}
.wi-badge{font-family:'Bricolage Grotesque',sans-serif;font-size:.82rem;font-weight:700;padding:.2rem .55rem;border-radius:999px;white-space:nowrap;}
.wi-down{background:#ECFDF5;color:#059669;border:1px solid #A7F3D0;}
.wi-up{background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;}
.wi-flat{background:#F1F5F9;color:#475569;border:1px solid #CBD5E1;}
[data-testid="stExpander"]{margin-top:.75rem!important;border-radius:14px!important;background:rgba(255,255,255,.78)!important;border:1px solid rgba(148,163,184,.6)!important;}
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
 .block-container{padding-left:1.1rem;padding-right:1.1rem;padding-top:1.2rem;}
 .brand{font-size:1.3rem;}
 .brand small{font-size:.75rem;}
 .hero{grid-template-columns:1fr;gap:1.4rem;padding:.8rem 0 .6rem;}
 .hero h1{font-size:2.15rem;line-height:1.08;margin-bottom:.7rem;}
 .hero p.lead{font-size:1rem;line-height:1.55;margin-bottom:1.1rem;}
 .hero-cta{display:flex;flex-direction:column;gap:.6rem;}
 .hero-cta .cta,.hero-cta .ghost{display:block;text-align:center;margin:0;padding:.8rem 1rem;}
 .hero-stats{grid-template-columns:1fr;}
 .dots{width:min(100%,280px);gap:5px;}
 .viz-cap{font-size:.98rem;}
 .stApp h2{font-size:1.5rem;margin-top:1.8rem;}
 .how-wrap,.band .grid,.team,.photo-grid,.fin-grid,.whatif-grid{grid-template-columns:1fr;}
 .how-row{grid-template-columns:44px 1fr;}
 .how-pill{grid-column:2;width:fit-content;}
 .band{padding:1.4rem 1.3rem;}
 .band .num{font-size:2.2rem;}
 .r-num{font-size:3.2rem;}
}
@media (prefers-reduced-motion:reduce){.gauge .fill,.stApp,.hero,.how-row,.result,.dots i.on,.hero-carousel .c-slide,.hero-carousel .c-dots i{transition:none;animation:none;}}
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
    cards = "".join(
        f'<div class="member">'
        f'<img class="m-avatar" src="{resolve_photo(m["foto"])}" alt="Foto {m["nama"]}" loading="lazy"/>'
        f'<div class="m-info"><b>{m["nama"]}</b><span class="m-nim">{m["nim"]}</span><span class="m-role">{m["peran"]}</span></div>'
        f'</div>'
        for m in TEAM
    )
    return f'<div class="team">{cards}</div>'
