import os
import streamlit as st
from google import genai
from PIL import Image
from gtts import gTTS
import tempfile
import base64

st.set_page_config(page_title="GenAI Image Captioning", layout="centered")
st.title("🦛 Moodeng Captioning (Thai) 🖼️")

# —– LOAD OR INPUT YOUR API KEY —–
genai_key = None
# 1) Try Streamlit secrets
try:
    genai_key = st.secrets["AIzaSyBFLvVpnJaTRlRz-yiZGrafiRb11C-6Bfk"]
except Exception:
    pass
# 2) Fallback to env var
if not genai_key:
    genai_key = os.getenv("AIzaSyBFLvVpnJaTRlRz-yiZGrafiRb11C-6Bfk", "")
# 3) If still missing, ask user
if not genai_key:
    genai_key = st.text_input(
        "🔑 Enter your GENAI_API_KEY", 
        type="password", 
        placeholder="AIzaSy…"
    )
if not genai_key:
    st.error("❗ Please provide your GENAI_API_KEY via secrets.toml, env var, or the box above.")
    st.stop()

client = genai.Client(api_key=genai_key)

# —– IMAGE UPLOADER —–
uploaded = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])
if not uploaded:
    st.info("📂 Please upload an image to begin.")
    st.stop()

img = Image.open(uploaded)
st.image(img, use_column_width=True)

# —– CAPTION & TTS —–
if st.button("Generate Caption & Speech",use_container_width=True):
    with st.spinner("✨ Generating caption…"):
        try:
            # 1) Save to temp file so GenAI can upload it
            tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            img.save(tmp_img.name)
            gen_file = client.files.upload(file=tmp_img.name)

            # 2) Call GenAI model
            resp = client.models.generate_content(
                model="gemini-2.0-flash",  # or "gemini-1.5-flash"
                contents=[
                    gen_file,
                    "อธิบายภาพนี้สั้น ๆ ภาษาไทย แบบกำลังทำคลิป TikTok (ตอบเป็นประโยคสไตล์ MC ยาว ๆ ไม่ต้องใส่ # ไม่ต้องลากคำ เช่น ทุกคนนนน เอาให้ชัดเจนว่ารูปภาพนี้กำลังทำอะไร)"
                ],
            )
            caption = resp.text.strip()
            st.markdown(f"**💬 คำบรรยายภาพ:** {caption}")

            # 3) Generate TTS and load into memory
            with st.spinner("🔊 Generating speech…"):
                tts = gTTS(text=caption, lang="th")
                tmp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp_mp3.name)
                tmp_mp3.flush()

                # Read and encode for autoplay
                with open(tmp_mp3.name, "rb") as f:
                    audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = (
                    f'<audio autoplay controls onplay="this.playbackRate=2">'
                    f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
                    "</audio>"
                )
                st.markdown(audio_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❗️ เกิดข้อผิดพลาด: {e}")
            st.info("ลองเปลี่ยนเป็น `model='gemini-2.5-flash-exp'` หากเจอ RateLimitError")
