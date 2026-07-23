import streamlit as st
import cv2
import numpy as np
from ai_edge_litert.interpreter import Interpreter
import os
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode, RTCConfiguration

# =====================================
# RTC CONFIGURATION FOR CLOUD DEPLOY
# =====================================
RTC_CONFIG = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

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

    # 4. Tambahkan Batch Dimension (axis=0)
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
    Memotong (crop) bagian tengah berukuran 224x224 piksel
    """
    h, w, _ = img_bgr.shape
    box_w = min(w, target_size)
    box_h = min(h, target_size)
    
    x1 = w // 2 - box_w // 2
    y1 = h // 2 - box_h // 2
    x2 = x1 + box_w
    y2 = y1 + box_h
    
    return img_bgr[y1:y2, x1:x2]

# =====================================
# WEBRTC VIDEO TRANSFORMER DENGAN OVERLAY KOTAK
# =====================================
class WasteClassifierTransformer(VideoTransformerBase):
    def __init__(self):
        self.latest_frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape

        # Tentukan posisi kotak 224x224 di tengah layar live webcam
        box_w, box_h = 224, 224
        x1 = max(0, w // 2 - box_w // 2)
        y1 = max(0, h // 2 - box_h // 2)
        x2 = min(w, x1 + box_w)
        y2 = min(h, y1 + box_h)

        # Simpan frame asli untuk diproses saat tombol dipencet
        self.latest_frame = img.copy()

        # Gambar Bounding Box Hijau & Teks Panduan pada Tampilan Kamera
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(
            img, 
            "Arahkan Sampah Ke Sini", 
            (x1 - 10, y1 - 15), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (0, 255, 0), 
            2, 
            cv2.LINE_AA
        )

        return img

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
        font-size: 36px; 
        font-weight: 800; 
        color: #0f291b; 
        margin-top: 10px; 
        margin-bottom: 8px; 
    }
    .sub { 
        text-align: center; 
        font-size: 17px; 
        color: #475569; 
        margin-bottom: 30px; 
        font-weight: 500;
    }
    
    div[data-testid="stRadio"] label {
        color: #0f172a !important; 
        font-size: 17px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 17px !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 22px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        border: 1px solid #e2e8f0 !important;
        margin-bottom: 20px !important;
    }
    
    .card-inside-title {
        font-size: 20px;
        font-weight: 800;
        color: #0f291b;
        margin-bottom: 16px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 10px;
    }
    
    div[data-testid="stImage"] img {
        width: 100% !important;
        max-width: 240px !important;
        height: 190px !important;
        object-fit: cover !important;
        border-radius: 12px !important;
        border: 2px solid #cbd5e1;
        margin: 0 auto !important;
        display: block;
    }
    
    .stButton > button {
        width: 100% !important;
        height: 50px !important;
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

    .banjir-container {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 16px;
        border-radius: 10px;
        margin-top: 16px;
        font-size: 16px;
        color: #0f172a;
        line-height: 1.6;
    }
    .banjir-header {
        color: #15803d;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .rekomendasi-container {
        background: #f8fafc;
        border-left: 5px solid #475569;
        padding: 16px;
        border-radius: 10px;
        margin-top: 16px;
        font-size: 16px;
        color: #0f172a;
        line-height: 1.6;
    }
    .rekomendasi-header {
        color: #334155;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    
    .placeholder-result {
        border: 2px dashed #cbd5e1;
        padding: 70px 20px;
        border-radius: 12px;
        text-align: center;
        color: #475569;
        font-size: 16px;
        background: #fafafa;
        line-height: 1.6;
    }

    .stDetails summary {
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
        font-size: 15px !important;
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

    col_left, col_right = st.columns(2)

    with col_left:
        with st.container(border=True):
            if "Kamera HP/Webcam" in pilihan_metode:
                st.markdown("<div class='card-inside-title'>📸 Live Kamera Webcam</div>", unsafe_allow_html=True)
                st.info("💡 **Petunjuk:** Arahkan objek sampah ke dalam **kotak hijau**, lalu klik tombol **Klasifikasikan Sampah** di bawah video.")
                
                # Menampilkan Stream Webcam beserta Bounding Box Hijau secara Real-time
                ctx = webrtc_streamer(
                    key="waste-classifier",
                    mode=WebRtcMode.SENDRECV,
                    rtc_configuration=RTC_CONFIG,
                    video_transformer_factory=WasteClassifierTransformer,
                    media_stream_constraints={"video": True, "audio": False},
                    async_processing=True
                )

                st.write("")
                btn_capture = st.button("📸 Klasifikasikan Sampah dalam Kotak", key="btn_capture_webrtc")

                if btn_capture:
                    if ctx.video_transformer and ctx.video_transformer.latest_frame is not None:
                        # Ambil frame mentah
                        img_raw = ctx.video_transformer.latest_frame
                        # Potong tepat 224x224 di tengah
                        img_cropped = crop_center_box(img_raw, target_size=224)
                        
                        with st.spinner("Menganalisis area kotak..."):
                            label, confidence = predict_image(img_cropped)
                            st.session_state.pred_label = label
                            st.session_state.pred_conf = confidence
                            st.session_state.pred_img = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
                    else:
                        st.warning("⚠️ Kamera belum aktif atau belum siap. Silakan klik 'START' pada panel kamera terlebih dahulu.")

            else:
                st.markdown("<div class='card-inside-title'>📂 Unggah File Foto</div>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Pilih gambar dari galeri Anda (.jpg, .png)", type=["jpg", "jpeg", "png"], key="uploader_v4")
                
                if uploaded_file is not None:
                    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                    img_uploaded = cv2.imdecode(file_bytes, 1)
                    
                    st.write("")
                    btn_upload = st.button("✨ Proses File Unggahan", key="btn_process_upload_v4")
                    
                    if btn_upload:
                        with st.spinner("Membaca berkas digital..."):
                            label_up, confidence_up = predict_image(img_uploaded)
                            st.session_state.pred_label = label_up
                            st.session_state.pred_conf = confidence_up
                            st.session_state.pred_img = cv2.cvtColor(img_uploaded, cv2.COLOR_BGR2RGB)

    with col_right:
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>📊 Dashboard Hasil & Aksi</div>", unsafe_allow_html=True)
            
            if st.session_state.pred_label is not None and st.session_state.pred_label != "Unknown":
                st.image(st.session_state.pred_img, caption="Hasil Cropping Area Kotak (224x224)", use_container_width=False)
                
                if st.session_state.pred_label == "Organic":
                    st.markdown(f"""
                    <div style='background-color: #eff6ff; border: 2px solid #93c5fd; padding: 18px; border-radius: 12px; text-align: center; margin-top: 12px;'>
                        <h2 style='margin: 0; color: #1e40af; font-size: 26px; font-weight: 800;'>🍂 SAMPAH ORGANIK</h2>
                        <p style='margin: 6px 0 0 0; color: #2563eb; font-weight: 700; font-size: 16px;'>Tingkat Keyakinan System: {st.session_state.pred_conf * 100:.1f}%</p>
                    </div>
                    
                    <div class='rekomendasi-container'>
                        <div class='rekomendasi-header'>📋 TINDAKAN YANG DIREKOMENDASIKAN:</div>
                        <ol style='margin: 0; padding-left: 20px; color: #0f172a; font-weight: 600;'>
                            <li style='margin-bottom: 6px;'><b>Pisahkan Segera:</b> Masukkan ke kompartemen wadah hijau khusus sisa organik.</li>
                            <li><b>Daur Ulang Hayati:</b> Olah menjadi pupuk kompos tanaman rumahan.</li>
                        </ol>
                    </div>
                    
                    <div class='banjir-container'>
                        <div class='banjir-header'>🌊 Pengaruh Pada Drainase Kota:</div>
                        Membuang sisa makanan ke selokan menciptakan sedimentasi lumpur yang menyumbat jalur air. Mengolahnya sendiri di rumah secara drastis mengurangi risiko banjir lokal!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    with st.expander("📖 Pelajari Cara Pembuatan Kompos Sederhana"):
                        st.markdown("""
                        1. **Persiapan:** Sediakan wadah tertutup yang telah diberi lubang udara kecil di sekelilingnya.
                        2. **Penyusunan:** Campurkan sampah organik basah (sisa sayur) dengan bahan kering (daun/tanah) secara seimbang.
                        3. **Pematangan:** Aduk seminggu sekali, dalam kurun waktu sekitar 4-6 minggu pupuk organik siap dipanen.
                        """)
                        
                else:
                    st.markdown(f"""
                    <div style='background-color: #fffbeb; border: 2px solid #fde68a; padding: 18px; border-radius: 12px; text-align: center; margin-top: 12px;'>
                        <h2 style='margin: 0; color: #92400e; font-size: 26px; font-weight: 800;'>🍾 ANORGANIK (RECYCLABLE)</h2>
                        <p style='margin: 6px 0 0 0; color: #d97706; font-weight: 700; font-size: 16px;'>Tingkat Keyakinan System: {st.session_state.pred_conf * 100:.1f}%</p>
                    </div>
                    
                    <div class='rekomendasi-container'>
                        <div class='rekomendasi-header'>📋 TINDAKAN YANG DIREKOMENDASIKAN:</div>
                        <ol style='margin: 0; padding-left: 20px; color: #0f172a; font-weight: 600;'>
                            <li style='margin-bottom: 6px;'><b>Bilas & Bersihkan:</b> Pastikan kemasan kosong dari zat cair sisa konsumsi.</li>
                            <li><b>Kumpulkan secara Kolektif:</b> Setorkan ke Bank Sampah terdekat untuk ditukar barang ekonomi.</li>
                        </ol>
                    </div>
                    
                    <div class='banjir-container' style='background: #fff5f5; border-left: 5px solid #ef4444;'>
                        <div class='banjir-header' style='color: #991b1b;'>⚠️ Bahaya Tersumbatnya Aliran Air:</div>
                        Komponen plastik/kaleng tidak terurai secara alami. Sifatnya yang mengapung berisiko tinggi mengunci pintu air utama penahan luapan banjir.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    with st.expander("📖 Kiat Optimalisasi Setoran Bank Sampah"):
                        st.markdown("""
                        * **Kempiskan Botol:** Pipihkan botol plastik atau kaleng aluminium untuk memperbanyak daya tampung kantong pilah Anda.
                        * **Kelompokkan Material:** Kelompokkan plastik keras (HDPE), botol transparan (PET), dan kertas karton agar nilai ekonomisnya dinilai lebih tinggi.
                        """)
            else:
                st.markdown("""
                <div class='placeholder-result'>
                    🔍 <b style='font-size: 18px;'>Sistem Siap Menerima Data</b><br><br>
                    Gunakan panel masukan di sebelah kiri untuk menampilkan hasil analisis kecerdasan buatan.
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_page()