# ⚡ IoT & Microcontroller Code Assistant

Final Project: **LLM-Based Tools and Gemini API Integration for Data Scientists**

Aplikasi Chatbot interaktif berbasis **Streamlit** dan **LangChain** dengan integrasi model **Google Gemini (gemini-2.5-flash)**. Dirancang khusus untuk membantu engineer, maker, dan data scientist dalam *troubleshooting* kode C++/MicroPython, merancang diagram *wiring* sensor/aktuator, serta mengkalibrasi mikrokontroler seperti **ESP32** dan **Arduino**.

---

## Fitur Utama

- **Model Mutakhir**: Menggunakan model `gemini-2.5-flash` dari Google AI via package `langchain-google-genai`.
- **Expert Persona System**: Dilengkapi `SystemMessage` terdedikasi sebagai *Expert IoT & Microcontroller Engineer* dengan pemahaman mendalam tentang pinout, arsitektur mikrokontroler, proteksi tegangan (3.3V vs 5V), serta filter sinyal sensor.
- **Dynamic Tone Selector**: Pilihan gaya bahasa interaktif:
  - `Professional/Technical`: Penjelasan teknis mendalam dan terminologi baku.
  - `Casual/Beginner-friendly`: Penjelasan ramah pemula dengan analogi mudah dipahami.
- **Customizable Temperature**: Slider pengatur temperatur untuk mengontrol tingkat deterministik dan kreativitas model.
- **Keamanan API Key**: Input API Key interaktif bertipe *password* di sidebar dengan validasi peringatan otomatis dan `st.stop()` jika belum diisi.
- **Stateful Chat Memory**: Riwayat percakapan tersimpan rapi menggunakan `st.session_state` dan `st.chat_message` dengan tombol **Clear Chat History** untuk reset cepat.

---

## 🛠️ Prasyarat & Instalasi

Pastikan Anda telah menginstal **Python 3.9+** di sistem Anda.

1. **Clone repositori (atau siapkan direktori proyek):**
   ```bash
   git clone <URL_REPOSITORY_GITHUB_ANDA>
   cd ai-chatbots-langchain
   ```

2. **Buat dan aktifkan Virtual Environment (Disarankan):**
   - **Windows:**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependensi yang diperlukan:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Cara Menjalankan Aplikasi

Jalankan perintah berikut pada terminal di direktori proyek:

```bash
streamlit run app.py
```

Setelah aplikasi berjalan di browser:
1. Buka sidebar di sebelah kiri.
2. Masukkan **Google Gemini API Key** Anda (Dapatkan secara gratis di [Google AI Studio](https://aistudio.google.com/)).
3. Atur nilai **Temperature** dan pilih **Gaya Bahasa** sesuai kebutuhan.
4. Mulai ajukan pertanyaan terkait kode, error compiler, skema wiring, atau kalibrasi sensor pada kolom chat.

---

## 📸 Tampilan Antarmuka (Screenshot UI)

<!-- Tempelkan screenshot tampilan aplikasi Anda di sini -->
![Screenshot UI](https://via.placeholder.com/900x500?text=Placeholder+Screenshot+Aplikasi+Streamlit+IoT+Assistant)

---

## 🔗 Tautan Repositori GitHub

- **Repository URL**: `https://github.com/<USERNAME>/<REPO_NAME>`

---

## 👨‍💻 Author & Credits

- **Developer**: Muhammad Faisal Abdurrahman
- **Program**: Hacktiv8 Final Project - LLM-Based Tools & Gemini API Integration
