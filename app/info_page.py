import streamlit as st # type: ignore

def main():
    # st.set_page_config(page_title="About & Help - Imagino", layout="wide")
    st.title("ℹ️ About Imagino & Help Center")

    st.markdown("""
    Welcome to **Imagino** – your all-in-one AI-powered image generation platform!

    ---  
    ### 📌 What is Imagino?
    Imagino allows users to generate stunning visuals using cutting-edge AI, refine them through feedback, and even consult experts for perfection.

    - 🚀 Powered by `Stable Diffusion XL`
    - 🧠 Real-time feedback and image enhancement
    - 💬 Live chat support with experts
    - 💾 Download and save generated art

    ---

    ### ❓ Frequently Asked Questions

    **Q. Do I need to log in?**  
    Yes. Logging in lets us save your work, enable chat, and offer personalized features.

    **Q. Can I download images?**  
    Yes! Every generated image includes a download button.

    **Q. Can I give feedback and regenerate images?**  
    Absolutely. Use the chat-style interface to request changes and get new versions instantly.

    **Q. Can I talk to a human expert?**  
    Yes. Click “Consult an expert” on the image thread to chat via Tawk.to.

    **Q. Where are my images stored?**  
    Images are temporarily stored and available for download after generation.

    ---

    ### 📬 Still have questions?
    Feel free to consult our expert from the image interface or reach out via [Linkedin](https://www.linkedin.com/in/somya-bhushan/)
    """)
