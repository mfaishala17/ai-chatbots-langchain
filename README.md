# ⚡ IoT & Microcontroller Code Assistant

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-3.6_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)

> **Final Project Hacktiv8**: *LLM-Based Tools and Gemini API Integration for Data Scientists*  
> **Author / Developer**: **Muhammad Faisal Abdurrahman**

---

## 📌 Tentang Proyek

**IoT & Microcontroller Code Assistant** adalah aplikasi chatbot interaktif berbasis **Streamlit** dan **LangChain** yang terintegrasi dengan model generasi terbaru **Google Gemini (gemini-3.6-flash)**. 

Aplikasi ini dirancang khusus untuk menjadi konsultan virtual bagi maker, pelajar, dan embedded engineer dalam:
- **Troubleshooting & Debugging**: Memecahkan error kompilasi C++/MicroPython, runtime crash (Guru Meditation Error, WDT reset, brownout).
- **Hardware Wiring & Desain Rangkaian**: Menyediakan panduan pin-ke-pin yang presisi untuk sensor analog/digital, modul komunikasi, aktuator, dan display (OLED/LCD).
- **Protokol IoT**: Membantu konfigurasi konektivitas jaringan (MQTT, HTTP REST, ESP-NOW, BLE, LoRa, Wi-Fi).
- **Tanya-Jawab Interaktif & Proaktif**: Secara cerdas menanyakan detail hardware (level tegangan 3.3V vs 5V, tipe board, pinout) jika pengguna memberikan informasi yang belum lengkap guna mencegah kerusakan komponen fisik.

---

## ✨ Fitur Unggulan

| Fitur | Deskripsi |
| :--- | :--- |
| ⚡ **Respon Real-Time Streaming** | Respon AI tampil mengalir kata demi kata secara instan (*streaming tokens*) menggunakan `client.stream` & `st.write_stream`, menghilangkan waktu tunggu lama. |
| 🗂️ **Multi-Session Chat History** | Tampilan sidebar bergaya modern (*ChatGPT / IDE style*) dengan menu *Chats and tasks*, pembuatan percakapan baru (`➕`), pergantian sesi aktif, dan tombol hapus sesi (`✕`). |
| 🎨 **Dukungan Tema Lengkap** | Pilihan tema fleksibel di pojok kanan atas: **🌙 Dark Mode**, **☀️ Light Mode**, dan **💻 System Mode** (mengikuti preferensi OS/browser secara otomatis). |
| 🤖 **Persona Expert IoT & Proaktif** | Dilengkapi instruksi sistem mendalam yang tidak hanya menjawab, namun **proaktif mengajukan pertanyaan klarifikasi** jika detail sensor atau board belum lengkap. |
| ⚙️ **Popup Pengaturan Interaktif** | Konfigurasi model AI, pengaturan *temperature slider* (kreativitas vs presisi), pemilihan gaya bahasa (*Professional* vs *Casual*), dan penggantian API Key via modal dialog popup. |
| 🔐 **Onboarding Aman** | Form input API Key yang elegan di tengah layar sebelum sesi dimulai, mencegah eksposur kredensial di kode publik. |

---

## 🛠️ Arsitektur & Teknologi

- **Frontend & UI**: [Streamlit](https://streamlit.io/) dengan Custom Modern CSS (CSS Variables, Flexbox, Glassmorphism elements).
- **LLM Framework**: [LangChain](https://python.langchain.com/) (`langchain-core`, `langchain-google-genai`).
- **Foundation Model**: `gemini-3.6-flash` dari Google AI.
- **Language**: Python 3.9+.

---

## 📁 Struktur Direktori

```text
ai-chatbots-langchain/
├── app.py              # Aplikasi utama Streamlit (UI, Logika LangChain, Streaming)
├── requirements.txt    # Daftar dependensi Python
├── README.md           # Dokumentasi resmi proyek
└── .gitignore          # Konfigurasi proteksi file rahasia & cache
```

---

## 🚀 Panduan Instalasi & Menjalankan Lokal

### 1. Prasyarat
Pastikan Anda telah menginstal **Python 3.9 atau lebih baru** di sistem Anda.

### 2. Clone Repositori
```bash
git clone  https://github.com/mfaishala17/ai-chatbots-langchain.git
cd ai-chatbots-langchain
```

### 3. Buat dan Aktifkan Virtual Environment (Opsional namun Disarankan)
- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependensi
```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
```bash
streamlit run app.py
```
Aplikasi akan terbuka otomatis di browser Anda pada alamat: `http://localhost:8501`.

---

## 📖 Cara Penggunaan

1. **Masukkan Google Gemini API Key:**
   - Saat aplikasi pertama kali dibuka, masukkan Gemini API Key Anda pada kotak yang tersedia di tengah layar.
   - Jika belum memiliki API Key, dapatkan secara gratis di [Google AI Studio](https://aistudio.google.com/).
2. **Mulai Percakapan:**
   - Ketik pertanyaan seputar kode mikrokontroler (Arduino / ESP32), rangkaian pin sensor, atau masalah error kompilasi.
3. **Eksplorasi Fitur:**
   - **Ganti Tema**: Gunakan menu dropdown di kanan atas untuk beralih antara Dark, Light, atau System mode.
   - **Kelola Riwayat Percakapan**: Buat obrolan baru dengan menekan tombol `➕` di sidebar kiri.
   - **Sesuaikan Konfigurasi**: Klik tombol `⚙️ Setting` di sidebar untuk mengganti Model, Temperature, atau Gaya Bahasa.

---

## 👨‍💻 Author & Credits

- **Developer**: **Muhammad Faisal Abdurrahman**
- **Program**: Hacktiv8 Final Project - *LLM-Based Tools and Gemini API Integration for Data Scientists*
- **Tahun**: 2026

