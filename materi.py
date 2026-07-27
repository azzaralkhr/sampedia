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
    # --- CSS CUSTOM UNTUK MENIRU DESAIN MOCKUP & MENAMBAHKAN ELEMEN EDUKASI BARU ---
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
        
        .hero-desc {
            font-size: 1.1rem;
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

        /* Karakteristik Cards */
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

        /* Contoh Cards Premium */
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

        /* Dosis & Don'ts Box Style */
        .dos-donts-box {
            background: white;
            border-radius: 12px;
            padding: 16px;
            border: 1px solid #e2e8f0;
            height: 100%;
        }

        .dos-title {
            color: #166534;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .donts-title {
            color: #991b1b;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .dos-list, .donts-list {
            margin: 0;
            padding-left: 18px;
            font-size: 0.85rem;
            line-height: 1.6;
            color: #334155;
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
            font-size: 0.85rem;
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
            font-size: 0.85rem;
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
            st.markdown('<div class="tahu-title">🟢 Mengapa Pemilahan Penting?</div>', unsafe_allow_html=True)
            if os.path.exists("assets/images/tong_organik.png"):
                st.image("assets/images/tong_organik.png", use_container_width=True, output_format="PNG")
            st.markdown('<p style="font-size:0.83rem; color:#475569; line-height:1.5; margin-top:8px; margin-bottom:0;">Sampah organik yang tercampur dengan plastik di TPA memicu gas metana berbahaya (penyebab ledakan/kebakaran TPA) dan timbulnya air lindi berbau busuk yang mencemari air sumur warga.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="tahu-title" style="color: #ca8a04;">🟡 Mengapa Pemilahan Penting?</div>', unsafe_allow_html=True)
            if os.path.exists("assets/images/tong_anorganik.png"):
                st.image("assets/images/tong_anorganik.png", use_container_width=True, output_format="PNG")
            st.markdown('<p style="font-size:0.83rem; color:#475569; line-height:1.5; margin-top:8px; margin-bottom:0;">Plastik butuh waktu hingga 500 tahun untuk hancur. Sampah anorganik yang dibuang sembarangan pecah menjadi mikroplastik yang mencemari lautan dan dapat masuk ke dalam rantai makanan manusia.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # --- HALAMAN 1: SAMPAH ORGANIK ---
    if st.session_state.materi_aktif == "Sampah Organik":
        img_base64_org = get_base64_image("assets/images/Organik.png")
        
        # 1. Hero Banner Utama
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-text">
                <h2 class="hero-title">1. Sampah Organik</h2>
                <p class="hero-desc">Sampah organik adalah sampah yang berasal dari sisa makhluk hidup dan dapat terurai secara alami oleh mikroorganisme. Jika dipilah dengan benar, sampah ini sangat ramah lingkungan dan kaya nutrisi untuk dijadikan kompos pupuk alami.</p>
            </div>
            <div class="hero-image-container">
                <img src="{img_base64_org}" alt="Sampah Organik">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Karakteristik Sampah Organik
        st.markdown('<div class="section-title">Karakteristik Utama Sampah Organik</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🌱</div><div class="karakter-info-box"><div class="karakter-header">Mudah Terurai</div><div class="karakter-body">Hancur alami dalam hitungan hari hingga beberapa minggu saja.</div></div></div>""", unsafe_allow_html=True)
        with k_col2:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">♻️</div><div class="karakter-header">Ramah Lingkungan</div><div class="karakter-body">Tidak mencemari tanah, air, dan udara jika dikelola secara terpisah.</div></div></div>""", unsafe_allow_html=True)
        with k_col3:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🪴</div><div class="karakter-info-box"><div class="karakter-header">Bernilai Manfaat</div><div class="karakter-body">Sangat baik diolah menjadi kompos, pakan maggot, atau pupuk organik.</div></div></div>""", unsafe_allow_html=True)
        with k_col4:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🕒</div><div class="karakter-info-box"><div class="karakter-header">Waktu Terurai</div><div class="karakter-body">Antara 1 hingga 4 minggu tergantung kelembapan udara.</div></div></div>""", unsafe_allow_html=True)
            
        # 3. Contoh Sampah Organik Grid (5 Kolom)
        st.markdown('<div class="section-title">Contoh Sampah Organik Sehari-hari</div>', unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
        
        with c_col1:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/sisa_sayur.webp", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Sisa Sayuran & Buah</div><div class="contoh-desc">Potongan kulit buah, sayur layu, dan sisa racikan dapur.</div></div></div>', unsafe_allow_html=True)
            
        with c_col2:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/daun_kering.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Daun & Ranting Kering</div><div class="contoh-desc">Guguran daun halaman dan ranting kecil kaya unsur karbon.</div></div></div>', unsafe_allow_html=True)
            
        with c_col3:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/sisa_makanan.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Sisa Tulang & Nasi</div><div class="contoh-desc">Sisa lauk pauk dan nasi meja makan yang dapat diolah kembali.</div></div></div>', unsafe_allow_html=True)
            
        with c_col4:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/ampas_kopi.webp", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Ampas Kopi & Teh</div><div class="contoh-desc">Sisa seduhan kopi dan kantong teh celup bebas plastik.</div></div></div>', unsafe_allow_html=True)
            
        with c_col5:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/kulit_telur.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Kulit Telur</div><div class="contoh-desc">Cangkang telur kaya kalsium tinggi untuk menyuburkan tanah.</div></div></div>', unsafe_allow_html=True)

        # 4. FITUR BARU: Boleh vs Jangan Masuk Kompos (Do's & Don'ts)
        st.markdown('<div class="section-title">⚠️ Panduan Pemilahan Pengomposan Rumah Tangga</div>', unsafe_allow_html=True)
        dd_col1, dd_col2 = st.columns(2)
        with dd_col1:
            st.markdown("""
            <div class="dos-donts-box" style="border-left: 4px solid #166534;">
                <div class="dos-title">✅ Boleh Dimasukkan ke Kompos</div>
                <ul class="dos-list">
                    <li>Sisa potongan buah, kulit buah, dan sayuran dapur.</li>
                    <li>Ampas kopi, serbuk gergaji kayu, dan daun-daunan kering.</li>
                    <li>Cangkang telur yang sudah dihancurkan kasar.</li>
                    <li>Kertas koran polos atau tisu tanpa bahan kimia pekat.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with dd_col2:
            st.markdown("""
            <div class="dos-donts-box" style="border-left: 4px solid #991b1b;">
                <div class="donts-title">❌ Hindari Masuk Kompos Rutin</div>
                <ul class="donts-list">
                    <li><strong>Minyak Goreng Bekas / Jelantah:</strong> Membunuh bakteri pengurai & memicu bau busuk.</li>
                    <li><strong>Daging Berlemak & Tulang Besar:</strong> Mengundang tikus, lalat, dan belatung berbahaya.</li>
                    <li><strong>Kotoran Hewan Peliharaan (Kucing/Anjing):</strong> Berisiko membawa parasit/bakteri berbahaya.</li>
                    <li><strong>Tanaman Terserang Hama:</strong> Berpotensi menularkan penyakit ke tanaman baru.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 5. Langkah Konkret Pengelolaan & Ringkasan Materi
        b_col1, b_col2 = st.columns([1, 1])
        
        with b_col1:
            st.markdown('<div class="section-title">🧺 Langkah Praktis Pengelolaan di Rumah</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="tips-container">
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">1️⃣</div><span><strong>Pisahkan Langsung:</strong> Sediakan tempat sampah khusus organik berpenutup di dekat dapur.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">2️⃣</div><span><strong>Tiriskan Air:</strong> Pastikan sisa makanan tidak terlalu berair untuk mencegah bau menyengat.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">3️⃣</div><span><strong>Olah Sederhana:</strong> Masukkan ke ember komposter atau buat lubang biopori sederhana di pekarangan.</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with b_col2:
            st.markdown('<div class="section-title">📋 Ringkasan Poin Penting</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="ringkasan-box">
                <ul class="ringkasan-list">
                    <li>Sampah organik berasal murni dari sisa makhluk hidup.</li>
                    <li>Proses penguraiannya alami, cepat, dan tidak merusak lingkungan.</li>
                    <li>Dapat diubah menjadi kompos kaya nutrisi bagi tanah dan tanaman.</li>
                    <li>Memilah sampah organik secara mandiri memangkas 60% beban volume sampah di TPA.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 6. Bottom Navigation Bar
        st.markdown("""
        <div class="bottom-nav-box">
            <div class="bottom-nav-text">
                <span>📖</span>
                <span>Lanjutkan edukasi untuk memahami jenis sampah anorganik dan cara penanganannya!</span>
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
        img_base64_anorg = get_base64_image("assets/images/Anorganik.png")

        # 1. Hero Banner Anorganik Utama
        st.markdown(f"""
        <div class="hero-banner" style="background: linear-gradient(135deg, #7c2d12 0%, #b45309 100%); box-shadow: 0 4px 15px rgba(124, 45, 18, 0.15);">
            <div class="hero-text">
                <h2 class="hero-title">2. Sampah Anorganik</h2>
                <p class="hero-desc">Sampah anorganik adalah sampah yang berasal dari bahan sintetis atau olahan non-hayati yang sangat sulit hingga tidak bisa terurai alami. Perlu pengelolaan daur ulang agar tidak menumpuk ratusan tahun di bumi.</p>
            </div>
            <div class="hero-image-container">
                <img src="{img_base64_anorg}" alt="Sampah Anorganik">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Karakteristik Sampah Anorganik
        st.markdown('<div class="section-title anorganik">Karakteristik Utama Sampah Anorganik</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">⏳</div><div class="karakter-info-box"><div class="karakter-header">Sangat Sulit Terurai</div><div class="karakter-body">Membutuhkan waktu puluhan hingga ratusan tahun untuk hancur.</div></div></div>""", unsafe_allow_html=True)
        with k_col2:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">♻️</div><div class="karakter-info-box"><div class="karakter-header">Dapat Didaur Ulang</div><div class="karakter-body">Bisa dilebur dan diolah kembali menjadi barang bernilai ekonomi.</div></div></div>""", unsafe_allow_html=True)
        with k_col3:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">🧪</div><div class="karakter-info-box"><div class="karakter-header">Bahan Sintetis</div><div class="karakter-body">Hasil dari pemrosesan kimiawi pabrik, plastik, atau olahan tambang logam.</div></div></div>""", unsafe_allow_html=True)
        with k_col4:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">🌏</div><div class="karakter-info-box"><div class="karakter-header">Potensi Bahaya</div><div class="karakter-body">Bisa merusak ekosistem tanah dan laut jika dibuang begitu saja.</div></div></div>""", unsafe_allow_html=True)
            
        # 3. Contoh Sampah Anorganik Grid (5 Kolom)
        st.markdown('<div class="section-title anorganik">Contoh Sampah Anorganik Sehari-hari</div>', unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
        
        with c_col1:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/botol_plastik.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Botol & Plastik Kresek</div><div class="contoh-desc">Plastik PET/PE yang bernilai tinggi di bank sampah dan industri daur ulang.</div></div></div>', unsafe_allow_html=True)
            
        with c_col2:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/kaleng_logam.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Kaleng & Kemasan Logam</div><div class="contoh-desc">Aluminium dan seng yang dapat dilebur ulang tanpa menurunkan kualitasnya.</div></div></div>', unsafe_allow_html=True)
            
        with c_col3:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/botol_kaca.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Botol Kaca & Beling</div><div class="contoh-desc">Material kaca tahan lama yang dapat dipakai ulang atau didaur ulang.</div></div></div>', unsafe_allow_html=True)
            
        with c_col4:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/styrofoam.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Styrofoam Kemasan</div><div class="contoh-desc">Material ringan yang sangat beracun jika dibakar dan sulit terurai.</div></div></div>', unsafe_allow_html=True)
            
        with c_col5:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/baterai_elektronik.png", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Baterai & E-Waste</div><div class="contoh-desc">Limbah elektronik beracun (B3) yang butuh tempat penampungan khusus.</div></div></div>', unsafe_allow_html=True)

        # 4. FITUR BARU: Boleh vs Jangan Didaur Ulang Biasa (Do's & Don'ts)
        st.markdown('<div class="section-title anorganik">⚠️ Panduan Pemilahan Daur Ulang Anorganik</div>', unsafe_allow_html=True)
        dd_col1, dd_col2 = st.columns(2)
        with dd_col1:
            st.markdown("""
            <div class="dos-donts-box" style="border-left: 4px solid #b45309;">
                <div class="dos-title" style="color:#b45309;">✅ Diterima Bank Sampah / Didaur Ulang</div>
                <ul class="dos-list">
                    <li>Botol plastik minuman (PET), gelas plastik, dan kemasan botol shampoo (HDPE).</li>
                    <li>Kaleng minuman aluminium, seng, dan besi bekas.</li>
                    <li>Kardus bersih, kertas koran, buku, dan majalah bekas.</li>
                    <li>Botol kaca utuh atau wadah beling bersih.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with dd_col2:
            st.markdown("""
            <div class="dos-donts-box" style="border-left: 4px solid #991b1b;">
                <div class="donts-title">❌ Perlu Perlakuan Khusus / Jangan Dicampur</div>
                <ul class="donts-list">
                    <li><strong>Baterai & Lampu Bekas:</strong> Mengandung logam berat (B3), jangan dibuang di wadah sampah biasa!</li>
                    <li><strong>Plastik Kotor Berminyak:</strong> Bilas dulu dengan air sebelum disetorkan ke bank sampah.</li>
                    <li><strong>Pecahan Kaca Tajam:</strong> Bungkus aman dengan koran tebal agar tidak melukai petugas kebersihan.</li>
                    <li><strong>Kemasan Sachet Makanan Berlapis Aluminium:</strong> Kumpulkan terpisah untuk dibuat kreasi ecobricks.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 5. Langkah Konkret Pengelolaan & Ringkasan Materi Anorganik
        b_col1, b_col2 = st.columns([1, 1])
        
        with b_col1:
            st.markdown('<div class="section-title anorganik">🧺 Langkah 3R (Reduce, Reuse, Recycle)</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="tips-container">
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">1️⃣</div><span><strong>Bersihkan Dahulu:</strong> Cuci/bilas sisa minuman dari botol atau kaleng dan keringkan.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">2️⃣</div><span><strong>Pipihkan / Pipihkan:</strong> Remas botol plastik dan pipihkan kardus untuk menghemat ruang wadah.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">3️⃣</div><span><strong>Setor ke Bank Sampah:</strong> Tabung sampah anorganik bernilai ke bank sampah terdekat atau pemulung.</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with b_col2:
            st.markdown('<div class="section-title anorganik">📋 Ringkasan Poin Penting</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="ringkasan-box">
                <ul class="ringkasan-list">
                    <li>Sampah anorganik tidak dapat busuk secara alami.</li>
                    <li>Potensi ekonomi tinggi jika dikumpulkan dalam keadaan bersih dan terpisah.</li>
                    <li>Mengurangi penggunaan plastik sekali pakai adalah langkah terbaik (Reduce).</li>
                    <li>Pengelolaan anorganik mencegah pencemaran mikroplastik di rantai makanan kita.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 6. Bottom Navigation Bar Anorganik
        st.markdown("""
        <div class="bottom-nav-box" style="background: #fffbeb; border: 1px solid #fef08a;">
            <div class="bottom-nav-text" style="color: #b45309;">
                <span>📖</span>
                <span>Kamu telah mempelajari dasar pemilahan sampah! Saatnya mempraktikkan pemilahan di rumah.</span>
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