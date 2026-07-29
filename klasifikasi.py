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

    # 1. Konversi BGR (OpenCV) -> RGB (Sama seperti image.load_img di Keras)
    if len(img_bgr.shape) == 3 and img_bgr.shape[2] == 3:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img_bgr

    # 2. Resize ke target_size (224, 224)
    img_resized = cv2.resize(img_rgb, (224, 224))
    
    # 3. Terapkan Preprocessing khusus ResNet50 (Bukan /255.0)
    img_preprocessed = resnet50_preprocess_input(img_resized)

    # 4. Tambahkan Batch Dimension (axis=0)
    img_input = np.expand_dims(img_preprocessed, axis=0)

    # 5. Jalankan Inferensi Model
    interpreter.set_tensor(input_details[0]['index'], img_input)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])

    # 6. Logika Klasifikasi (Persis dari Colab: prob = float(pred[0][0]))
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
    Memotong (crop) tepat di bagian tengah gambar berukuran target_size x target_size (224x224).
    Jika ukuran gambar lebih kecil dari target_size, lakukan penyesuaian otomatis.
    """
    h, w, _ = img_bgr.shape
    
    # Menentukan ukuran crop (maksimal selebar/setinggi gambar jika terlalu kecil)
    box_w = min(w, target_size)
    box_h = min(h, target_size)
    
    x1 = w // 2 - box_w // 2
    y1 = h // 2 - box_h // 2
    x2 = x1 + box_w
    y2 = y1 + box_h
    
    # Lakukan cropping tepat di area tengah 224x224
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
        font-size: 15px;
        color: #0f172a;
        line-height: 1.5;
    }
    .rekomendasi-header {
        color: #0f291b;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .banjir-container {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 16px;
        border-radius: 10px;
        font-size: 15px;
        color: #0f172a;
        line-height: 1.6;
    }
    .banjir-header {
        color: #15803d;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 6px;
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

    .stDetails summary {
        font-size: 15px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        font-size: 14px !important;
        line-height: 1.6 !important;
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

    # TATA LETAK 2 KOLOM SEIMBANG
    col_left, col_right = st.columns(2)

    # =====================================
    # KOLOM KIRI (INPUT & FOTO + TIPS PENGISI SPACE)
    # =====================================
    with col_left:
        with st.container(border=True):
            if "Kamera HP/Webcam" in pilihan_metode:
                st.markdown("<div class='card-inside-title'>📸 Tangkap Foto dari Kamera</div>", unsafe_allow_html=True)
                st.info("💡 **Petunjuk:** Arahkan objek sampah ke tengah layar, lalu tekan **Take Photo**.")
                
                cam_photo = st.camera_input("Ambil Foto Sampah")
                
                if cam_photo is not None:
                    file_bytes = np.asarray(bytearray(cam_photo.read()), dtype=np.uint8)
                    img_captured = cv2.imdecode(file_bytes, 1)
                    
                    # Potong bagian tengah berukuran 224x224
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

            # Pengisi Dead Space di Kolom Kiri
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

    # =====================================
    # KOLOM KANAN (HASIL & AKSI RINGKAS)
    # =====================================
    with col_right:
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>🏷️ Hasil Klasifikasi</div>", unsafe_allow_html=True)
            
            if st.session_state.pred_label is not None and st.session_state.pred_label != "Unknown":
                # Tampilkan pratinjau gambar tanpa teks teknis '224x224'
                st.image(st.session_state.pred_img, caption="Pratinjau Foto Sampah", use_container_width=False)
                
                if st.session_state.pred_label == "Organic":
                    st.markdown(f"""
                    <div class='banner-organik'>
                        <h2 style='margin: 0; color: #156347; font-size: 24px; font-weight: 800;'>🟢 SAMPAH ORGANIK</h2>
                        <p style='margin: 4px 0 0 0; color: #16a34a; font-weight: 700; font-size: 15px;'>Tingkat Keyakinan Sistem: {st.session_state.pred_conf * 100:.1f}%</p>
                        <div class='bin-status bin-organik'>🗑️ Masukkan ke: Tong Sampah Hijau</div>
                    </div>
                    
                    <div class='rekomendasi-container'>
                        <div class='rekomendasi-header'>📋 TINDAKAN DIREKOMENDASIKAN:</div>
                        <ul style='margin: 0; padding-left: 18px; color: #0f172a; font-weight: 600;'>
                            <li style='margin-bottom: 4px;'><b>Pisahkan Segera:</b> Masukkan ke kompartemen wadah hijau khusus sisa organik.</li>
                            <li><b>Daur Ulang Hayati:</b> Olah menjadi pupuk kompos tanaman rumahan.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                        
                else:
                    st.markdown(f"""
                    <div class='banner-anorganik'>
                        <h2 style='margin: 0; color: #d97706; font-size: 24px; font-weight: 800;'>🟡 ANORGANIK (RECYCLABLE)</h2>
                        <p style='margin: 4px 0 0 0; color: #b45309; font-weight: 700; font-size: 15px;'>Tingkat Keyakinan Sistem: {st.session_state.pred_conf * 100:.1f}%</p>
                        <div class='bin-status bin-anorganik'>🗑️ Masukkan ke: Tong Sampah Kuning</div>
                    </div>
                    
                    <div class='rekomendasi-container' style='border-left-color: #d97706;'>
                        <div class='rekomendasi-header'>📋 TINDAKAN DIREKOMENDASIKAN:</div>
                        <ul style='margin: 0; padding-left: 18px; color: #0f172a; font-weight: 600;'>
                            <li style='margin-bottom: 4px;'><b>Bilas & Bersihkan:</b> Pastikan kemasan kosong dari zat cair sisa konsumsi.</li>
                            <li><b>Setor Bank Sampah:</b> Kumpulkan secara kolektif untuk ditukar nilai ekonomi.</li>
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

    # =====================================
    # PANDUAN & EDUKASI LANJUTAN (FULL WIDTH - BAWAH)
    # =====================================
    if st.session_state.pred_label is not None and st.session_state.pred_label != "Unknown":
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>📖 Panduan Pengolahan & Dampak Lingkungan</div>", unsafe_allow_html=True)
            
            col_edu_1, col_edu_2 = st.columns(2)
            
            if st.session_state.pred_label == "Organic":
                with col_edu_1:
                    st.markdown("""
                    <div class='banjir-container'>
                        <div class='banjir-header'>🌊 Pengaruh Pada Drainase Kota:</div>
                        Membuang sisa makanan ke selokan menciptakan sedimentasi lumpur yang menyumbat jalur air. Mengolahnya sendiri di rumah secara drastis mengurangi risiko banjir lokal!
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_edu_2:
                    with st.expander("📖 Pelajari Cara Pembuatan Kompos Sederhana", expanded=True):
                        st.markdown("""
                        1. **Persiapan:** Sediakan wadah tertutup yang telah diberi lubang udara kecil di sekelilingnya.
                        2. **Penyusunan:** Campurkan sampah organik basah (sisa sayur) dengan bahan kering (daun/tanah) secara seimbang.
                        3. **Pematangan:** Aduk seminggu sekali, dalam kurun waktu sekitar 4-6 minggu pupuk organik siap dipanen.
                        """)
            else:
                with col_edu_1:
                    st.markdown("""
                    <div class='banjir-container' style='background: #fff5f5; border-left-color: #ef4444;'>
                        <div class='banjir-header' style='color: #991b1b;'>⚠️ Bahaya Tersumbatnya Aliran Air:</div>
                        Komponen plastik/kaleng tidak terurai secara alami. Sifatnya yang mengapung berisiko tinggi mengunci pintu air utama penahan luapan banjir.
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_edu_2:
                    with st.expander("📖 Kiat Optimalisasi Setoran Bank Sampah", expanded=True):
                        st.markdown("""
                        * **Kempiskan Botol:** Pipihkan botol plastik atau kaleng aluminium untuk memperbanyak daya tampung wadah Anda.
                        * **Kelompokkan Material:** Kelompokkan plastik keras (HDPE), botol transparan (PET), dan kertas karton agar nilai ekonomisnya lebih tinggi.
                        """)

if __name__ == "__main__":
    render_page()