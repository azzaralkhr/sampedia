import streamlit as st
import base64
import os

def get_base64_image(image_path):
    """Fungsi untuk mengubah gambar lokal menjadi Base64 agar bisa dibaca tag HTML <img>"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return ""

# --- POP-UP DIALOG UNTUK PANDUAN CEPAT PEMBUANGAN ---
@st.dialog("🚨 Panduan Keamanan & Pembuangan Limbah B3")
def show_b3_dialog():
    st.error("**Baterai & Lampu Bekas Mengandung Logam Berat Beracun (Merkuri, Kadmium, Timbal)!**")
    st.write("""
    **Mengapa Bahaya?** Jika dibuang di tempat sampah biasa dan terurai di TPA, racun logam berat akan meresap ke dalam air tanah yang kita konsumsi dan memicu risiko penyakit berat seperti kanker.
    
    **Langkah Penanganan Aman:**
    1. **Jangan Dibakar / Dibuang ke Dapur:** Pisahkan dalam kotak/toples plastik khusus limbah B3.
    2. **Segel Kutub Baterai:** Tempelkan isolasi bening pada ujung (+/-) baterai untuk mencegah korsleting/percikan api.
    3. **Tujuan Pembuangan:** Setorkan ke *Drop Box E-Waste*, Kantor Dinas Lingkungan Hidup (DLH), atau Bank Sampah yang menerima limbah elektronik.
    """)
    if st.button("Saya Paham & Mengerti", use_container_width=True):
        st.rerun()

def render_page():
    # --- CSS CUSTOM UNTUK TAMPILAN MODERN, CLEAN & FLEKSIBEL ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
            background-color: #f8fafc;
        }
        
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* Sidebar Styling */
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

        /* Hero Banner */
        .hero-banner {
            background: linear-gradient(135deg, #0b4632 0%, #156347 100%);
            border-radius: 20px;
            padding: 30px 40px;
            color: white;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 25px rgba(11, 70, 50, 0.2);
        }
        
        .hero-text {
            max-width: 65%;
        }
        
        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff !important;
            margin: 0 0 10px 0 !important;
            letter-spacing: -0.5px;
        }
        
        .hero-desc {
            font-size: 1rem;
            font-weight: 400;
            color: #e2e8f0 !important;
            line-height: 1.6;
            margin: 0 !important;
        }
        
        .hero-image-container {
            max-width: 30%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .hero-image-container img {
            max-height: 150px;
            width: auto;
            object-fit: contain;
            filter: drop-shadow(0px 8px 16px rgba(0, 0, 0, 0.2));
        }

        /* Section Titles */
        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin: 20px 0 12px 0;
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
            padding: 14px;
            height: 100%;
            display: flex;
            gap: 12px;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .karakter-icon {
            font-size: 1.5rem;
            background: #e8f5e9;
            width: 42px;
            height: 42px;
            border-radius: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .karakter-icon.anorganik {
            background: #fef9c3;
        }
        
        .karakter-header {
            font-weight: 700;
            font-size: 0.9rem;
            color: #0f172a;
            margin-bottom: 2px;
        }
        
        .karakter-body {
            font-size: 0.8rem;
            color: #475569;
            line-height: 1.3;
        }

        /* Contoh Cards Container */
        .contoh-card-container {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            overflow: hidden;
            height: 100%;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }
        
        .contoh-content {
            padding: 10px;
            flex-grow: 1;
            border-top: 1px solid #f1f5f9;
        }
        
        .contoh-title {
            font-weight: 700;
            font-size: 0.85rem;
            color: #0f172a;
            margin-bottom: 4px;
        }
        
        .contoh-desc {
            font-size: 0.75rem;
            color: #64748b;
            line-height: 1.3;
        }

        /* Detail Box Styling */
        .detail-box {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 10px;
        }
        
        .detail-header {
            font-weight: 700;
            font-size: 0.95rem;
            color: #1e293b;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Tips & Ringkasan Box */
        .tips-container, .ringkasan-box {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .tips-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.83rem;
            color: #1e293b;
            margin-bottom: 10px;
        }
        
        .tips-badge {
            width: 28px;
            height: 28px;
            border-radius: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            flex-shrink: 0;
            font-weight: bold;
        }

        .ringkasan-list {
            margin: 0;
            padding-left: 18px;
            font-size: 0.83rem;
            color: #334155;
            line-height: 1.6;
        }
        
        .bottom-nav-box {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 12px;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 20px;
        }
        
        .bottom-nav-text {
            font-size: 0.88rem;
            color: #065f46;
            font-weight: 500;
        }

        .stButton button {
            font-weight: 600 !important;
            border-radius: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR NAVIGASI ---
    if 'materi_aktif' not in st.session_state:
        st.session_state.materi_aktif = "Sampah Organik"

    with st.sidebar:
        st.markdown('<div class="sidebar-title">📁 Menu Materi Edukasi</div>', unsafe_allow_html=True)
        
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
            st.markdown('<p style="font-size:0.8rem; color:#475569; line-height:1.5; margin-top:8px; margin-bottom:0;">Sampah organik yang tercampur plastik di TPA terperangkap tanpa udara, menghasilkan <b>gas metana</b> memicu ledakan TPA serta air lindi yang mencemari sumur warga.</p>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="tahu-title" style="color: #ca8a04;">🟡 Mengapa Pemilahan Penting?</div>', unsafe_allow_html=True)
            if os.path.exists("assets/images/tong_anorganik.png"):
                st.image("assets/images/tong_anorganik.png", use_container_width=True, output_format="PNG")
            st.markdown('<p style="font-size:0.8rem; color:#475569; line-height:1.5; margin-top:8px; margin-bottom:0;">Plastik butuh waktu hingga 500 tahun untuk hancur. Sampah anorganik liar akan pecah menjadi <b>mikroplastik</b> yang mengontaminasi air dan makanan kita.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    # =========================================================================
    # --- HALAMAN 1: SAMPAH ORGANIK ---
    # =========================================================================
    if st.session_state.materi_aktif == "Sampah Organik":
        img_base64_org = get_base64_image("assets/images/Organik.png")
        
        # 1. Hero Banner Utama
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-text">
                <h2 class="hero-title">1. Sampah Organik</h2>
                <p class="hero-desc">Sampah yang berasal dari sisa makhluk hidup (hayati) dan dapat terurai secara alami oleh mikroorganisme. Memilahnya secara terpisah mencegah bau busuk dan menghasilkan pupuk kaya nutrisi.</p>
            </div>
            <div class="hero-image-container">
                <img src="{img_base64_org}" alt="Sampah Organik">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Karakteristik Utama
        st.markdown('<div class="section-title">Karakteristik Utama Sampah Organik</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🌱</div><div><div class="karakter-header">Mudah Terurai</div><div class="karakter-body">Hancur alami dalam hitungan hari hingga beberapa minggu.</div></div></div>""", unsafe_allow_html=True)
        with k_col2:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">♻️</div><div><div class="karakter-header">Ramah Lingkungan</div><div class="karakter-body">Tidak merusak tanah atau air jika dikelola terpisah.</div></div></div>""", unsafe_allow_html=True)
        with k_col3:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🪴</div><div><div class="karakter-header">Bernilai Manfaat</div><div class="karakter-body">Ideal diolah jadi kompos, pupuk cair, atau pakan maggot.</div></div></div>""", unsafe_allow_html=True)
        with k_col4:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon">🕒</div><div><div class="karakter-header">Waktu Wajar</div><div class="karakter-body">Terurai penuh dalam 1-4 minggu tergantung kelembapan.</div></div></div>""", unsafe_allow_html=True)
            
        # 3. Contoh Sampah Organik Grid
        st.markdown('<div class="section-title">Contoh Sampah Organik Sehari-hari</div>', unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
        
        with c_col1:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/sisa_sayur.webp", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Sisa Sayur & Buah</div><div class="contoh-desc">Kulit buah, sisa racikan dapur yang kaya unsur hara.</div></div></div>', unsafe_allow_html=True)
        with c_col2:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/daun_kering.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Daun & Ranting</div><div class="contoh-desc">Guguran halaman kaya unsur karbon untuk penyeimbang kompos.</div></div></div>', unsafe_allow_html=True)
        with c_col3:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/sisa_makanan.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Sisa Nasi & Lauk</div><div class="contoh-desc">Sisa meja makan yang dapat diolah kembali menjadi pakan ternak/maggot.</div></div></div>', unsafe_allow_html=True)
        with c_col4:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/ampas_kopi.webp", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Ampas Kopi & Teh</div><div class="contoh-desc">Sisa seduhan kopi & kantong teh kertas penyubur media tanah.</div></div></div>', unsafe_allow_html=True)
        with c_col5:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/kulit_telur.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Cangkang Telur</div><div class="contoh-desc">Sumber kalsium tinggi untuk menutrisi akar tanaman.</div></div></div>', unsafe_allow_html=True)

        # 4. PENJELASAN KHUSUS DETAIL - EXPANDER INTERAKTIF (Mencegah Long Scroll)
        st.markdown('<div class="section-title">⚠️ Panduan Pemilahan Khusus & Pengomposan</div>', unsafe_allow_html=True)
        
        with st.expander("🔴 **KLIK DI SINI: Jenis Sampah Organik Khusus (Hindari Kompos Rutin)**", expanded=True):
            st.caption("Pilih jenis sampah di bawah untuk melihat alasan teknis, cara penanganan aman, dan lokasi pembuangannya:")
            
            tab_j1, tab_j2, tab_j3, tab_j4 = st.tabs([
                "🛢️ Minyak Jelantah", 
                "🥩 Daging & Tulang Besar", 
                "💩 Kotoran Hewan Peliharaan", 
                "🍂 Tanaman Hama/Sakit"
            ])
            
            with tab_j1:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b91c1c;">🛢️ Minyak Goreng Bekas (Jelantah)</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Mengapa Dilarang Masuk Kompos / Wastafel?</b><br>
                    Minyak akan melapisi bahan organik dan menutup pori-pori tanah, mematikan sirkulasi udara (oksigen), membunuh bakteri pengurai, serta menimbulkan bau busuk menyengat. Dibuang ke wastafel akan membeku dan menyumbat total saluran air rumah.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pengolahan & Cara Pembuangan Aman:</b><br>
                    1. Biarkan minyak dingin, lalu tuang ke dalam botol/jerigen plastik bekas.<br>
                    2. Tutup rapat agar tidak tumpah atau mencemari lingkungan.<br>
                    3. <b>Ke mana dibuang?</b> Kumpulkan dan setorkan ke <b>Bank Sampah</b> atau agen penampung jelantah terdekat untuk didaur ulang menjadi <b>biodiesel</b> atau <b>sabun cuci</b>.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with tab_j2:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b91c1c;">🥩 Daging Berlemak & Tulang Besar</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Mengapa Dilarang Masuk Kompos Biasa?</b><br>
                    Lemak hewan membusuk sangat lambat dan memicu bau bangkai yang dapat mengundang hama seperti tikus, lalat hijau, belatung, dan hewan pemangsa lainnya ke wadah kompos.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pengolahan & Cara Pembuangan Aman:</b><br>
                    1. <b>Metode Komposter Bokashi (Anaerob):</b> Gunakan ember tertutup dengan starter mikroorganisme efektif (EM4) yang mampu mengurai lemak.<br>
                    2. <b>Lubang Biopori Dalam:</b> Tanam dalam Lubang Resapan Biopori (LRB) di tanah minimal kedalaman 1 meter lalu uruk kembali dengan tanah rapat-rapat.</p>
                </div>
                """, unsafe_allow_html=True)

            with tab_j3:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b91c1c;">💩 Kotoran Hewan Peliharaan (Kucing / Anjing)</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Mengapa Dilarang Masuk Kompos Sayuran?</b><br>
                    Kotoran hewan karnivora/omnivora berisiko tinggi membawa parasit beracun (seperti <i>Toxoplasma gondii</i>) dan bakteri patogen yang dapat bertahan hidup dan menulari tanaman pangan yang kita makan.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pengolahan & Cara Pembuangan Aman:</b><br>
                    1. Buat lubang galian khusus di sudut pekarangan yang jauh dari sumber air minum/sumur (minimal jarak 10 meter).<br>
                    2. Buang kotoran ke lubang tersebut dan tutup rapat dengan tanah secara bertahap.<br>
                    3. <b>Jangan Pernah</b> dicampur ke kompos tanaman buah/sayuran dapur!</p>
                </div>
                """, unsafe_allow_html=True)

            with tab_j4:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b91c1c;">🍂 Tanaman Terserang Hama & Jamur</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Mengapa Dilarang Masuk Kompos?</b><br>
                    Spora jamur, virus tanaman, atau telur hama tidak selalu mati selama proses pengomposan dingin. Tanaman sakit yang dikomposkan justru akan menularkan penyakit ke seluruh media tanaman baru.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pengolahan & Cara Pembuangan Aman:</b><br>
                    1. Keringkan tanaman yang sakit di bawah terik matahari.<br>
                    2. Bakar secara terbatas dalam wadah tertutup, atau bungkus rapat dalam kantong sampah residu untuk dibuang ke TPA.</p>
                </div>
                """, unsafe_allow_html=True)

        # 5. Langkah Konkret & Ringkasan
        b_col1, b_col2 = st.columns([1, 1])
        with b_col1:
            st.markdown('<div class="section-title">🧺 Langkah Praktis Pengelolaan di Rumah</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="tips-container">
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">1</div><span><b>Pisahkan Langsung:</b> Sediakan tempat sampah khusus organik berpenutup di area dapur.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">2</div><span><b>Tiriskan Air:</b> Tiriskan sisa makanan dari kuah/air sebelum dibuang agar tidak bau busuk.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#e8f5e9; color:#2e7d32;">3</div><span><b>Olah Mandiri:</b> Masukkan ke komposter sederhana atau lubang biopori pekarangan.</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with b_col2:
            st.markdown('<div class="section-title">📋 Ringkasan Poin Penting</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="ringkasan-box">
                <ul class="ringkasan-list">
                    <li>Sampah organik berasal dari sisa hayati/makhluk hidup.</li>
                    <li>Penguraian berlangsung cepat dan ramah lingkungan jika dipilah.</li>
                    <li>Dapat diubah menjadi pupuk organik kaya nutrisi.</li>
                    <li>Memilah sampah organik dari rumah memangkas hingga 60% beban sampah ke TPA.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 6. Bottom Navigation Bar
        st.markdown("""
        <div class="bottom-nav-box">
            <div class="bottom-nav-text">
                <span>📖 Lanjutkan edukasi untuk memahami jenis sampah anorganik dan perlakuan khususnya!</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns([3, 1])
        with col_b2:
            if st.button("Lanjut ke Anorganik ➡️", key="btn_next_anorg", use_container_width=True):
                st.session_state.materi_aktif = "Sampah Anorganik"
                st.rerun()


    # =========================================================================
    # --- HALAMAN 2: SAMPAH ANORGANIK ---
    # =========================================================================
    elif st.session_state.materi_aktif == "Sampah Anorganik":
        img_base64_anorg = get_base64_image("assets/images/Anorganik.png")

        # 1. Hero Banner Anorganik Utama
        st.markdown(f"""
        <div class="hero-banner" style="background: linear-gradient(135deg, #7c2d12 0%, #b45309 100%);">
            <div class="hero-text">
                <h2 class="hero-title">2. Sampah Anorganik</h2>
                <p class="hero-desc">Sampah dari bahan sintetis atau olahan non-hayati yang sangat sulit hingga tidak bisa terurai alami. Wajib dikelola dengan prinsip 3R (Reduce, Reuse, Recycle) agar tidak menumpuk ratusan tahun di bumi.</p>
            </div>
            <div class="hero-image-container">
                <img src="{img_base64_anorg}" alt="Sampah Anorganik">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Karakteristik Utama
        st.markdown('<div class="section-title anorganik">Karakteristik Utama Sampah Anorganik</div>', unsafe_allow_html=True)
        k_col1, k_col2, k_col3, k_col4 = st.columns(4)
        with k_col1:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">⏳</div><div><div class="karakter-header">Sulit Terurai</div><div class="karakter-body">Membutuhkan puluhan hingga ratusan tahun untuk hancur.</div></div></div>""", unsafe_allow_html=True)
        with k_col2:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">♻️</div><div><div class="karakter-header">Bisa Didaur Ulang</div><div class="karakter-body">Dapat dilebur & diolah jadi produk baru bernilai ekonomi.</div></div></div>""", unsafe_allow_html=True)
        with k_col3:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">🧪</div><div><div class="karakter-header">Bahan Sintetis</div><div class="karakter-body">Hasil pemrosesan kimiawi pabrik, plastik, atau olahan logam.</div></div></div>""", unsafe_allow_html=True)
        with k_col4:
            st.markdown("""<div class="karakter-card"><div class="karakter-icon anorganik">🌏</div><div><div class="karakter-header">Potensi Bahaya</div><div class="karakter-body">Bisa menjadi limbah mikroplastik beracun jika dibakar/dibuang liar.</div></div></div>""", unsafe_allow_html=True)
            
        # 3. Contoh Sampah Anorganik Grid
        st.markdown('<div class="section-title anorganik">Contoh Sampah Anorganik Sehari-hari</div>', unsafe_allow_html=True)
        c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns(5)
        
        with c_col1:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/botol_plastik.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Botol & Plastik</div><div class="contoh-desc">Plastik PET/HDPE bernilai tinggi di bank sampah & daur ulang.</div></div></div>', unsafe_allow_html=True)
        with c_col2:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/kaleng_logam.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Kaleng & Logam</div><div class="contoh-desc">Aluminium & seng yang bisa dilebur berulang kali tanpa merusak mutu.</div></div></div>', unsafe_allow_html=True)
        with c_col3:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/botol_kaca.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Kaca & Beling</div><div class="contoh-desc">Material kaca tahan lama yang dapat dipakai ulang secara higienis.</div></div></div>', unsafe_allow_html=True)
        with c_col4:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/styrofoam.jpg", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Styrofoam</div><div class="contoh-desc">Sangat sulit terurai & beracun jika terkena panas makanan/dibakar.</div></div></div>', unsafe_allow_html=True)
        with c_col5:
            st.markdown('<div class="contoh-card-container">', unsafe_allow_html=True)
            st.image("assets/images/baterai_elektronik.png", use_container_width=True)
            st.markdown('<div class="contoh-content"><div class="contoh-title">Baterai & E-Waste</div><div class="contoh-desc">Limbah elektronik beracun (B3) yang butuh penanganan khusus.</div></div></div>', unsafe_allow_html=True)

        # 4. PENJELASAN KHUSUS DETAIL - EXPANDER INTERAKTIF (Anorganik Khusus)
        st.markdown('<div class="section-title anorganik">⚠️ Perlakuan Khusus & Tata Cara Daur Ulang</div>', unsafe_allow_html=True)
        
        # Pop-Up Dialog Quick Action
        if st.button("🚨 Klik di Sini untuk Peringatan Khusus Baterai & Limbah B3", use_container_width=True):
            show_b3_dialog()

        with st.expander("🟡 **KLIK DI SINI: Panduan Daur Ulang & Penanganan Kaca/Plastik/Sachet**", expanded=True):
            st.caption("Pilih tab di bawah untuk mempelajari cara aman mengolah sampah anorganik khusus:")
            
            tab_a1, tab_a2, tab_a3, tab_a4 = st.tabs([
                "🪫 Baterai & Lampu (B3)", 
                "🔪 Pecahan Kaca Tajam", 
                "🧽 Plastik Berminyak", 
                "🧃 Sachet Aluminium"
            ])
            
            with tab_a1:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b45309;">🪫 Baterai Bekas & Lampu Neon (Limbah B3)</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Risiko Bahaya:</b> Mengandung logam berat berbahaya (Merkuri, Kadmium, Timbal). Jika dibuang di tempat sampah biasa, racun dapat meresap ke dalam air tanah dan memicu kanker.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pembuangan Aman:</b><br>
                    1. <b>Jangan Pernah Dibakar / Dibuang Dapur!</b> Kumpulkan terpisah di kotak/toples khusus B3.<br>
                    2. Tutup kutub positif-negatif baterai dengan lakban bening untuk cegah percikan api.<br>
                    3. <b>Ke mana dibuang?</b> Bawa ke <i>Drop Box E-Waste</i> di pusat perbelanjaan, Kantor Dinas Lingkungan Hidup (DLH), atau Bank Sampah terdekat.</p>
                </div>
                """, unsafe_allow_html=True)

            with tab_a2:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b45309;">🔪 Pecahan Kaca & Beling Tajam</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Risiko Bahaya:</b> Sangat mudah merobek kantong sampah dan melukai tangan petugas kebersihan/pemulung saat diangkut.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pembuangan Aman:</b><br>
                    1. Bungkus pecahan kaca secara berlapis menggunakan koran tebal atau masukkan ke dalam kardus bekas yang kokoh.<br>
                    2. Lakban seluruh permukaan bungkus kardus hingga rapi.<br>
                    3. <b>Tuliskan Label Tegas:</b> Tuliskan kalimat <i>"AWAS PECAHAN KACA TAJAM"</i> menggunakan spidol hitam tebal di luar bungkus sebelum dibuang.</p>
                </div>
                """, unsafe_allow_html=True)

            with tab_a3:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b45309;">🧽 Plastik Kotor & Berminyak</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Risiko Bahaya:</b> Sisa lemak/minyak memicu bau busuk dan membusukkan sampah kering lain. Mesin daur ulang di Bank Sampah akan menolak plastik yang kotor.</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Pembuangan Aman:</b><br>
                    1. Bilas wadah/botol plastik dengan sedikit air sabun bekas cuci piring.<br>
                    2. Tiriskan hingga benar-benar kering.<br>
                    3. Setelah bersih & kering, satukan dengan wadah anorganik untuk disetorkan ke Bank Sampah.</p>
                </div>
                """, unsafe_allow_html=True)

            with tab_a4:
                st.markdown("""
                <div class="detail-box">
                    <div class="detail-header" style="color: #b45309;">🧃 Kemasan Sachet Aluminium Foil (Multi-layer)</div>
                    <p style="font-size: 0.85rem; color: #334155;"><b>❌ Risiko Bahaya:</b> Terdiri dari campuran plastik dan lapisan aluminium foil yang tidak bisa dilebur oleh mesin daur ulang biasa (bernilai jual nol di pemulung).</p>
                    <p style="font-size: 0.85rem; color: #1e293b;"><b>💡 Solusi Daur Ulang Kreatif:</b><br>
                    1. <b>Kreasi Ecobricks:</b> Gunting sachet kecil-kecil, lalu masukkan dan padatkan ke dalam botol plastik bekas menggunakan tongkat hingga keras. Bisa dijadikan meja/kursi.<br>
                    2. Kumpulkan terpisah dan salurkan ke Bank Sampah yang memiliki fasilitas pengolah limbah menjadi bahan bakar alternatif (<i>Refuse-Derived Fuel / RDF</i>).</p>
                </div>
                """, unsafe_allow_html=True)

        # 5. Langkah Konkret & Ringkasan Anorganik
        b_col1, b_col2 = st.columns([1, 1])
        with b_col1:
            st.markdown('<div class="section-title anorganik">🧺 Langkah 3R (Reduce, Reuse, Recycle)</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="tips-container">
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">1</div><span><b>Bersihkan & Keringkan:</b> Bilas sisa minuman/makanan dari botol atau kaleng.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">2</div><span><b>Pipihkan Kardus/Botol:</b> Remas botol & pipihkan kardus untuk menghemat ruang tempat sampah.</span></div>
                <div class="tips-item"><div class="tips-badge" style="background:#fffbeb; color:#b45309;">3</div><span><b>Setor ke Bank Sampah:</b> Tabung sampah anorganik bersih menjadi uang tunai di Bank Sampah.</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with b_col2:
            st.markdown('<div class="section-title anorganik">📋 Ringkasan Poin Penting</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="ringkasan-box">
                <ul class="ringkasan-list">
                    <li>Sampah anorganik tidak dapat membusuk atau terurai alami.</li>
                    <li>Sangat bernilai ekonomi tinggi jika dikumpulkan bersih dan terpisah.</li>
                    <li>Mengurangi penggunaan plastik sekali pakai adalah pilihan terbaik (Reduce).</li>
                    <li>Pemilahan tepat mencegah ancaman mikroplastik di rantai makanan kita.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # 6. Bottom Navigation Bar Anorganik
        st.markdown("""
        <div class="bottom-nav-box" style="background: #fffbeb; border: 1px solid #fef08a;">
            <div class="bottom-nav-text" style="color: #b45309;">
                <span>📖 Selamat! Anda telah mempelajari seluruh materi dasar pemilahan sampah secara komprehensif.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_b1, col_b2 = st.columns([3, 1])
        with col_b2:
            if st.button("↩️ Kembali ke Organik", key="btn_back_org", use_container_width=True):
                st.session_state.materi_aktif = "Sampah Organik"
                st.rerun()

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Sampedia - Ruang Edukasi")
    render_page()