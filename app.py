import streamlit as st
import base64
import os
import materi       # Mengimpor modul halaman materi
import klasifikasi # Mengimpor modul halaman klasifikasi yang baru dibuat

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Sampedia - Belajar, Pilah, Selamatkan Bumi",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inisialisasi State Navigasi Halaman
if "page" not in st.session_state:
    st.session_state.page = "beranda"

# Tangkap parameter navigasi URL
url_params = st.query_params
if "page" in url_params:
    st.session_state.page = url_params["page"]

# Fungsi untuk mengubah gambar lokal menjadi Base64 agar bisa dibaca CSS
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

img_base64 = get_base64_image("assets/images/hero_sampah.png")

# 2. INJEKSI CSS GLOBAL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f4f9f4 !important;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 0rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
    }
    
    [data-testid="stHeader"] {
        display: none;
    }

    /* NAVBAR CUSTOM */
    .custom-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #ffffff;
        padding: 12px 40px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
        margin-bottom: 16px;
    }
    .nav-logo-box {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-logo-text {
        font-weight: 800;
        font-size: 1.4rem;
        color: #1b4d3e;
    }
    .nav-logo-sub {
        font-size: 0.65rem;
        color: #6b7280;
        font-weight: 500;
        margin-top: -2px;
    }
    .nav-links {
        display: flex;
        gap: 30px;
    }
    .nav-item {
        text-decoration: none;
        color: #1f2937;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .nav-item.active {
        color: #2e7d32;
        position: relative;
    }
    .nav-item.active::after {
        content: '';
        position: absolute;
        bottom: -6px;
        left: 0;
        width: 100%;
        height: 3px;
        background: #2e7d32;
        border-radius: 2px;
    }
    .nav-btn-right {
        background: #1b4d3e; 
        color: white !important; 
        padding: 10px 22px; 
        border-radius: 12px; 
        font-weight: 700; 
        font-size: 0.9rem;
        text-decoration: none;
        display: inline-block;
    }
    
    /* HERO ELEMENTS */
    .badge-ai {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 800;
        margin-bottom: 12px;
        display: inline-block;
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.15;
        color: #0f2e25;
        margin-bottom: 12px;
        max-width: 55%;
    }
    .hero-title span {
        color: #2e7d32;
    }
    .hero-desc {
        font-size: 0.95rem;
        color: #4b5563;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 24px;
        max-width: 50%;
    }
    .hero-buttons {
        display: flex;
        gap: 15px;
        margin-bottom: 24px;
    }
    .btn-hero-primary {
        background: #1b4d3e;
        color: white !important;
        padding: 11px 24px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(27,77,62,0.15);
        text-decoration: none;
    }
    .btn-hero-secondary {
        background: #ffffff;
        color: #1b4d3e;
        border: 1px solid #d1d5db;
        padding: 11px 24px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.9rem;
        text-decoration: none;
        display: inline-block;
    }
    .chips-container {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .chip-item {
        background: #fffbdf;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #1b4d3e;
    }
    .chip-item:nth-child(even) {
        background: #eefcf2;
    }

    /* CARDS & LAYOUT */
    .feature-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.01);
        display: flex;
        align-items: center;
        gap: 12px;
        height: 82px;
        border: 1px solid #eef4ee;
    }
    .card-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        flex-shrink: 0;
    }
    .card-h4 {
        font-size: 0.88rem;
        font-weight: 800;
        color: #0f2e25;
        margin-bottom: 2px;
    }
    .card-p {
        font-size: 0.78rem;
        color: #6b7280;
        line-height: 1.3;
        margin: 0;
    }
    
    /* STATS BAR */
    .counter-bar-wrapper {
        margin: 20px 0;
        padding: 4px;
        background: linear-gradient(135deg, #2e7d32 0%, #a7f3d0 100%);
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(46, 125, 50, 0.08);
    }
    .counter-bar-inner {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px 30px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
    }
    .counter-item-box {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 10px 20px;
        background: #ffffff;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
        border: 1px solid rgba(46, 125, 50, 0.08);
        flex: 1;
        min-width: 220px;
        transition: transform 0.2s ease;
    }
    .counter-item-box:hover {
        transform: translateY(-2px);
    }
    .counter-icon-sphere {
        width: 46px;
        height: 46px;
        border-radius: 12px;
        background: #e8f5e9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        flex-shrink: 0;
    }
    .counter-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #1b4d3e;
        line-height: 1.2;
    }
    .counter-label {
        font-size: 0.78rem;
        color: #6b7280;
        font-weight: 600;
        margin-top: 1px;
    }

    /* CARA MENGGUNAKAN */
    .section-title-center {
        text-align: center;
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f2e25;
        margin: 16px 0 14px 0;
    }
    .flow-card-row {
        background: #fafdfa;
        border-radius: 14px;
        padding: 12px 16px;
        border: 1px solid #eef2ee;
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
    }
    .flow-number {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #2e7d32;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    .flow-arrow {
        font-size: 1.1rem;
        color: #9ca3af;
    }

    /* STYLE SUB-HALAMAN MATERI */
    .materi-hero {
        background: linear-gradient(135deg, #1b4d3e 0%, #113629 100%);
        color: white;
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 24px;
        text-align: center;
    }
    .materi-box-organik {
        background: #ffffff;
        border-top: 5px solid #2e7d32;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .materi-box-anorganik {
        background: #ffffff;
        border-top: 5px solid #ca8a04;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .item-list-materi {
        background: #f8fafc;
        padding: 10px 14px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #334155;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* FOOTER */
    .footer-wave-container {
        margin-top: 20px;
        margin-bottom: -1px;
        width: 100%;
        display: block;
        line-height: 0;
    }
    .custom-footer {
        background-color: #113629;
        color: #ffffff;
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;
        padding: 15px 40px 30px 40px;
    }
    .footer-quote {
        font-size: 1.25rem;
        font-weight: 700;
    }
    .footer-heading {
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .footer-link {
        color: #d1d5db;
        text-decoration: none;
        margin-bottom: 6px;
        font-size: 0.82rem;
        display: block;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        padding: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. BACKGROUND HERO BANNER
st.markdown(f"""
<style>
    .hero-section {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center right;
        background-repeat: no-repeat;
        padding: 50px 45px;
        border-radius: 24px;
        margin-bottom: 14px;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.01);
    }}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. NAVBAR GLOBAL (DIPERBAIKI)
# ==========================================
is_beranda_active = "active" if st.session_state.page == "beranda" else ""
is_materi_active = "active" if st.session_state.page == "materi" else ""
is_klasifikasi_active = "active" if st.session_state.page == "klasifikasi" else ""

st.markdown(f"""
<div class="custom-navbar">
    <div class="nav-logo-box">
        <span style="font-size: 2rem;">♻️</span>
        <div>
            <div class="nav-logo-text">Sampedia</div>
            <div class="nav-logo-sub">Belajar, Pilah, Selamatkan Bumi</div>
        </div>
    </div>
    <div class="nav-links">
        <a class="nav-item {is_beranda_active}" href="/?page=beranda" target="_self">Beranda</a>
        <a class="nav-item {is_materi_active}" href="/?page=materi" target="_self">Materi</a>
        <a class="nav-item {is_klasifikasi_active}" href="/?page=klasifikasi" target="_self">Klasifikasi</a>
        <a class="nav-item" href="#">Tentang</a>
    </div>
    <a class="nav-btn-right" href="/?page=klasifikasi" target="_self">📸 Mulai Klasifikasi</a>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 5. INTEGRASI ROUTING HALAMAN MODULAR
# ==========================================

if st.session_state.page == "beranda":
    # --- KONTEN BERANDA ---
    st.markdown("""
    <div class="hero-section">
        <div>
            <div class="badge-ai">🌱 EDUKASI SAMPAH BERBASIS AI</div>
            <h1 class="hero-title">Mulai Dari Sampah, Mulai Dari Kita <span>untuk Bumi yang Lebih Baik</span></h1>
            <p class="hero-desc">Belajar memilah sampah dengan AI dan game edukatif yang interaktif, menyenangkan, dan mudah dipahami untuk semua usia.</p>
            <div class="hero-buttons">
                <a href="/?page=klasifikasi" target="_self" class="btn-hero-primary">📸 Mulai Klasifikasi</a>
                <a href="/?page=materi" target="_self" class="btn-hero-secondary">📖 Lihat Materi</a>
            </div>
            <div class="chips-container">
                <div class="chip-item">✨ AI Cerdas</div>
                <div class="chip-item">😊 Mudah Digunakan</div>
                <div class="chip-item">👨‍👩‍👧‍👦 Untuk Semua Usia</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Kartu Manfaat
    card_col1, card_col2, card_col3, card_col4 = st.columns(4)
    with card_col1:
        st.markdown("""<div class="feature-card"><div class="card-icon-box" style="color: #2563eb; background: #eff6ff;">🌍</div><div><div class="card-h4">Bumi Lebih Bersih</div><div class="card-p">Mengurangi pencemaran lingkungan.</div></div></div>""", unsafe_allow_html=True)
    with card_col2:
        st.markdown("""<div class="feature-card"><div class="card-icon-box" style="color: #16a34a; background: #f0fdf4;">🌱</div><div><div class="card-h4">Sumber Daya Terjaga</div><div class="card-p">Daur ulang sampah jadi fungsional.</div></div></div>""", unsafe_allow_html=True)
    with card_col3:
        st.markdown("""<div class="feature-card"><div class="card-icon-box" style="color: #dc2626; background: #fef2f2;">❤️</div><div><div class="card-h4">Hidup Lebih Sehat</div><div class="card-p">Mencegah sarang penyakit.</div></div></div>""", unsafe_allow_html=True)
    with card_col4:
        st.markdown("""<div class="feature-card"><div class="card-icon-box" style="color: #ca8a04; background: #fefce8;">♻️</div><div><div class="card-h4">Masa Depan Baik</div><div class="card-p">Investasi keasrian generasi esok.</div></div></div>""", unsafe_allow_html=True)

    # Stats Bar
    st.markdown("""
    <div class="counter-bar-wrapper">
        <div class="counter-bar-inner">
            <div class="counter-item-box"><div class="counter-icon-sphere">🖼️</div><div><span class="counter-value">3.500+</span><br><span class="counter-label">Dataset Citra</span></div></div>
            <div class="counter-item-box"><div class="counter-icon-sphere">♻️</div><div><span class="counter-value">2 Kategori</span><br><span class="counter-label">Organik & Anorganik</span></div></div>
            <div class="counter-item-box"><div class="counter-icon-sphere">🧠</div><div><span class="counter-value">ResNet50</span><br><span class="counter-label">Arsitektur Model AI</span></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cara Menggunakan
    st.markdown('<div class="section-title-center"> Cara Menggunakan Sampedia</div>', unsafe_allow_html=True)
    flow_col1, flow_col2, flow_col3 = st.columns([4, 1, 4])
    with flow_col1:
        st.markdown("""<div class="flow-card-row"><div class="flow-number">1</div><div style="font-size:1.5rem;">📖</div><div><h6 style="margin:0; font-weight:800; font-size:0.88rem; color:#0f2e25;">Pelajari Materi</h6><p style="margin:2px 0 0 0; font-size:0.78rem; color:#6b7280; line-height:1.3;">Baca materi jenis sampah organik dan anorganik dengan mudah.</p></div></div>""", unsafe_allow_html=True)
    with flow_col2:
        st.markdown('<div style="text-align:center; padding-top:10px;" class="flow-arrow">➔</div>', unsafe_allow_html=True)
    with flow_col3:
        st.markdown("""<div class="flow-card-row"><div class="flow-number">2</div><div style="font-size:1.5rem;">📸</div><div><h6 style="margin:0; font-weight:800; font-size:0.88rem; color:#0f2e25;">Klasifikasi Sampah</h6><p style="margin:2px 0 0 0; font-size:0.78rem; color:#6b7280; line-height:1.3;">Upload gambar sampah dan dapatkan hasil klasifikasi otomatis.</p></div></div>""", unsafe_allow_html=True)

elif st.session_state.page == "materi":
    # --- MEMANGGIL KONTEN DARI FILE MATERI.PY ---
    materi.render_page()

elif st.session_state.page == "klasifikasi":
    # --- MEMANGGIL KONTEN DARI FILE KLASIFIKASI.PY (BARU) ---
    klasifikasi.render_page()


# ==========================================
# 6. FOOTER GLOBAL
# ==========================================
st.markdown("""
<div class="footer-wave-container">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 60" style="display:block; width:100%; height:auto;">
        <path fill="#113629" fill-opacity="1" d="M0,45 C240,15 480,15 720,45 C960,75 1200,45 1440,30 L1440,60 L0,60 Z"></path>
    </svg>
</div>
<div class="custom-footer">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">
        <div style="flex: 1.5; min-width: 250px;">
            <div class="footer-quote">"Jangan tunggu bumi berubah, mulailah dari dirimu."</div>
            <p style="font-size: 0.88rem; color: #a7f3d0; margin-top: 2px;">— Sampedia</p>
        </div>
        <div style="flex: 1; min-width: 180px;">
            <div class="footer-heading">Sampedia</div>
            <p style="font-size: 0.8rem; color: #d1d5db; line-height: 1.4; margin:0;">Platform edukasi pemilahan sampah berbasis AI untuk masa depan yang lebih bersih.</p>
        </div>
        <div style="flex: 0.8; min-width: 120px;">
            <div class="footer-heading">Menu</div>
            <a class="footer-link" href="/?page=beranda" target="_self">Beranda</a>
            <a class="footer-link" href="/?page=materi" target="_self">Materi</a>
            <a class="footer-link" href="/?page=klasifikasi" target="_self">Klasifikasi</a>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <div class="footer-heading">Kontak</div>
            <div class="footer-link">📩 sampedia@gmail.com</div>
            <div class="footer-link">📸 @sampedia.id</div>
        </div>
    </div>
    <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 20px 0 10px 0;">
    <p style="text-align: center; font-size: 0.78rem; color: #a7f3d0; margin: 0;">© 2026 Sampedia AI Project.</p>
</div>
""", unsafe_allow_html=True)