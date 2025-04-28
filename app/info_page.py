import streamlit as st # type: ignore

def main():
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #000000, #000000, #3533cd); 
        }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("<h1 style='color: white; text-align: left;'>ℹ️ About <span style='color:#6C63FF;'>Imagino</span> & Help Center</h1>", unsafe_allow_html=True)

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

        ##### **Q. Do I need to log in?**  
        Yes, logging in is required to personalize your experience. It allows us to save your work, enable chat support, and offer tailored features such as saving your image history and preferences.

        ##### **Q. Can I download images?**  
        Absolutely! Once your image is generated, you'll find a download button that allows you to easily save your artwork. We ensure you have complete ownership of the creations you generate.

        ##### **Q. Can I give feedback and regenerate images?**  
        Definitely! After generating an image, you can provide feedback using our chat-style interface. Our AI will use your input to instantly regenerate and refine the image, helping you perfect your vision.

        ##### **Q. Can I talk to a human expert?**  
        Yes, you can! If you need expert guidance or have specific questions, click on the “Consult an Expert” button in the image thread. This will connect you with a professional via Tawk.to for real-time assistance.

        ##### **Q. Where are my images stored?**  
        Your generated images are temporarily stored within the platform. After generation, you can download them immediately. 

        ---

        ### 📬 Still have questions?
        Feel free to consult our expert from the image interface or reach out via [Linkedin](https://www.linkedin.com/in/somya-bhushan/)
        """)
