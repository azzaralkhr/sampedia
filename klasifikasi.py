import streamlit as st
import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
import os

# =====================================
# LOAD MODEL DENGAN CACHE & MEMORY MAPPING
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "BO_Resnet_5class.tflite")

@st.cache_resource
def load_tflite_model(model_path):
    """
    Memuat model TFLite secara akurat.
    """
    if not os.path.exists(model_path):
        st.error(f"❌ File model tidak ditemukan di path: {model_path}")
        return None
    
    file_size = os.path.getsize(model_path)
    if file_size < 1000:
        st.error("❌ File model `.tflite` rusak atau terpotong saat di-upload ke GitHub.")
        return None

    try:
        interpreter = Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter
    except Exception as e:
        st.error(f"❌ Gagal menginisialisasi TFLite Interpreter: {e}")
        return None

# Memuat model sekali secara global
interpreter = load_tflite_model(MODEL_PATH)

def resnet50_preprocess_input(x):
    """
    Implementasi persis tensorflow.keras.applications.resnet50.preprocess_input
    1. Konversi RGB -> BGR
    2. Zero-center setiap saluran warna sesuai rata-rata ImageNet:
       R_mean = 123.68, G_mean = 116.779, B_mean = 103.939
    """
    x = x.astype(np.float32)
    # Konversi RGB ke BGR jika inputnya RGB
    x = x[..., ::-1]
    # Kurangi rata-rata ImageNet (skala BGR)
    x[..., 0] -= 103.939  # B
    x[..., 1] -= 116.779  # G
    x[..., 2] -= 123.68   # R
    return x

def predict_image(img_bgr):
    """
    Fungsi prediksi yang disesuaikan persis dengan Notebook Colab Pelatihan.
    """
    if interpreter is None:
        st.error("Model TFLite gagal dimuat. Harap periksa file model Anda.")
        return "Unknown", 0.0

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # 1. Konversi BGR (OpenCV) -> RGB
    if len(img_bgr.shape) == 3 and img_bgr.shape[2] == 3:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img_bgr

    # 2. Resize ke target_size (224, 224)
    img_resized = cv2.resize(img_rgb, (224, 224))
    
    # 3. Terapkan Preprocessing khusus ResNet50
    img_preprocessed = resnet50_preprocess_input(img_resized)

    # 4. Tambahkan Batch Dimension
    img_input = np.expand_dims(img_preprocessed, axis=0)

    # 5. Jalankan Inferensi Model
    interpreter.set_tensor(input_details[0]['index'], img_input)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])

    # 6. Logika Klasifikasi
    prob = float(pred[0][0])

    if prob > 0.5:
        label = "Recyclable"
        confidence = prob
    else:
        label = "Organic"
        confidence = 1.0 - prob

    return label, confidence

def crop_center_box(img_bgr, target_size=224):
    """
    Memotong (crop) tepat di bagian tengah gambar berukuran target_size x target_size.
    """
    h, w, _ = img_bgr.shape
    box_w = min(w, target_size)
    box_h = min(h, target_size)
    
    x1 = w // 2 - box_w // 2
    y1 = h // 2 - box_h // 2
    x2 = x1 + box_w
    y2 = y1 + box_h
    
    cropped_img = img_bgr[y1:y2, x1:x2]
    return cropped_img

# =====================================
# RENDER PAGE
# =====================================
def render_page():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .title { 
        text-align: center; 
        font-size: 34px; 
        font-weight: 800; 
        color: #0f291b; 
        margin-top: 5px; 
        margin-bottom: 6px; 
    }
    .sub { 
        text-align: center; 
        font-size: 16px; 
        color: #475569; 
        margin-bottom: 25px; 
        font-weight: 500;
    }
    
    div[data-testid="stRadio"] label {
        color: #0f172a !important; 
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04) !important;
        border: 1px solid #e2e8f0 !important;
        margin-bottom: 16px !important;
    }
    
    .card-inside-title {
        font-size: 19px;
        font-weight: 800;
        color: #0f291b;
        margin-bottom: 14px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 8px;
    }
    
    div[data-testid="stImage"] img {
        width: 100% !important;
        max-width: 220px !important;
        height: 180px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        border: 2px solid #cbd5e1;
        margin: 0 auto !important;
        display: block;
    }
    
    .stButton > button {
        width: 100% !important;
        height: 48px !important;
        border: none !important;
        border-radius: 10px !important;
        background: #10b981 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
    }
    .stButton > button:hover {
        background: #059669 !important;
        box-shadow: 0 6px 16px rgba(5, 150, 105, 0.35) !important;
        transform: translateY(-1px);
    }

    /* Banners & Cards */
    .banner-organik {
        background-color: #f0fdf4;
        border: 2px solid #86efac;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 14px;
    }
    .banner-anorganik {
        background-color: #fffbeb;
        border: 2px solid #fde68a;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 14px;
    }

    .bin-status {
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 15px;
        margin-top: 10px;
        display: inline-block;
    }
    .bin-organik {
        background-color: #dcfce7;
        color: #156347;
        border: 1px solid #86efac;
    }
    .bin-anorganik {
        background-color: #fef3c7;
        color: #d97706;
        border: 1px solid #fde68a;
    }

    .rekomendasi-container {
        background: #f8fafc;
        border-left: 5px solid #10b981;
        padding: 14px 16px;
        border-radius: 8px;
        margin-top: 12px;
        font-size: 14px;
        color: #0f172a;
        line-height: 1.6;
    }

    .tips-box {
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        padding: 14px;
        border-radius: 12px;
        margin-top: 14px;
        font-size: 14px;
        color: #334155;
    }
    
    .placeholder-result {
        border: 2px dashed #cbd5e1;
        padding: 60px 20px;
        border-radius: 12px;
        text-align: center;
        color: #64748b;
        font-size: 15px;
        background: #fafafa;
        line-height: 1.6;
    }

    /* Edukasi & Grid Style */
    .edu-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px;
        height: 100%;
    }
    .edu-title {
        font-weight: 800;
        font-size: 15px;
        color: #0f291b;
        margin-bottom: 6px;
    }
    .edu-desc {
        font-size: 13px;
        color: #475569;
        line-height: 1.5;
    }

    .stDetails summary {
        font-size: 15px !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>♻️ Klasifikasi Jenis Sampah</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Gunakan salah satu fitur di bawah ini untuk mengidentifikasi kategori sampah Anda secara otomatis.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        pilihan_metode = st.radio(
            "Pilih Metode Masukan Gambar:",
            ("📸 Kamera HP/Webcam", "📂 Unggah Berkas Foto"),
            horizontal=True,
            key="pilihan_metode_klasifikasi_baru"
        )

    if 'pred_label' not in st.session_state:
        st.session_state.pred_label = None
        st.session_state.pred_conf = 0.0
        st.session_state.pred_img = None

    # ========================================================================================
    # BAGIAN 1: INPUT & HASIL UTAMA (2 Kolom Seimbang)
    # ========================================================================================
    col_left, col_right = st.columns(2)

    # --- KOLOM KIRI: INPUT ---
    with col_left:
        with st.container(border=True):
            if "Kamera HP/Webcam" in pilihan_metode:
                st.markdown("<div class='card-inside-title'>📸 Tangkap Foto dari Kamera</div>", unsafe_allow_html=True)
                st.info("💡 **Petunjuk:** Arahkan objek sampah ke tengah layar, lalu tekan **Take Photo**.")
                
                cam_photo = st.camera_input("Ambil Foto Sampah")
                
                if cam_photo is not None:
                    file_bytes = np.asarray(bytearray(cam_photo.read()), dtype=np.uint8)
                    img_captured = cv2.imdecode(file_bytes, 1)
                    img_cropped = crop_center_box(img_captured, target_size=224)
                    
                    with st.spinner("Menganalisis gambar..."):
                        label, confidence = predict_image(img_cropped)
                        st.session_state.pred_label = label
                        st.session_state.pred_conf = confidence
                        st.session_state.pred_img = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)

            else:
                st.markdown("<div class='card-inside-title'>📂 Unggah File Foto</div>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Pilih gambar dari galeri Anda (.jpg, .png)", type=["jpg", "jpeg", "png"], key="uploader_v4")
                
                if uploaded_file is not None:
                    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                    img_uploaded = cv2.imdecode(file_bytes, 1)
                    
                    st.write("")
                    btn_upload = st.button("✨ Proses File Unggahan", key="btn_process_upload_v4")
                    
                    if btn_upload:
                        with st.spinner("Menganalisis gambar..."):
                            label_up, confidence_up = predict_image(img_uploaded)
                            st.session_state.pred_label = label_up
                            st.session_state.pred_conf = confidence_up
                            st.session_state.pred_img = cv2.cvtColor(img_uploaded, cv2.COLOR_BGR2RGB)

            # Tips Foto Akurat
            st.markdown("""
            <div class='tips-box'>
                <b style='color: #0f291b; font-size: 15px;'>💡 Tips Foto untuk Hasil Akurat:</b>
                <ul style='margin-top: 6px; margin-bottom: 0; padding-left: 18px; line-height: 1.6;'>
                    <li>Pastikan pencahayaan cukup terang.</li>
                    <li>Fokuskan hanya pada <b>satu objek sampah</b>.</li>
                    <li>Gunakan latar belakang yang kontras/bersih.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # --- KOLOM KANAN: HASIL REKAP SANGAT RINGKAS ---
    with col_right:
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>🏷️ Hasil Klasifikasi</div>", unsafe_allow_html=True)
            
            if st.session_state.pred_label is not None and st.session_state.pred_label != "Unknown":
                st.image(st.session_state.pred_img, caption="Pratinjau Foto Sampah", use_container_width=False)
                
                if st.session_state.pred_label == "Organic":
                    st.markdown(f"""
                    <div class='banner-organik'>
                        <h2 style='margin: 0; color: #156347; font-size: 22px; font-weight: 800;'>🟢 SAMPAH ORGANIK</h2>
                        <p style='margin: 2px 0 0 0; color: #16a34a; font-weight: 700; font-size: 14px;'>Akurasi System: {st.session_state.pred_conf * 100:.1f}%</p>
                        <div class='bin-status bin-organik'>🗑️ Masukkan ke: TONG SAMPAH HIJAU</div>
                    </div>
                    
                    <div class='rekomendasi-container'>
                        <b>💧 LANGKAH AWAL (3 Detik):</b>
                        <ul style='margin: 4px 0 8px 0; padding-left: 18px;'>
                            <li>Tiriskan kuah/airnya terlebih dahulu.</li>
                        </ul>
                        
                        <b style='color: #dc2626;'>❌ PANTANGAN:</b>
                        <ul style='margin: 4px 0 8px 0; padding-left: 18px;'>
                            <li>DILARANG dibuang ke selokan/got.</li>
                            <li>DILARANG dibungkus plastik rapat.</li>
                        </ul>
                        
                        <b>🌱 MANFAAT LANGSUNG:</b>
                        <ul style='margin: 4px 0 8px 0; padding-left: 18px;'>
                            <li>Tanam di pot atau olah jadi kompos.</li>
                        </ul>
                        
                        <b>💡 CONTOH SEJENIS:</b>
                        <ul style='margin: 4px 0 0 0; padding-left: 18px;'>
                            <li>Sisa sayur, dedaunan, ampas teh.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                        
                else:
                    st.markdown(f"""
                    <div class='banner-anorganik'>
                        <h2 style='margin: 0; color: #d97706; font-size: 22px; font-weight: 800;'>🟡 SAMPAH ANORGANIK</h2>
                        <p style='margin: 2px 0 0 0; color: #b45309; font-weight: 700; font-size: 14px;'>Akurasi System: {st.session_state.pred_conf * 100:.1f}%</p>
                        <div class='bin-status bin-anorganik'>🗑️ Masukkan ke: TONG SAMPAH KUNING</div>
                    </div>
                    
                    <div class='rekomendasi-container' style='border-left-color: #d97706;'>
                        <b>💧 LANGKAH AWAL (3 Detik):</b>
                        <ul style='margin: 4px 0 8px 0; padding-left: 18px;'>
                            <li>Kosongkan dan bilas sisa cairan/makanan.</li>
                        </ul>
                        
                        <b style='color: #dc2626;'>❌ PANTANGAN:</b>
                        <ul style='margin: 4px 0 8px 0; padding-left: 18px;'>
                            <li>DILARANG membakar sampah plastik/kaleng.</li>
                            <li>DILARANG mencampur dengan sampah basah.</li>
                        </ul>
                        
                        <b>🌱 MANFAAT LANGSUNG:</b>
                        <ul style='margin: 4px 0 8px 0; padding-left: 18px;'>
                            <li>Dapat didaur ulang / disetor ke Bank Sampah.</li>
                        </ul>
                        
                        <b>💡 CONTOH SEJENIS:</b>
                        <ul style='margin: 4px 0 0 0; padding-left: 18px;'>
                            <li>Botol plastik, kaleng minuman, kardus.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='placeholder-result'>
                    🔍 <b style='font-size: 17px; color: #334155;'>Sistem Siap Menerima Data</b><br><br>
                    Silakan unggah atau ambil foto sampah di panel sebelah kiri untuk melihat hasil analisis.
                </div>
                """, unsafe_allow_html=True)

    # Jika sudah ada hasil prediksi, tampilkan Bagian 2, 3, dan 4 di bawah (Full Width)
    if st.session_state.pred_label is not None and st.session_state.pred_label != "Unknown":
        
        # ========================================================================================
        # BAGIAN 2: PANDUAN MEMBUAT KOMPOS (EXPANDER) (Full Width)
        # ========================================================================================
        if st.session_state.pred_label == "Organic":
            with st.container(border=True):
                st.markdown("<div class='card-inside-title'>📖 Panduan Pengolahan Sampah</div>", unsafe_allow_html=True)
                
                with st.expander("📖 Pelajari Cara Pembuatan Kompos Sederhana di Rumah", expanded=False):
                    st.markdown("""
                    <ol style='line-height: 1.8; font-size: 14px; color: #1e293b; margin-bottom: 0;'>
                        <li><b>Persiapan:</b> Sediakan wadah tertutup (ember/tong) yang telah diberi lubang-lubang udara kecil di sekelilingnya.</li>
                        <li><b>Penyusunan:</b> Campurkan sampah organik basah (sisa sayur/buah) dengan bahan kering (daun kering/tanah/serbuk kayu) secara seimbang.</li>
                        <li><b>Pematangan:</b> Aduk seminggu sekali untuk sirkulasi udara. Dalam kurun waktu sekitar <b>4–6 minggu</b>, pupuk organik siap dipanen!</li>
                    </ol>
                    """, unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown("<div class='card-inside-title'>📖 Panduan Daur Ulang Anorganik</div>", unsafe_allow_html=True)
                
                with st.expander("📖 Pelajari Cara Pengolahan & Penyetoran Anorganik", expanded=False):
                    st.markdown("""
                    <ol style='line-height: 1.8; font-size: 14px; color: #1e293b; margin-bottom: 0;'>
                        <li><b>Pembersihan:</b> Bilas wadah plastik atau kaleng hingga bersih dari sisa makanan/minuman agar tidak mengundang hama.</li>
                        <li><b>Pemilahan:</b> Kelompokkan sampah berdasarkan jenisnya (plastik PET, kertas/kardus, atau logam).</li>
                        <li><b>Penyetoran:</b> Pipihkan botol/dus untuk menghemat ruang, lalu setor ke Bank Sampah terdekat untuk didaur ulang.</li>
                    </ol>
                    """, unsafe_allow_html=True)

        # ========================================================================================
        # BAGIAN 3: EDUKASI PENGECUALIAN KOMPOS / PEMILAHAN KHUSUS (Full Width)
        # ========================================================================================
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>⚠️ Panduan Pemilahan Khusus & Pengecualian</div>", unsafe_allow_html=True)
            
            with st.expander("KLIK DI SINI: Jenis Sampah Organik Khusus (Hindari Kompos Rutin)", expanded=False):
                col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
                
                with col_ex1:
                    st.markdown("""
                    <div class='edu-card'>
                        <div class='edu-title'>🛢️ Minyak Jelantah</div>
                        <div class='edu-desc'><b>Alasan:</b> Menutupi pori tanah & menyumbat saluran.<br><b>Solusi:</b> Kumpulkan dalam jerigen, setor ke Bank Sampah untuk biodiesel.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_ex2:
                    st.markdown("""
                    <div class='edu-card'>
                        <div class='edu-title'>🍗 Daging & Tulang</div>
                        <div class='edu-desc'><b>Alasan:</b> Memicu bau busuk menyengat & mengundang tikus/alat.<br><b>Solusi:</b> Tanam langsung di tanah dalam (metode biopori).</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_ex3:
                    st.markdown("""
                    <div class='edu-card'>
                        <div class='edu-title'>💩 Kotoran Hewan</div>
                        <div class='edu-desc'><b>Alasan:</b> Berisiko membawa parasit/bakteri berbahaya.<br><b>Solusi:</b> Olah khusus pada komposter fermentasi terpisah.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_ex4:
                    st.markdown("""
                    <div class='edu-card'>
                        <div class='edu-title'>🍂 Tanaman Sakit</div>
                        <div class='edu-desc'><b>Alasan:</b> Spora jamur/hama bisa menulari tanaman lain.<br><b>Solusi:</b> Buang terpisah atau bakar secara aman.</div>
                    </div>
                    """, unsafe_allow_html=True)

        # ========================================================================================
        # BAGIAN 4: KERUGIAN LINGKUNGAN JIKA TIDAK DIOLAH (Full Width Paling Bawah)
        # ========================================================================================
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>🌍 Bahaya Sampah Organik Jika Cuma Dibuang Begitu Saja</div>", unsafe_allow_html=True)
            
            col_danger1, col_danger2 = st.columns(2)
            
            with col_danger1:
                st.markdown("""
                <div class='edu-card' style='background: #fef2f2; border-color: #fca5a5;'>
                    <div class='edu-title' style='color: #991b1b;'>💥 Bahaya Gas Metana (TPA Meledak)</div>
                    <div class='edu-desc' style='color: #7f1d1d;'>
                        Sampah organik yang terperangkap di TPA tanpa udara akan mengalami pembusukan anaerobik dan menghasilkan <b>gas metana</b>. Gas ini sangat mudah terbakar, memicu ledakan TPA, serta menjadi gas rumah kaca yang 28x lebih berbahaya dari CO2.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col_danger2:
                st.markdown("""
                <div class='edu-card' style='background: #eff6ff; border-color: #93c5fd;'>
                    <div class='edu-title' style='color: #1e40af;'>🌊 Penyumbatan & Banjir Lokal</div>
                    <div class='edu-desc' style='color: #1e3a8a;'>
                        Membuang sisa makanan atau sampah basah ke selokan/got menciptakan endapan lumpur padat yang membusuk. Endapan ini mempersempit aliran air dan menjadi penyebab utama pendangkalan saluran pemicu banjir lokal.
                    </div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_page()