import streamlit as st
from PIL import Image
import colorsys
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Fungsi untuk setiap halaman
def halaman_utama():
    st.title("Project UTS Pengolahan Citra")
    st.write("Pada website ini kami membuat beberapa project pengolahan citra.")
    st.write("Silakan pilih pada sidebar untuk melihat project yang telah saya buat.")

def rgb_hsv():
    st.title("Mengkonversi Gambar RGB ke HSV")
    st.write("Ini adalah halaman untuk mengkonversi gambar dari format RGB ke HSV.")

    def rgb_to_hsv_image(image):
        img_array = np.array(image)

        r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]

        r = r / 255.0
        g = g / 255.0
        b = b / 255.0

        hsv_array = np.zeros_like(img_array, dtype=float)

        for i in range(r.shape[0]):
            for j in range(r.shape[1]):
                h, s, v = colorsys.rgb_to_hsv(r[i, j], g[i, j], b[i, j])
                hsv_array[i, j, 0] = h * 360  # Konversi H ke derajat 0-360
                hsv_array[i, j, 1] = s * 100  # Konversi S ke persen 0-100
                hsv_array[i, j, 2] = v * 100  # Konversi V ke persen 0-100

        hsv_image = Image.fromarray(np.uint8(hsv_array), 'RGB')

        return hsv_image

    uploaded_file = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar Asli (RGB)", use_column_width=True)

        hsv_image = rgb_to_hsv_image(image)
        st.image(hsv_image, caption="Gambar dalam Format HSV", use_column_width=True)

def histogram():
    st.title("Menghitung Histogram Pada Foto")
    st.write("Ini adalah halaman untuk menghitung histogram pada foto.")

    def hitung_histogram(gambar):
        # Menghitung histogram untuk setiap kanal warna
        warna = ('b', 'g', 'r')  # Warna: blue, green, red
        histogram = {}

        for i, col in enumerate(warna):
            histogram[col] = cv2.calcHist([gambar], [i], None, [256], [0, 256])

        return histogram

    def tampilkan_histogram(histogram):
        # Menampilkan histogram menggunakan Matplotlib
        plt.figure()
        plt.title("Histogram Gambar")
        plt.xlabel("Intensitas Warna")
        plt.ylabel("Jumlah Piksel")

        for col, hist in histogram.items():
            plt.plot(hist, color=col)
            plt.xlim([0, 256])

        st.pyplot(plt)

    uploaded_file = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        gambar = cv2.imdecode(file_bytes, 1)
        
        if gambar is not None:
            histogram = hitung_histogram(gambar)
            tampilkan_histogram(histogram)
        else:
            st.write("Gagal memuat gambar. Periksa path gambar.")

def ubah_kecerahan_kontras():
    st.title("Mengubah Brightness dan Kontras")
    st.write("Ini adalah halaman untuk mengubah kecerahan dan kontras gambar.")

    def ubah_kontras(gambar, alpha=1.0, beta=0):
        # Mengubah kecerahan dan kontras
        gambar_baru = cv2.convertScaleAbs(gambar, alpha=alpha, beta=beta)
        return gambar_baru

    def tampilkan_gambar(gambar_asli, gambar_baru):
        # Menampilkan gambar asli dan gambar baru menggunakan Matplotlib
        plt.figure(figsize=(10, 5))

        # Gambar asli
        plt.subplot(1, 2, 1)
        plt.title("Gambar Asli")
        plt.imshow(cv2.cvtColor(gambar_asli, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        # Gambar baru
        plt.subplot(1, 2, 2)
        plt.title("Gambar Baru")
        plt.imshow(cv2.cvtColor(gambar_baru, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        st.pyplot(plt)

    uploaded_file = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        gambar = cv2.imdecode(file_bytes, 1)

        if gambar is not None:
            alpha = st.slider('Kontras', 0.1, 3.0, 1.0)
            beta = st.slider('Kecerahan', -100, 100, 0)
            gambar_baru = ubah_kontras(gambar, alpha, beta)

            tampilkan_gambar(gambar, gambar_baru)
        else:
            st.write("Gagal memuat gambar. Periksa path gambar.")

def ubah_kontur():
    st.title("Mengubah Kontur pada Gambar")
    st.write("Ini adalah halaman untuk mendeteksi dan mengubah kontur pada gambar.")

    def ubah_kontur_gambar(gambar, warna=(0, 255, 0), ketebalan=2):
        # Mengubah gambar ke grayscale
        gray = cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)
        
        # Menggunakan threshold untuk mendapatkan gambar biner
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Mendeteksi kontur
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Membuat salinan gambar untuk menggambar kontur
        gambar_kontur = np.copy(gambar)
        
        # Menggambar kontur pada gambar
        cv2.drawContours(gambar_kontur, contours, -1, warna, ketebalan)
        
        return gambar_kontur

    uploaded_file = st.file_uploader("Pilih file gambar", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Membaca gambar menggunakan PIL, lalu mengonversi ke format OpenCV
        image = Image.open(uploaded_file)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Menampilkan gambar asli
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption="Gambar Asli", use_column_width=True)
        
        # Slider untuk memilih ketebalan kontur
        ketebalan = st.slider('Ketebalan Kontur', 1, 10, 2)
        
        # Memproses gambar untuk mengubah kontur
        gambar_kontur = ubah_kontur_gambar(image, ketebalan=ketebalan)
        
        # Menampilkan gambar dengan kontur yang diubah
        st.image(cv2.cvtColor(gambar_kontur, cv2.COLOR_BGR2RGB), caption="Gambar dengan Kontur", use_column_width=True)

# Buat menu di sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio(
    "Pilih halaman:",
    ("Halaman Utama", "RGB to HSV", "Menghitung Histogram", "Mengubah Brightness dan Contrast", "Mengubah Contour")
)

# Pindah halaman berdasarkan pilihan menu
if menu == "Halaman Utama":
    halaman_utama()
elif menu == "RGB to HSV":
    rgb_hsv()
elif menu == "Menghitung Histogram":
    histogram()
elif menu == "Mengubah Brightness dan Contrast":
    ubah_kecerahan_kontras()
elif menu == "Mengubah Contour":
    ubah_kontur()
