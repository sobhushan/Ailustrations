# app/main_app.py
import base64
import streamlit as st # type: ignore
import requests
from PIL import Image # type: ignore
from io import BytesIO
import os
from dotenv import load_dotenv
from auth.firebase_utils import save_history, load_history
from firebase_admin import firestore # type: ignore
import streamlit.components.v1 as components # type: ignore

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
TAWK_PROPERTY_ID = os.getenv("TAWK_PROPERTY_ID")
TAWK_WIDGET_ID = os.getenv("TAWK_WIDGET_ID")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Function to scroll to top using JS
def scroll_to_top():
    st.experimental_js("window.scrollTo({ top: 0, behavior: 'smooth' });")

def generate_image_from_prompt(prompt: str):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt}, timeout=30)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return img_bytes.getvalue(), None

    except requests.exceptions.HTTPError as http_err:
        return None, f"HTTP error: {http_err} — {response.text}"
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except requests.exceptions.RequestException as err:
        return None, f"Something went wrong: {err}"
    except Exception as e:
        return None, f"Unexpected error: {e}"
    
if "scroll_to" in st.session_state:
    section = st.session_state.scroll_to
    st.components.v1.html(f"""
        <div style="position: absolute; top: 0; height: 0;">
        <script>
        window.addEventListener('DOMContentLoaded', function() {{
            const el = window.parent.document.getElementById("{section}");
            if (el) {{
                el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }});
        </script>
        </div>
    """, height=0)
    del st.session_state.scroll_to

def main_app():
    st.components.v1.html("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    """, height=0)
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #000000, #000000, #3533cd); 
        }
        section[data-testid="stSidebar"] {
            background-color: #31333f !important;
        }
        .stDownloadButton button {
            background: linear-gradient(135deg, #000000,  #3533cd) !important; 
            border: 1px solid #3533cd !important;
            color: white !important; 
        }
        .stDownloadButton button:hover {
            opacity: 0.8 !important;
            border: 1px solid #1a1c24 !important;
            color: white !important; 
        }
        h2, h3 {
            color: white !important;
        }
        p {
            color: white;
        }
        div.stButton > button:first-child {
            width: 100%;
            height: 50px;
            font-size: 18px;
            background: linear-gradient(135deg, #6C63FF 0%, #9C88FF 100%);
            color: white;
            border: none;
            border-radius: 8px;
            transition: background 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(135deg, #4B36F7 0%, #6C63FF 100%);
        }
        
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("<h1 style='text-align: left;'><span style='color:#6C63FF;'>Ailustrations</span></h1>", unsafe_allow_html=True)

        if "history" not in st.session_state:
            if "user" in st.session_state and "email" in st.session_state["user"]:
                st.session_state.history = load_history(st.session_state["user"]["email"])
            else:
                st.session_state.history = []
        if "image_generated" not in st.session_state:
            st.session_state.image_generated = False


        # Sidebar button
        st.sidebar.markdown("---")
        if "show_confirm" not in st.session_state:
            st.session_state.show_confirm = False

        if st.sidebar.button("Start New Session"):
            st.session_state.show_confirm = True
            st.session_state.scroll_to = "top"
            st.rerun()


        # Delete Firebase data
        def delete_user_history_from_firebase(email):
            db = firestore.client()
            doc_ref = db.collection("history").document(email)
            if doc_ref.get().exists:
                doc_ref.delete()

        def cancel_reset():
            st.session_state.show_confirm = False

        def proceed_reset():
            if "user" in st.session_state and "email" in st.session_state["user"]:
                delete_user_history_from_firebase(st.session_state["user"]["email"])
            st.session_state.history = []
            st.session_state.image_generated = False
            st.session_state.show_confirm = False
            st.success("✅ New session started. History deleted.")
            st.rerun()

        # Prompt Builder 
        if "prompt_builder_visible" not in st.session_state:
            st.session_state.prompt_builder_visible = False
        if st.session_state.prompt_builder_visible:
            st.sidebar.markdown("---")
            st.sidebar.title("🛠 Prompt Builder")
            use_builder = st.sidebar.toggle("Enable Builder", value=False, key="toggle_builder")

            style, mood, use_case = "", "", ""
            if use_builder:
                style = st.sidebar.selectbox("Style", ["Realistic", "Cartoon", "Digital Art", "Oil Painting", "Abstract"])
                mood = st.sidebar.selectbox("Mood", ["Vibrant","Melancholic","Happy", "Dark", "Surreal", "Peaceful"])
                use_case = st.sidebar.selectbox("Use Case", ["Poster", "Marketing Banner", "Product Mockup", "Team Avatar", "Wallpaper"])
        else:
            # Prompt builder is disabled after first image
            style = mood = use_case = ""

        st.markdown("<h5 style='text-align: left; color:white;'>Write your prompt and generate your image just the way you want!</h5>", unsafe_allow_html=True)
        user_prompt = st.text_input("Enter your prompt", placeholder="e.g. a futuristic cyberpunk city at night")
        st.markdown('<div id="top"></div>', unsafe_allow_html=True)
        if st.button("✨ Generate Image"):
            # final_prompt = f"{style}, {mood}, {use_case}. {user_prompt}" if user_prompt else f"{style}, {mood}, {use_case}"
            parts = [p for p in [style, mood, use_case, user_prompt] if p]
            final_prompt = ". ".join(parts)

            with st.spinner("Generating image..."):
                image_bytes, error = generate_image_from_prompt(final_prompt)

            if error:
                st.error(error)
            elif image_bytes:
                st.session_state.image_generated = True
                st.session_state.history.append({
                    "prompt": final_prompt,
                    "image_bytes": image_bytes,
                    "feedback": ""
                })

                if "user" in st.session_state and "email" in st.session_state["user"]:
                    save_history(st.session_state["user"]["email"], st.session_state.history)
                st.session_state.prompt_builder_visible = False


        # Confirmation dialog in main content
        if st.session_state.show_confirm:
            with st.container():
                st.markdown("---")
                st.markdown("""
                    <style>
                    .confirm-box {
                        background-color: rgba(255, 75, 75, 0.1);
                        border: 2px solid rgba(255, 75, 75);
                        padding: 30px;
                        border-radius: 15px;
                        box-shadow: 0px 0px 25px 5px rgba(255, 75, 75, 0.5);
                        text-align: center;
                        margin-top: 30px;
                        margin-bottom: 10px;
                    }
                    .confirm-title {
                        font-size: 24px;
                        color: #ffffff;
                        margin-bottom: 20px;
                    }
                    .confirm-text {
                        font-size: 16px;
                        color: #cccccc;
                        margin-bottom: 10px;
                    }
                    </style>
                    <div class="confirm-box">
                        <div class="confirm-title">⚠️ Confirm New Session</div>
                        <div class="confirm-text">Are you sure you want to start a new session?<br>This will delete all your saved prompts and images permanently.</div>
                    </div>
                """, unsafe_allow_html=True)

                # Better two-button layout
                confirm_col1, confirm_col2, confirm_col3 = st.columns([1, 1, 1])

                with confirm_col1:
                    if st.button("✅ Yes, Start New", key="confirm_yes"):
                        proceed_reset()

                with confirm_col3:
                    if st.button("❎ Cancel", key="confirm_no"):
                        cancel_reset()

        if st.session_state.history:
            st.markdown("---")
            st.subheader("Your Generated Images")
            for idx, entry in enumerate(st.session_state.history):
                st.markdown(f"**Prompt:** {entry['prompt']}")
                st.image(entry["image_bytes"], use_container_width=True)
                st.download_button("Download Image", entry["image_bytes"], f"ai_image_{idx+1}.png", "image/png", key=f"download-{idx}")
                feedback = st.text_input("Want changes?", placeholder="Add something to improve or refine the image...", key=f"feedback-{idx}")
                if feedback and not entry["feedback"]:  
                    updated_prompt = entry["prompt"] + ". " + feedback

                    with st.spinner("Regenerating..."):
                        image_bytes, error = generate_image_from_prompt(updated_prompt)

                    if error:
                        st.error(error)
                    elif image_bytes:
                        st.session_state.history.append({
                            "prompt": updated_prompt,
                            "image_bytes": image_bytes,
                            "feedback": []
                        })

                        if "user" in st.session_state and "email" in st.session_state["user"]:
                            save_history(st.session_state["user"]["email"], st.session_state.history)

                        entry["feedback"] = "processed"
                        st.rerun()

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
        st.markdown("---")
        if st.session_state.image_generated:
            st.markdown("## 💬 Not satisfied? Consult our Experts")
            expert_toggle = st.toggle("Toggle to send your image and prompt to our expert.", key="expert_toggle")
            if expert_toggle and TAWK_PROPERTY_ID and TAWK_WIDGET_ID:
                st.components.v1.html(f"""
                <script type="text/javascript">
                    var Tawk_API = Tawk_API || {{}}, Tawk_LoadStart = new Date();

                    // Auto-clear previous chat on load
                    Tawk_API.onLoad = function() {{
                        console.log("🔁 Resetting previous chat session.");
                        Tawk_API.endChat();
                        
                        // Optional: Send welcome message
                        setTimeout(function() {{
                            Tawk_API.addEvent("WelcomeMessage", {{
                                description: "👋 Let us help you perfect your image!"
                            }});
                        }}, 1000);
                    }};

                    (function() {{
                        var s1 = document.createElement("script"),
                            s0 = document.getElementsByTagName("script")[0];
                        s1.async = true;
                        s1.src = 'https://embed.tawk.to/{TAWK_PROPERTY_ID}/{TAWK_WIDGET_ID}';
                        s1.charset = 'UTF-8';
                        s1.setAttribute('crossorigin','*');
                        s0.parentNode.insertBefore(s1, s0);
                    }})();

                    // Send prompt & image to support via event
                    function waitForTawk() {{
                        if (typeof Tawk_API.addEvent === "function") {{
                            const prompt = localStorage.getItem("latestPrompt") || "No prompt provided";
                            const image = localStorage.getItem("latestImage") || "";

                            if (!image) {{
                                console.warn("⚠️ No image found in localStorage.");
                                return;
                            }}

                            const confirmed = confirm("⚠️ We will send your prompt and image to our expert. Are you sure you want to continue?");
                            if (!confirmed) {{
                                console.log("❌ User cancelled expert request.");
                                return;
                            }}

                            const preview = image.length > 100 ? image.slice(0, 100) + "..." : image;

                            const message = "🧠 Image Help Request\\n" +
                                            "Prompt: " + prompt + "\\n" +
                                            "Image (Base64 Preview): " + preview;

                            Tawk_API.addEvent("ImageGenerated", {{
                                description: message
                            }}, function(error) {{
                                if (error) {{
                                    console.error("❌ Failed to send chat message:", error);
                                }} else {{
                                    console.log("✅ Chat message sent with prompt and image preview.");
                                }}
                            }});
                        }} else {{
                            console.log("⏳ Waiting for Tawk API...");
                            setTimeout(waitForTawk, 1000);
                        }}
                    }}

                    // Trigger message on page load (after Tawk is ready)
                    window.addEventListener("load", function() {{
                        setTimeout(waitForTawk, 2000);
                    }});
                </script>
                """, height=500)