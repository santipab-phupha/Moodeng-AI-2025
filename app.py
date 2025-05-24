# moodeng_captioning.py
# -------------------------------------------------
# Streamlit + Gemini + gTTS (male-like English voice) demo
# -------------------------------------------------
# ⚠️ หมายเหตุ: การใส่ API Key ตรง ๆ ในไฟล์ไม่ปลอดภัย
#  - ควรย้ายไปใช้ secrets.toml หรือ ตัวแปร ENV สำหรับโปรดักชัน

import os
import streamlit as st
from google import genai
from PIL import Image
from gtts import gTTS
import tempfile, base64

st.set_page_config(page_title="GenAI Image Captioning", layout="centered")
st.title("🦛 Moodeng Captioning (Thai) 🖼️")

# ── 1. LOAD / FALLBACK GENAI KEY ───────────────────────────────────────────
DEFAULT_API_KEY = "AIzaSyBFLvVpnJaTRlRz-yiZGrafiRb11C-6Bfk"   # ← ใส่ค่าเริ่มต้นที่นี่

genai_key = (
    st.secrets.get("GENAI_API_KEY", "")         # ① secrets.toml → [general] GENAI_API_KEY="AIza…"
    or os.getenv("GENAI_API_KEY", "")           # ② ตัวแปร ENV  → export GENAI_API_KEY=AIza…
    or DEFAULT_API_KEY                          # ③ ค่านี้ถ้า ①-② ไม่พบ
)

client = genai.Client(api_key=genai_key)

# ── 2. IMAGE UPLOADER ──────────────────────────────────────────────────────
uploaded = st.file_uploader("📂 Upload an image", type=("jpg", "jpeg", "png"))
if not uploaded:
    st.info("โปรดอัปโหลดภาพก่อนเริ่มใช้งาน")
    st.stop()

img = Image.open(uploaded)
st.image(img, use_column_width=True)

# ── 3. CAPTION + TTS ───────────────────────────────────────────────────────
if st.button("✨ Generate Caption & English Voice 🎙️", use_container_width=True):
    with st.spinner("⚡ Generating caption…"):
        try:
            # 3-A. upload image to Gemini
            tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            img.save(tmp_img.name)
            gen_file = client.files.upload(file=tmp_img.name)

            # 3-B. ask Gemini for a TikTok-style English caption
            resp = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    gen_file,
                    (
                        "อธิบายภาพนี้สั้น ๆ ภาษาอังกฤษ "
                        "แบบกำลังทำคลิป TikTok "
                        "(ตอบเป็นประโยคสไตล์ MC ยาว ๆ ไม่ต้องใส่ # ไม่ต้องลากคำ "
                        "เช่น ทุกคนนนน เอาให้ชัดเจนว่ารูปภาพนี้กำลังทำอะไร)"
                    ),
                ],
            )
            caption = resp.text.strip()
            st.markdown(f"**💬 Caption:** {caption}")

            # 3-C. create English TTS (ลอง accent อินเดีย ซึ่งมักเป็นเสียงชาย)
            with st.spinner("🔊 Synthesising voice…"):
                tts = gTTS(text=caption, lang="en", tld="co.uk", slow=False)
                tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp_mp3.name)

                # embed audio & autoplay – playbackRate ≈ 1.25 ให้โทนฟัง-หนาขึ้น
                with open(tmp_mp3.name, "rb") as f:
                    audio_b64 = base64.b64encode(f.read()).decode()
                audio_html = f"""
                <audio autoplay controls onplay="this.playbackRate=1.25">
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
            st.info("ถ้าเจอ RateLimitError ลองเปลี่ยน model เป็น 'gemini-2.5-flash-exp' หรือรอสักครู่")
