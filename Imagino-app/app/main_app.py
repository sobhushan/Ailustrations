# app/main_app.py
import base64
import streamlit as st # type: ignore
import requests
from PIL import Image # type: ignore
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
TAWK_PROPERTY_ID = os.getenv("TAWK_PROPERTY_ID")
TAWK_WIDGET_ID = os.getenv("TAWK_WIDGET_ID")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def main_app():
    # st.set_page_config(page_title="Imagino", layout="centered")
    st.markdown("<h1 style='text-align: left;'><span style='color:#6C63FF;'>Imagino ✨</span></h1>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    # Prompt Builder with Toggle Switch
    st.sidebar.title("🛠 Prompt Builder")
    use_builder = st.sidebar.toggle("Enable Builder", value=False, key="toggle_builder")

    # Only show builder options if the switch is ON
    style, mood, use_case = "", "", ""
    if use_builder:
        style = st.sidebar.selectbox("Style", ["Realistic", "Cartoon", "Digital Art", "Abstract"])
        mood = st.sidebar.selectbox("Mood", ["Happy", "Dark", "Surreal", "Peaceful"])
        use_case = st.sidebar.selectbox("Use Case", ["Marketing Banner", "Product Mockup", "Team Avatar", "Wallpaper"])


    # st.subheader("Write your own prompt or use the builder from the sidebar.")
    st.markdown("<h5 style='text-align: left; color:gray;'>Write your own prompt or use the builder from the sidebar and generate your image just the way you want!</h5>", unsafe_allow_html=True)
    user_prompt = st.text_input("Enter your prompt", placeholder="e.g. a futuristic cyberpunk city at night")

    if st.button("✨ Generate Image"):
        # final_prompt = f"{style}, {mood}, {use_case}. {user_prompt}" if user_prompt else f"{style}, {mood}, {use_case}"
        parts = [p for p in [style, mood, use_case, user_prompt] if p]
        final_prompt = ". ".join(parts)

        with st.spinner("Generating image..."):
            response = requests.post(API_URL, headers=HEADERS, json={"inputs": final_prompt})
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                img_bytes = BytesIO()
                image.save(img_bytes, format="PNG")
                img_bytes.seek(0)
                st.session_state.history.append({
                    "prompt": final_prompt,
                    "image_bytes": img_bytes.getvalue(),
                    "feedback": ""
                })
            else:
                st.error(f"Error {response.status_code}: {response.text}")

    if st.session_state.history:
        st.markdown("---")
        st.subheader("🖼️ Your Generated Images")
        for idx, entry in enumerate(st.session_state.history):
            st.markdown(f"**Prompt:** {entry['prompt']}")
            st.image(entry["image_bytes"], use_container_width=True)
            st.download_button("📥 Download", entry["image_bytes"], f"ai_image_{idx+1}.png", "image/png", key=f"download-{idx}")
            feedback = st.text_input("Want changes?", "", key=f"feedback-{idx}")
            if feedback and not entry["feedback"]:  
                updated_prompt = entry["prompt"] + ". " + feedback
                with st.spinner("Regenerating..."):
                    response = requests.post(API_URL, headers=HEADERS, json={"inputs": updated_prompt})
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        img_bytes = BytesIO()
                        image.save(img_bytes, format="PNG")
                        img_bytes.seek(0)
                        st.session_state.history.append({
                            "prompt": updated_prompt,
                            "image_bytes": img_bytes.getvalue(),
                            "feedback": feedback
                        })
                        entry["feedback"] = "processed"  
                        st.rerun()
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")

            st.markdown("---")

            # Save to localStorage
            b64_image = base64.b64encode(entry["image_bytes"]).decode("utf-8")
            data_url = f"data:image/png;base64,{b64_image}"
            st.components.v1.html(f"""
                <script>
                    localStorage.setItem("latestPrompt", {entry['prompt']!r});

                    localStorage.setItem("latestImage", {b64_image!r});
                    console.log("Latest prompt and image stored.");
                </script>
            """, height=0)

    # ✅ Embed Tawk.to and send prompt/image as a chat message
    if TAWK_PROPERTY_ID and TAWK_WIDGET_ID:
        st.markdown("### 💬 Need Help? Chat with Support Below")
        st.components.v1.html(f"""
        <script type="text/javascript">
            var Tawk_API = Tawk_API || {{}}, Tawk_LoadStart = new Date();

            (function() {{
                var s1 = document.createElement("script"),
                    s0 = document.getElementsByTagName("script")[0];
                s1.async = true;
                s1.src = 'https://embed.tawk.to/{TAWK_PROPERTY_ID}/{TAWK_WIDGET_ID}';
                s1.charset = 'UTF-8';
                s1.setAttribute('crossorigin','*');
                s0.parentNode.insertBefore(s1, s0);
            }})();

            function uploadToImgur(base64Image, callback) {{
                 let base64Clean = base64Image;
                if (base64Image.startsWith("data:image")) {{
                    base64Clean = base64Image.split(",")[1];
                }}
                
                fetch("https://api.imgur.com/3/image", {{
                    method: "POST",
                    headers: {{
                        "Authorization": "Client-ID 0d7fa91852c4df6",
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{ image: base64Clean }})
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success && data.data.link) {{
                        callback(null, data.data.link);
                    }} else {{
                        callback("❌ Failed to upload to Imgur", null);
                    }}
                }})
                .catch(err => {{
                    callback(err.message, null);
                }});
            }}

            function waitForTawk() {{
                if (typeof Tawk_API.addEvent === "function") {{
                    const prompt = localStorage.getItem("latestPrompt") || "No prompt";
                    const base64 = localStorage.getItem("latestImage") || "";
                    console.log("Prompt:", prompt);
                    console.log("Base64 Image:", base64);
                    if (!base64) {{
                        console.log("⚠️ No image to send.");
                        return;
                    }}

                    uploadToImgur(base64, function(err, imgUrl) {{
                        if (err) {{
                            console.error(err);
                            return;
                        }}

                        const message = "🖼️ New image generated<br>" +
                                        "📝 <b>Prompt:</b> " + prompt + "<br>" +
                                        "📷 <b>Image:</b><br><img src='" + imgUrl + "' width='250'/>";

                        Tawk_API.addEvent("ImageGenerated", {{
                            description: message
                        }}, function(error) {{
                            if (error) {{
                                console.error("❌ Message Error:", error);
                            }} else {{
                                console.log("✅ Chat message sent with Imgur image");
                            }}
                        }});
                    }});
                }} else {{
                    console.log("⏳ Waiting for Tawk API...");
                    setTimeout(waitForTawk, 1000);
                }}
            }}

            window.addEventListener("load", function() {{
                setTimeout(waitForTawk, 2000);
            }});
        </script>
        """, height=500)


