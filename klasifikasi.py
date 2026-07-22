import streamlit as st
import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import os

# =====================================
# LOAD MODEL & PREDICT FUNCTION OUTSIDE
# =====================================
# Menggunakan os.path untuk mengunci lokasi pasti file model di Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "BO_Resnet_5class.tflite")

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def predict_image(img):
    img = cv2.resize(img, (224, 224))
    img = img.astype(np.float32)
    img = np.expand_dims(img, axis=0)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    pred = interpreter.get_tensor(output_details[0]['index'])
    prob = float(pred[0][0])

    if prob > 0.5:
        label = "Recyclable"
        confidence = prob
    else:
        label = "Organic"
        confidence = 1 - prob

    return label, confidence

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.crop = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        h, w, _ = img.shape
        box_size = 220
        x1 = w // 2 - box_size // 2
        y1 = h // 2 - box_size // 2
        x2 = x1 + box_size
        y2 = y1 + box_size

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(img, "Arahkan Sampah", (x1 + 5, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        self.crop = img[y1:y2, x1:x2]
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# =====================================
# RENDER PAGE - DESAIN PREMIUM INTERAKTIF & AKSESIBEL
# =====================================
def render_page():
    # INJEKSI CSS MODERN DENGAN UKURAN TEKS DIPERBESAR
    st.markdown("""
    <style>
    /* Reset Font Global & Judul */
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
    
    /* Teks Pilihan Metode Radio Button */
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
    
    /* Container Wadah Utama */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 22px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        border: 1px solid #e2e8f0 !important;
        margin-bottom: 20px !important;
    }
    
    /* Penataan Judul Kartu */
    .card-inside-title {
        font-size: 20px;
        font-weight: 800;
        color: #0f291b;
        margin-bottom: 16px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 10px;
    }
    
    /* Memaksa Tampilan Gambar Deteksi Proporsional */
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
    
    /* Tombol Aksi Keren Eksklusif Hijau */
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

    /* Container Edukasi Penanggulangan Banjir */
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

    /* Container Rekomendasi Alur Tindakan */
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
    
    /* Placeholder Menunggu Hasil */
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

    /* Penyesuaian Komponen Expander */
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

    # Wadah Pilihan Utama
    with st.container(border=True):
        pilihan_metode = st.radio(
            "Pilih Metode Masukan Gambar:",
            ("📷 Kamera Real-time", "📂 Unggah Berkas Foto"),
            horizontal=True,
            key="pilihan_metode_klasifikasi_baru"
        )

    if 'pred_label' not in st.session_state:
        st.session_state.pred_label = None
        st.session_state.pred_conf = 0.0
        st.session_state.pred_img = None

    col_left, col_right = st.columns(2)

    # --- PANEL SEBELAH KIRI (WADAH INPUT) ---
    with col_left:
        with st.container(border=True):
            if "Kamera" in pilihan_metode:
                st.markdown("<div class='card-inside-title'>📷 Pengambilan Berbasis Kamera</div>", unsafe_allow_html=True)
                
                ctx = webrtc_streamer(
                    key="cam-capture-v3",
                    video_processor_factory=VideoProcessor,
                    media_stream_constraints={
                        "video": {"width": 480, "height": 360},
                        "audio": False
                    }
                )
                
                st.write("") 
                btn_cam = st.button("✨ Pindai & Analisis Sekarang", key="btn_capture_cam_v3")
                
                if btn_cam:
                    if ctx.video_processor:
                        image = ctx.video_processor.crop
                        if image is not None:
                            with st.spinner("Memproses gambar dari kamera..."):
                                label, confidence = predict_image(image)
                                st.session_state.pred_label = label
                                st.session_state.pred_conf = confidence
                                st.session_state.pred_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        else:
                            st.error("Gagal merekam gambar! Harap posisikan objek tepat di dalam batas kotak.")
                    else:
                        st.info("Klik tombol 'Start' di atas panel untuk menghidupkan kamera perangkat.")

            else:
                st.markdown("<div class='card-inside-title'>📂 Unggah File Foto</div>", unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Pilih gambar dari galeri Anda (.jpg, .png)", type=["jpg", "jpeg", "png"], key="uploader_v3")
                
                if uploaded_file is not None:
                    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                    img_uploaded = cv2.imdecode(file_bytes, 1)
                    
                    st.write("")
                    btn_upload = st.button("✨ Proses File Unggahan", key="btn_process_upload_v3")
                    
                    if btn_upload:
                        with st.spinner("Membaca berkas digital..."):
                            label_up, confidence_up = predict_image(img_uploaded)
                            st.session_state.pred_label = label_up
                            st.session_state.pred_conf = confidence_up
                            st.session_state.pred_img = cv2.cvtColor(img_uploaded, cv2.COLOR_BGR2RGB)

    # --- PANEL SEBELAH KANAN (HASIL & PANDUAN) ---
    with col_right:
        with st.container(border=True):
            st.markdown("<div class='card-inside-title'>📊 Dashboard Hasil & Aksi</div>", unsafe_allow_html=True)
            
            if st.session_state.pred_label is not None:
                st.image(st.session_state.pred_img, caption="Foto Objek Dideteksi", use_container_width=False)
                
                if st.session_state.pred_label == "Organic":
                    # Tampilan Badge Kategori Organik (Ukuran Teks Diperbesar)
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
                    # Tampilan Badge Kategori Anorganik (Ukuran Teks Diperbesar)
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