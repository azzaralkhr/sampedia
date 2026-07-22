import streamlit as st
import base64
import os

def get_base64_image(image_path):
    """Fungsi untuk mengubah gambar lokal menjadi Base64 agar bisa dibaca tag HTML <img>"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""

def render_page():
    # --- CSS CUSTOM UNTUK MENIRU DESAIN MOCKUP 2 (LEBIH HIDUP, PREMIUM & TERCERNA) ---
    st.markdown("""
    <style>
        /* Mengatur font global agar bersih */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        
        /* Mengurangi padding default Streamlit block container */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
        }
        
        /* --- SIDEBAR STYLE RE-DESIGN --- */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        
        .sidebar-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1b4d3e;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tahu-box {
            background-color: #f1f5f9;
            border-radius: 14px;
            padding: 16px;
            margin-top: 20px;
            border: 1px solid #cbd5e1;
            text-align: left;
        }
        
        .tahu-title {
            color: #0f172a;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* --- MAIN CONTENT STYLE --- */
        /* Hero Banner Premium disesuaikan dengan gambar ke-2 */
        .hero-banner {
            background: linear-gradient(135deg, #0b4632 0%, #156347 100%);
            border-radius: 20px;
            padding: 40px 50px;
            color: white;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 25px rgba(11, 70, 50, 0.25);
        }
        
        .hero-text {
            max-width: 60%;
        }
        
        .hero-title {
            font-size: 2.5rem;
            font-weight: 800;
            color: #ffffff !important;
            margin: 0 0 15px 0 !important;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }
        
        /* Deskripsi dibuat lebih besar, tebal, dan warna mencolok putih bersih */
        .hero-desc {
            font-size: 1.15rem;
            font-weight: 500;
            color: #ffffff !important;
            line-height: 1.7;
            margin: 0 !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .hero-image-container {
            max-width: 35%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .hero-image-container img {
            max-height: 180px;
            width: auto;
            object-fit: contain;
            filter: drop-shadow(0px 8px 16px rgba(0, 0, 0, 0.2));
        }

        /* Subheadings diperjelas */
        .section-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #0f172a;
            margin: 24px 0 14px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            border-left: 4px solid #156347;
            padding-left: 10px;
        }
        
        .section-title.anorganik {
            border-left: 4px solid #d97706;
        }

        /* Karakteristik Cards dibuat lebih hidup & readable */
        .karakter-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            height: 100%;
            display: flex;
            gap: 14px;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .karakter-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        .karakter-icon {
            font-size: 1.6rem;
            background: #e8f5e9;
            width: 48px;
            height: 48px;
            border-radius: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .karakter-icon.anorganik {
            background: #fef9c3;
        }
        
        .karakter-info-box {
            display: flex;
            flex-direction: column;
        }
        
        .karakter-header {
            font-weight: 700;
            font-size: 0.95rem;
            color: #0f172a;
            margin-bottom: 4px;
        }
        
        .karakter-body {
            font-size: 0.82rem;
            color: #475569;
            line-height: 1.4;
        }

        /* Contoh Cards Premium sesuai mockup */
        .contoh-card-container {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .contoh-card-container:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        }
        
        .contoh-content {
            padding: 12px;
            flex-grow: 1;
            border-top: 1px solid #f1f5f9;
        }
        
        .contoh-title {
            font-weight: 700;
            font-size: 0.9rem;
            color: #0f172a;
            margin-bottom: 6px;
        }
        
        .contoh-desc {
            font-size: 0.78rem;
            color: #64748b;
            line-height: 1.4;
        }

        /* Tips & Ringkasan Box */
        .tips-container {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .tips-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.88rem;
            color: #1e293b;
            font-weight: 500;
        }
        
        .tips-badge {
            width: 32px;
            height: 32px;
            border-radius: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }

        .ringkasan-box {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .ringkasan-list {
            margin: 0;
            padding-left: 20px;
            font-size: 0.88rem;
            color: #334155;
            line-height: 1.6;
        }
        
        .ringkasan-list li {
            margin-bottom: 6px;
        }
        
        /* Bottom Banner Info */
        .bottom-nav-box {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 12px;
            padding: 14px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 24px;
            margin-bottom: 12px;
        }
        
        .bottom-nav-text {
            font-size: 0.9rem;
            color: #065f46;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Tombol Streamlit Style Override */
        .stButton button {
            font-weight: 600 !important;
            border-radius: 10px !important;
            transition: all 0.2s !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR NAVIGASI ---
    if 'materi_aktif' not in st.session_state:
        st.session_state.materi_aktif = "Sampah Organik"

    with st.sidebar:
        st.markdown('<div class="sidebar-title">📁 Menu Materi</div>', unsafe_allow_html=True)
        
        if st.button("🍃 1. Sampah Organik", use_container_width=True, key="side_org"):
            st.session_state.materi_aktif = "Sampah Organik"
            st.rerun()
            
        if st.button("⚡ 2. Sampah Anorganik", use_container_width=True, key="side_anorg"):
            st.session_state.materi_aktif = "Sampah Anorganik"
            st.rerun()

        # Section "Tahukah Kamu?"
        st.markdown('<div class="tahu-box">', unsafe_allow_html=True)
        if st.session_state.materi_aktif == "Sampah Organik":
            st.markdown('<div class="tahu-title">🟢 Tahukah Kamu?</div>', unsafe_allow_html=True)
            if os.path.exists("assets/images/tong_organik.png"):
                st.image("assets/images/tong_organik.png", use_container_width=True, output_format="PNG")
            st.markdown('<p style="font-size:0.83rem; color:#475569; line-height:1.5; margin-top:8px; margin-bottom:0;">Sampah organik jika dikelola dengan baik dapat menjadi kompos yang bermanfaat untuk menyuburkan tanaman dan mengurangi volume sampah di lingkungan kita.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="tahu-title" style="color: #ca8a04;">🟡 Tahukah Kamu?</div>', unsafe_allow_html=True)
            if os.path.exists("assets/images/tong_anorganik.png"):
                st.image("assets/images/tong_anorganik.png", use_container_width=True, output_format="PNG")
            st.markdown('<p style="font-size:0.83rem; color:#475569; line-height:1.5; margin-top:8px; margin-bottom:0;">Sampah anorganik membutuhkan waktu sangat lama untuk terurai secara alami. Namun, sampah ini dapat didaur ulang menjadi produk baru yang bermanfaat.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # --- HALAMAN 1: SAMPAH ORGANIK ---
    if st.session_state.materi_aktif == "Sampah Organik":
        # Mengonversi gambar Organik lokal ke Base64 agar tampil lancar di HTML
        img_base64_org = get_base64_image("assets/images/Organik.png")
        
        # 1. Hero Banner Utama dengan Gambar Ilustrasi Wadah Sampah Organik Melimpah
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-text">
                <h2 class="hero-title">1. Sampah Organik</h2>
                <p class="hero-desc">Sampah organik adalah sampah yang berasal dari makhluk hidup dan dapat terurai secara alami oleh mikroorganisme. Sampah ini ramah lingkungan dan dapat diolah menjadi kompos atau pupuk alami.</p>
            </div>
            <div class="hero-image-container">
                <img src="{img_base64_org}" alt="Sampah Organik">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Karakteristik Sampah Organik
        st.markdown('<div class="section-title">Characteristics / Karakteristik Sampah Organik</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🌱</div><div class="karakter-info-box"><div class="karakter-header">Mudah Terurai</div><div class="karakter-body">Dapat terurai secara alami dalam hitungan hari hingga minggu.</div></div></div>""", unsafe_allow_html=True)
        with k_col2:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">♻️</div><div class="karakter-info-box"><div class="karakter-header">Ramah Lingkungan</div><div class="karakter-body">Tidak mencemari tanah, air, and udara serta aman bagi makhluk hidup.</div></div></div>""", unsafe_allow_html=True)
        with k_col3:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🪴</div><div class="karakter-info-box"><div class="karakter-header">Bermanfaat</div><div class="karakter-body">Dapat diolah menjadi kompos atau pupuk untuk tanaman.</div></div></div>""", unsafe_allow_html=True)
        with k_col4:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🕒</div><div class="karakter-info-box"><div class="karakter-header">Waktu Terurai</div><div class="karakter-body">Beberapa hari hingga beberapa minggu tergantung jenisnya.</div></div></div>""", unsafe_allow_html=True)
            
        # 3. Contoh Sampah Organik Grid (5 Kolom)
        st.markdown('<div class="section-title">Contoh Sampah Organik</div>', unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
        
        with c_col1:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/sisa_sayur.webp", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Sisa Sayuran & Buah</div><div class="contoh-desc">Sisa potongan sayur, kulit buah, and buah busuk termasuk sampah organik.</div></div></div>', unsafe_allow_html=True)
            
        with c_col2:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/daun_kering.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Daun Kering & Ranting</div><div class="contoh-desc">Daun kering dan ranting dapat terurai alami dan menyuburkan tanah.</div></div></div>', unsafe_allow_html=True)
            
        with c_col3:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/sisa_makanan.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Sisa Tulang & Nasi</div><div class="contoh-desc">Sisa makanan seperti nasi dan tulang hewan bisa menjadi pakan ternak.</div></div></div>', unsafe_allow_html=True)
            
        with c_col4:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/ampas_kopi.webp", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Ampas Kopi / Teh</div><div class="contoh-desc">Ampas kopi dan teh dapat digunakan sebagai pupuk alami penyubur.</div></div></div>', unsafe_allow_html=True)
            
        with c_col5:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/kulit_telur.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Kulit Telur</div><div class="contoh-desc">Kulit telur dapat diolah menjadi pupuk organik kaya kalsium untuk tanaman.</div></div></div>', unsafe_allow_html=True)

        # 4. Tips Pengelolaan & Ringkasan Materi (Baris Kompak)
        b_col1, b_col2 = st.columns([1, 1])
        
        with b_col1:
            st.markdown('<div class="section-title">🧺 Tips Pengelolaan</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="tips-container">
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">🗑️</div><span>Pisahkan sampah organik dari sampah anorganik.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">📦</div><span>Kumpulkan sampah organik di wadah tertutup.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">🍃</div><span>Olah menjadi kompos secara rutin.</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with b_col2:
            st.markdown('<div class="section-title">📋 Ringkasan Materi</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="ringkasan-box">
                <ul class="ringkasan-list">
                    <li>Sampah organik berasal dari makhluk hidup.</li>
                    <li>Mudah terurai dan ramah lingkungan.</li>
                    <li>Dapat diolah menjadi kompos atau pupuk alami.</li>
                    <li>Manfaatnya besar untuk lingkungan dan tanaman.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 5. Bottom Navigation Bar
        st.markdown("""
        <div class="bottom-nav-box">
            <div class="bottom-nav-text">
                <span>📖</span>
                <span>Pahami jenis sampah lainnya dan cara pengelolaannya dengan benar untuk lingkungan yang lebih bersih!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns([4, 1])
        with col_b2:
            if st.button("Lanjut ke Materi Anorganik ➡️", key="btn_next_anorg", use_container_width=True):
                st.session_state.materi_aktif = "Sampah Anorganik"
                st.rerun()


    # --- HALAMAN 2: SAMPAH ANORGANIK ---
    elif st.session_state.materi_aktif == "Sampah Anorganik":
        # PERBAIKAN UTAMA: Mengonversi gambar Anorganik lokal ke Base64 dengan path yang benar
        img_base64_anorg = get_base64_image("assets/images/Anorganik.png")

        # 1. Hero Banner Anorganik Utama dengan Gambar Ilustrasi Wadah Sampah Anorganik
        st.markdown(f"""
        <div class="hero-banner" style="background: linear-gradient(135deg, #7c2d12 0%, #b45309 100%); box-shadow: 0 4px 15px rgba(124, 45, 18, 0.15);">
            <div class="hero-text">
                <h2 class="hero-title">2. Sampah Anorganik</h2>
                <p class="hero-desc">Sampah anorganik adalah sampah yang berasal dari bahan-bahan sintetis atau non-hayati yang sulit atau tidak dapat terurai secara alami. Sampah ini membutuhkan waktu ratusan tahun untuk terurai.</p>
            </div>
            <div class="hero-image-container">
                <img src="{img_base64_anorg}" alt="Sampah Anorganik">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Karakteristik Sampah Anorganik
        st.markdown('<div class="section-title anorganik">Karakteristik Sampah Anorganik</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">⏳</div><div class="karakter-info-box"><div class="karakter-header">Sulit Terurai</div><div class="karakter-body">Membutuhkan waktu ratusan tahun untuk terurai secara alami.</div></div></div>""", unsafe_allow_html=True)
        with k_col2:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">♻️</div><div class="karakter-info-box"><div class="karakter-header">Dapat Didaur Ulang</div><div class="karakter-body">Dapat diolah kembali menjadi produk baru yang bernilai ekonomi.</div></div></div>""", unsafe_allow_html=True)
        with k_col3:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">🧪</div><div class="karakter-info-box"><div class="karakter-header">Berasal dari Bahan Sintetis</div><div class="karakter-body">Dibuat dari bahan kimia atau proses industri pabrik.</div></div></div>""", unsafe_allow_html=True)
        with k_col4:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">🌏</div><div class="karakter-info-box"><div class="karakter-header">Mencemari Lingkungan</div><div class="karakter-body">Jika tidak dikelola dengan baik dapat mencemari tanah, air, dan laut.</div></div></div>""", unsafe_allow_html=True)
            
        # 3. Contoh Sampah Anorganik Grid (5 Kolom)
        st.markdown('<div class="section-title anorganik">Contoh Sampah Anorganik</div>', unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
        
        with c_col1:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/botol_plastik.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Botol Plastik & Kantong Kresek</div><div class="contoh-desc">Terbuat dari plastik PE atau PET yang sulit terurai secara alami, tetapi dapat didaur ulang.</div></div></div>', unsafe_allow_html=True)
            
        with c_col2:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/kaleng_logam.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Kaleng Minuman & Logam</div><div class="contoh-desc">Kaleng aluminium atau besi dapat didaur ulang menjadi produk logam baru.</div></div></div>', unsafe_allow_html=True)
            
        with c_col3:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/botol_kaca.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Botol Kaca & Pecahan Beling</div><div class="contoh-desc">Kaca membutuhkan waktu sangat lama untuk terurai, namun dapat didaur ulang.</div></div></div>', unsafe_allow_html=True)
            
        with c_col4:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/styrofoam.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Styrofoam & Kardus Berlapis</div><div class="contoh-desc">Styrofoam sulit terurai dan dapat mencemari lingkungan jika dibakar.</div></div></div>', unsafe_allow_html=True)
            
        with c_col5:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/baterai_elektronik.png", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Baterai & Elektronik</div><div class="contoh-desc">Mengandung bahan kimia berbahaya, perlu penanganan khusus dan didaur ulang.</div></div></div>', unsafe_allow_html=True)

        # 4. Tips Pengelolaan & Ringkasan Materi Anorganik
        b_col1, b_col2 = st.columns([1, 1])
        
        with b_col1:
            st.markdown('<div class="section-title anorganik">🧺 Tips Pengelolaan</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="tips-container">
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">🗑️</div><span>Pisahkan sampah anorganik dari sampah organik.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">💧</div><span>Bersihkan sampah sebelum didaur ulang.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">🛍️</div><span>Gunakan kembali barang yang masih bisa dipakai.</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with b_col2:
            st.markdown('<div class="section-title anorganik">📋 Ringkasan Materi</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="ringkasan-box">
                <ul class="ringkasan-list">
                    <li>Berasal dari bahan sintetis atau non-hayati.</li>
                    <li>Sulit atau tidak dapat terurai secara alami.</li>
                    <li>Dapat didaur ulang menjadi produk baru.</li>
                    <li>Perlu pengelolaan agar tidak mencemari lingkungan.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 5. Bottom Navigation Bar Anorganik
        st.markdown("""
        <div class="bottom-nav-box" style="background: #fffbeb; border: 1px solid #fef08a;">
            <div class="bottom-nav-text" style="color: #b45309;">
                <span>📖</span>
                <span>Pelajari lebih lanjut tentang jenis sampah lainnya dan cara pengelolaan yang tepat untuk masa depan yang lebih baik!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns([4, 1])
        with col_b2:
            if st.button("↩️ Kembali ke Organik", key="btn_back_org", use_container_width=True):
                st.session_state.materi_aktif = "Sampah Organik"
                st.rerun()

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Sampedia - Ruang Edukasi")
    render_page()