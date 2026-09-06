# pyrefly: ignore [missing-import]
import uuid
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="IoT & Microcontroller Code Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
defaults = {
    "theme": "dark",  # "dark", "light", "system"
    "api_key": "",
    "api_key_confirmed": False,
    "selected_model": "gemini-3.6-flash",
    "temperature": 0.3,
    "tone_style": "Professional/Technical",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Multi-conversation session management
if "sessions" not in st.session_state:
    init_id = str(uuid.uuid4())[:8]
    old_messages = st.session_state.get("messages", [])
    first_title = "Percakapan Baru"
    if old_messages:
        for m in old_messages:
            if isinstance(m, HumanMessage):
                clean = m.content.strip().replace("\n", " ")
                first_title = clean[:24] + ("…" if len(clean) > 24 else "")
                break
    st.session_state.sessions = {
        init_id: {
            "title": first_title,
            "messages": old_messages,
        }
    }
    st.session_state.current_session_id = init_id

if "current_session_id" not in st.session_state or st.session_state.current_session_id not in st.session_state.sessions:
    st.session_state.current_session_id = list(st.session_state.sessions.keys())[0]

current_session = st.session_state.sessions[st.session_state.current_session_id]
st.session_state.messages = current_session["messages"]

# ─────────────────────────────────────────────
#  THEME DEFINITIONS & CSS INJECTION
# ─────────────────────────────────────────────
DARK = {
    "--bg":          "#0e1117",
    "--bg2":         "#161b22",
    "--bg3":         "#21262d",
    "--surface":     "#1c212c",
    "--border":      "#30363d",
    "--text":        "#f0f6fc",
    "--text2":       "#8b949e",
    "--accent":      "#58a6ff",
    "--accent2":     "#388bfd",
    "--user-msg":    "#161f2e",
    "--ai-msg":      "#12161f",
    "--danger":      "#f85149",
}

LIGHT = {
    "--bg":          "#ffffff",
    "--bg2":         "#f6f8fa",
    "--bg3":         "#eaeef2",
    "--surface":     "#ffffff",
    "--border":      "#d0d7de",
    "--text":        "#1f2328",
    "--text2":       "#656d76",
    "--accent":      "#0969da",
    "--accent2":     "#0550ae",
    "--user-msg":    "#f0f4f9",
    "--ai-msg":      "#ffffff",
    "--danger":      "#cf222e",
}

selected_theme = st.session_state.theme

if selected_theme == "dark":
    vars_css = "\n".join(f"    {k}: {v};" for k, v in DARK.items())
    theme_root = f":root {{\n{vars_css}\n}}"
elif selected_theme == "light":
    vars_css = "\n".join(f"    {k}: {v};" for k, v in LIGHT.items())
    theme_root = f":root {{\n{vars_css}\n}}"
else:  # system
    light_vars = "\n".join(f"    {k}: {v};" for k, v in LIGHT.items())
    dark_vars = "\n".join(f"    {k}: {v};" for k, v in DARK.items())
    theme_root = f"""
:root {{
{light_vars}
}}
@media (prefers-color-scheme: dark) {{
    :root {{
{dark_vars}
    }}
}}
"""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

{theme_root}

/* Base application styling */
html, body, .stApp {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}}

/* Header Chrome: keep expand button visible, hide redundant toolbars */
header[data-testid="stHeader"] {{
    background: transparent !important;
    z-index: 99 !important;
}}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

/* Sidebar Container & Responsiveness */
section[data-testid="stSidebar"] {{
    background-color: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    background-color: var(--bg2) !important;
}}
section[data-testid="stSidebar"][aria-expanded="false"] {{
    min-width: 0 !important;
    width: 0 !important;
}}
section[data-testid="stSidebar"][aria-expanded="true"] {{
    min-width: 280px !important;
}}

/* Collapse and Expand sidebar buttons */
[data-testid="stSidebarCollapseButton"],
[data-testid="stExpandSidebarButton"] {{
    visibility: visible !important;
    display: inline-flex !important;
}}
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"] button {{
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    padding: 4px 8px !important;
    cursor: pointer !important;
}}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stExpandSidebarButton"] svg {{
    fill: var(--text) !important;
    color: var(--text) !important;
}}

/* Main Block Layout - Centered & prevents cut-off */
.stMainBlockContainer, [data-testid="stMainBlockContainer"], .block-container {{
    background: var(--bg) !important;
    padding-top: 1.2rem !important;
    padding-bottom: 3.5rem !important;
    max-width: 950px !important;
    margin: 0 auto !important;
}}

/* Sidebar chat history list items */
section[data-testid="stSidebar"] div.stButton > button {{
    text-align: left !important;
    justify-content: flex-start !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    padding: 7px 11px !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    width: 100% !important;
    margin: 1px 0 !important;
    transition: all 0.15s ease !important;
}}

/* Active session pill */
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {{
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.12) !important;
}}

/* Inactive session pills */
section[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {{
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--text2) !important;
    font-weight: 400 !important;
}}
section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {{
    background: var(--bg3) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}}

/* Sidebar delete button */
[data-testid="stSidebar"] .del-btn-col div.stButton > button {{
    background: transparent !important;
    border: none !important;
    color: var(--text2) !important;
    padding: 6px 4px !important;
    font-size: 0.85rem !important;
    justify-content: center !important;
    text-align: center !important;
}}
[data-testid="stSidebar"] .del-btn-col div.stButton > button:hover {{
    color: var(--danger) !important;
    background: transparent !important;
}}

/* Chat Messages */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    padding: 0.5rem 0 !important;
}}
[data-testid="stChatMessageContent"] {{
    background: var(--ai-msg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    color: var(--text) !important;
    overflow-wrap: break-word !important;
    word-break: break-word !important;
    line-height: 1.6 !important;
}}
[data-testid="stChatMessage"]:has([data-testid="stAvatarUser"]) [data-testid="stChatMessageContent"] {{
    background: var(--user-msg) !important;
}}

/* Chat Input Bar */
[data-testid="stChatInput"] {{
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
}}
[data-testid="stChatInput"] textarea {{
    color: var(--text) !important;
    background: transparent !important;
}}

/* Code blocks */
code, pre {{
    font-family: 'JetBrains Mono', monospace !important;
    background: var(--bg3) !important;
    color: var(--text) !important;
    border-radius: 6px;
}}

/* Dividers */
hr {{
    border-color: var(--border) !important;
    margin: 0.8rem 0 !important;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DIALOG: SETTINGS POPUP
# ─────────────────────────────────────────────
@st.dialog("⚙️ Pengaturan Model & Konfigurasi", width="small")
def dialog_settings():
    st.markdown("**🤖 Konfigurasi Model AI**")

    model_options = ["gemini-3.6-flash", "gemini-2.0-flash", "Custom"]
    curr_model = st.session_state.selected_model
    curr_idx = model_options.index(curr_model) if curr_model in model_options else len(model_options) - 1

    model_choice = st.selectbox(
        "Pilih Model Gemini",
        options=model_options,
        index=curr_idx,
        help="Rekomendasi model aktif: gemini-3.6-flash",
    )
    if model_choice == "Custom":
        actual_model = st.text_input("ID Model Kustom", value=curr_model)
    else:
        actual_model = model_choice

    temp_val = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.temperature),
        step=0.05,
        help="0.0 - 0.3: Presisi tinggi untuk kode & wiring | 0.7+: Lebih eksploratif",
    )

    tone_val = st.selectbox(
        "Gaya Bahasa",
        options=["Professional/Technical", "Casual/Beginner-friendly"],
        index=0 if st.session_state.tone_style == "Professional/Technical" else 1,
    )

    st.divider()
    st.markdown("**🔑 Google Gemini API Key**")
    current_key = st.session_state.api_key
    masked_key = ("•" * 16 + current_key[-4:]) if len(current_key) > 4 else "Belum dikonfigurasi"
    st.caption(f"Key aktif saat ini: `{masked_key}`")

    new_key = st.text_input(
        "Ganti API Key baru (opsional)",
        type="password",
        placeholder="Kosongkan jika tidak ingin mengubah...",
    )

    st.divider()
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 Simpan", use_container_width=True, type="primary"):
            st.session_state.selected_model = actual_model
            st.session_state.temperature = temp_val
            st.session_state.tone_style = tone_val
            if new_key.strip():
                st.session_state.api_key = new_key.strip()
                st.session_state.api_key_confirmed = True
            st.rerun()
    with col_cancel:
        if st.button("Batal", use_container_width=True):
            st.rerun()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # 1. Branding
    st.markdown("""
    <div style="padding: 0.1rem 0 0.4rem 0;">
        <div style="font-size:1.15rem; font-weight:700; display:flex; align-items:center; gap:8px;">
            <span>⚡</span> <span>IoT Assistant</span>
        </div>
        <div style="font-size:0.75rem; color:var(--text2); margin-top:2px;">
            Firmware · Wiring · Kalibrasi Sensor
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # 2. Header row matching user reference: "Chats and tasks ⌵" + action buttons
    col_lbl, col_act_new, col_act_set = st.columns([3.8, 1.1, 1.1], vertical_alignment="center")
    with col_lbl:
        st.markdown("""
        <div style="font-size:0.8rem; font-weight:600; color:var(--text2); display:flex; align-items:center; gap:4px; padding-left:2px;">
            <span>Chats and tasks</span> <span style="font-size:0.65rem;">⌵</span>
        </div>
        """, unsafe_allow_html=True)
    with col_act_new:
        if st.button("➕", key="btn_new_chat", help="Percakapan baru"):
            new_id = str(uuid.uuid4())[:8]
            st.session_state.sessions[new_id] = {
                "title": "Percakapan Baru",
                "messages": [],
            }
            st.session_state.current_session_id = new_id
            st.rerun()
    with col_act_set:
        if st.button("⚙️", key="btn_open_settings_icon", help="Buka Pengaturan Model"):
            dialog_settings()

    # Session list items
    session_items = list(st.session_state.sessions.items())
    for s_id, s_data in reversed(session_items):
        is_active = (s_id == st.session_state.current_session_id)
        title = s_data.get("title", "Percakapan Baru")
        label = f"○  {title}"

        if is_active:
            col_s_btn, col_s_del = st.columns([5.3, 1.1], vertical_alignment="center")
            with col_s_btn:
                st.button(label, key=f"btn_sess_{s_id}", type="primary", use_container_width=True)
            with col_s_del:
                st.markdown('<div class="del-btn-col">', unsafe_allow_html=True)
                if st.button("✕", key=f"del_sess_{s_id}", help="Hapus sesi ini"):
                    del st.session_state.sessions[s_id]
                    if not st.session_state.sessions:
                        new_id = str(uuid.uuid4())[:8]
                        st.session_state.sessions[new_id] = {"title": "Percakapan Baru", "messages": []}
                        st.session_state.current_session_id = new_id
                    else:
                        st.session_state.current_session_id = list(st.session_state.sessions.keys())[-1]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            if st.button(label, key=f"btn_sess_{s_id}", type="secondary", use_container_width=True):
                st.session_state.current_session_id = s_id
                st.rerun()

    # 3. Bottom actions
    st.divider()
    col_b_set, col_b_clr = st.columns(2)
    with col_b_set:
        if st.button("⚙️ Setting", key="btn_setting_bottom", use_container_width=True):
            dialog_settings()
    with col_b_clr:
        if st.button("🗑️ Clear", key="btn_clear_bottom", use_container_width=True, help="Bersihkan chat sesi aktif"):
            curr_sess = st.session_state.sessions[st.session_state.current_session_id]
            curr_sess["messages"] = []
            curr_sess["title"] = "Percakapan Baru"
            st.session_state.messages = []
            st.rerun()

    # Status summary badge
    st.markdown(f"""
    <div style="
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 7px 10px;
        font-size: 0.72rem;
        color: var(--text2);
        margin-top: 0.5rem;
        line-height: 1.4;
    ">
        <div>Model: <b style="color:var(--text);">{st.session_state.selected_model}</b></div>
        <div>Temp: <b style="color:var(--text);">{st.session_state.temperature}</b> · <span style="color:var(--text);">{ 'Pro' if st.session_state.tone_style.startswith('Pro') else 'Casual' }</span></div>
    </div>
    <div style="
        text-align: center;
        margin-top: 1.2rem;
        padding-top: 0.8rem;
        border-top: 1px dashed var(--border);
        font-size: 0.74rem;
        color: var(--text2);
        line-height: 1.5;
    ">
        Crafted with ⚡ by <b style="color:var(--text);">Muhammad Faisal Abdurrahman</b><br>
        <span style="font-size:0.68rem; opacity:0.85;">Hacktiv8 AI Final Project</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN TOP HEADER (Title & Theme Selector)
# ─────────────────────────────────────────────
col_head_title, col_head_theme = st.columns([3.8, 1.4], vertical_alignment="center")

with col_head_title:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px;">
        <div>
            <h2 style="margin:0; font-size:1.35rem; font-weight:700; letter-spacing:-0.02em;">
                IoT &amp; Microcontroller Code Assistant
            </h2>
            <p style="margin:3px 0 0 0; font-size:0.8rem; color:var(--text2);">
                Troubleshooting C++/MicroPython · Wiring Sensor · Kalibrasi ESP32 &amp; Arduino
            </p>
            <div style="margin-top:4px; font-size:0.72rem; color:var(--accent); font-weight:500;">
                ✦ Created by Muhammad Faisal Abdurrahman · Final Project Hacktiv8
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_head_theme:
    theme_labels = {"dark": "🌙 Dark", "light": "☀️ Light", "system": "💻 System"}
    theme_keys = ["dark", "light", "system"]
    curr_theme_idx = theme_keys.index(st.session_state.theme) if st.session_state.theme in theme_keys else 0

    chosen_theme_label = st.selectbox(
        "Pilih Tema Tampilan",
        options=[theme_labels[k] for k in theme_keys],
        index=curr_theme_idx,
        label_visibility="collapsed",
    )
    # Map back to key
    inv_map = {v: k for k, v in theme_labels.items()}
    new_theme = inv_map[chosen_theme_label]
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

st.divider()

# ─────────────────────────────────────────────
#  INITIAL SETUP CARD (JIKA API KEY BELUM DIISI)
# ─────────────────────────────────────────────
if not st.session_state.api_key_confirmed or not st.session_state.api_key:
    col_pad1, col_center, col_pad2 = st.columns([1, 2.2, 1])
    with col_center:
        st.markdown("""
        <div style="
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2.2rem 2rem 1.8rem 2rem;
            text-align: center;
            box-shadow: 0 8px 30px rgba(0,0,0,0.18);
            margin-top: 1rem;
        ">
            <h3 style="margin:0 0 0.4rem 0; font-size:1.3rem;">Mulai Sesi Chatbot IoT</h3>
            <p style="font-size:0.85rem; color:var(--text2); margin-bottom:1.5rem; line-height:1.5;">
                Silakan masukkan Google Gemini API Key Anda untuk mulai berkonsultasi seputar kode mikrokontroler, rangkaian sensor, dan troubleshooting error.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        key_input = st.text_input(
            "Google Gemini API Key",
            type="password",
            placeholder="Tempel API Key di sini",
            label_visibility="collapsed",
        )
        st.caption("🔑 Belum punya API Key? Dapatkan gratis di [Google AI Studio ↗](https://aistudio.google.com/)")

        if st.button("Mulai Sesi Chat ", use_container_width=True, type="primary"):
            if key_input.strip():
                st.session_state.api_key = key_input.strip()
                st.session_state.api_key_confirmed = True
                st.rerun()
            else:
                st.error("⚠️ Silakan tempel Google Gemini API Key terlebih dahulu!")

        st.markdown("""
        <div style="text-align:center; margin-top:1.2rem; font-size:0.74rem; color:var(--text2);">
            Developed with ⚡ by <b style="color:var(--text);">Muhammad Faisal Abdurrahman</b> · Hacktiv8 Final Project
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ─────────────────────────────────────────────
#  ACTIVE CHAT AREA
# ─────────────────────────────────────────────
active_session = st.session_state.sessions[st.session_state.current_session_id]
current_messages = active_session["messages"]

# System prompt instructions
tone_instruction = (
    "Gunakan gaya komunikasi profesional, teknis, presisi, dan terstruktur menggunakan terminologi sistem embedded & electrical engineering yang baku."
    if st.session_state.tone_style == "Professional/Technical"
    else "Gunakan gaya komunikasi santai, ramah, mudah dipahami oleh pemula (beginner-friendly), dengan analogi sederhana namun tetap tepat dan akurat secara konsep teknis."
)
system_instruction = (
    f"Anda adalah seorang 'Expert IoT & Microcontroller Engineer' yang bertindak sebagai konsultan interaktif sistem embedded.\n"
    f"Keahlian teknis Anda meliputi:\n"
    f"- Pemrograman mikrokontroler C/C++ (Arduino framework & ESP-IDF) dan MicroPython.\n"
    f"- Arsitektur mikrokontroler: ESP32 (ESP32-S2, S3, C3, WROOM), ESP8266, STM32, Arduino (Uno, Nano, Mega, dll).\n"
    f"- Konfigurasi pinout & bus komunikasi: GPIO, I2C (SDA/SCL), SPI (MOSI/MISO/SCK/CS), UART, ADC, DAC, PWM, dan interrupt (ISR).\n"
    f"- Troubleshooting error kompilasi, runtime crash (Guru Meditation Error, Watchdog Timer WDT Reset, brownout detector, memory leak).\n"
    f"- Desain rangkaian & skematik wiring sensor analog/digital, aktuator, relay, optocoupler, display (OLED SSD1306, LCD I2C, e-Paper), serta protokol IoT (MQTT, HTTP REST, ESP-NOW, BLE, LoRa).\n"
    f"- Teknik kalibrasi sensor, konversi ADC (attenuasi, resolusi, tegangan referensi), dan filtering sinyal.\n\n"
    f"Pedoman Respons & Interaktivitas:\n"
    f"1. PROAKTIF BERTANYA (Klarifikasi Informasi yang Kurang):\n"
    f"   - Jika pertanyaan pengguna masih umum atau ada detail krusial yang belum lengkap (seperti tipe board spesifik, model sensor/modul, level tegangan 3.3V vs 5V, protokol komunikasi I2C/SPI/UART, atau pesan error di Serial Monitor), WAJIB ajukan 1-3 pertanyaan klarifikasi yang terarah dan bernomor di bagian akhir jawaban Anda.\n"
    f"   - Jangan membuat asumsi berbahaya jika berisiko merusak komponen fisik (misal overvoltage pada pin GPIO ESP32).\n"
    f"   - Berikan panduan awal yang relevan, lalu tanyakan spesifikasi hardware yang sedang digunakan pengguna.\n"
    f"2. DIAGNOSA SISTEMATIS: Pisahkan antara diagnosa hardware (koneksi, power supply, sinyal) dan software (library, timing, kode loop).\n"
    f"3. KEAMANAN HARDWARE: Selalu ingatkan batas tegangan (ESP32 3.3V logic level, resistor pembagi tegangan, pull-up/down, transistor driver relay).\n"
    f"4. TABEL & KODE: Sertakan tabel wiring pin-ke-pin yang jelas serta kode bersih dengan komentar penjelas di baris kritis.\n"
    f"5. GAYA BAHASA: {tone_instruction}"
)

# Display existing messages for active conversation
for msg in current_messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User Chat Input
if user_prompt := st.chat_input("Tanyakan kode C++/MicroPython, wiring sensor, atau kalibrasi..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Append to current session
    current_messages.append(HumanMessage(content=user_prompt))

    # Auto name session if it was default
    if active_session["title"] == "Percakapan Baru":
        clean_title = user_prompt.strip().replace("\n", " ")
        active_session["title"] = clean_title[:24] + ("…" if len(clean_title) > 24 else "")

    chat_history = [SystemMessage(content=system_instruction)] + current_messages

    client = ChatGoogleGenerativeAI(
        model=st.session_state.selected_model,
        google_api_key=st.session_state.api_key,
        temperature=st.session_state.temperature,
        max_retries=2,
    )

    with st.chat_message("assistant"):
        try:
            def stream_response():
                for chunk in client.stream(chat_history):
                    if hasattr(chunk, "content"):
                        yield chunk.content
                    elif isinstance(chunk, str):
                        yield chunk

            ai_full_text = st.write_stream(stream_response())
            current_messages.append(AIMessage(content=ai_full_text))
            st.session_state.messages = current_messages
        except Exception as e:
            st.error(f"⚠️ Kendala memanggil model `{st.session_state.selected_model}`:\n\n{e}")
            st.info("💡 Anda dapat mengganti model via menu **⚙️ Setting** di sidebar atau pojok atas.")
