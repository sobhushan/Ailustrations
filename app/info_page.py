import streamlit as st # type: ignore

def main():
    st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(180deg, #000000, #000000, #3533cd); 
        }
        section[data-testid="stSidebar"] {
            background-color: #31333f !important;
        }
        /* General body text */
        .stMarkdown, .stText, .st-bb, .st-c4, p, li, a {
            color: white !important;
        }

        /* Headings */
        h1, h2, h3, h5, h6 {
            color: white !important;
        }
        h4 {
            color: #FFD700 !important; /* Gold color for h4 headings */
        }

        /* Horizontal rule styling */
        hr {
            border: none;
            border-top: 1px solid white;
            margin: 20px 0;
        }
        /* FAQ links */
        a {
            color: #A6A6FF !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("---")
        st.markdown("### Table of Contents")
        st.markdown("""
        <p style="margin: 0"><a href="#what-is-ailustrations" style="text-decoration: none">What is Ailustrations?</a></p>
        <p style="margin: 0"><a href="#ai-powered-art-creation-fast-creative-and-adaptive" style="text-decoration: none">AI Features</a></p>
        <p style="margin: 0"><a href="#when-ai-falls-short-bridging-the-gap-with-human-expertise" style="text-decoration: none">Expert Consultation</a></p>
        <p style="margin: 0"><a href="#frequently-asked-questions" style="text-decoration: none">FAQ</a></p>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("<h1 style='color: white; text-align: left;'>ℹ️ About <span style='color:#6C63FF;'>Ailustrations</span> & Help Center</h1>", unsafe_allow_html=True)

        st.markdown("""
        Welcome to **Ailustrations** – your all-in-one AI-powered image generation platform!

        ---  
        ### What is Ailustrations?
        **Ailustrations** isn’t just a platform where you generate AI art and call it a day. It’s a space where **AI creativity** meets **human expertise**, empowering users to **create stunning visuals** while ensuring the final product is exactly what they envisioned. Here’s how we bridge the gap between **AI-generated art** and **human designers**:

        #### AI-Powered Art Creation: Fast, Creative, and Adaptive
        At the core of **Ailustrations** is a state-of-the-art AI model, powered by **Stable Diffusion XL**, that allows users to generate beautiful, high-quality visuals from simple prompts. Whether you’re an artist, marketer, designer, or someone looking to visualize your creative ideas, our AI tool helps you quickly create original artwork based on the styles, moods, and themes you want. The process is fast, creative, and intuitive, allowing you to explore endless visual possibilities without the need for advanced technical skills.

        **Key Features of AI in Ailustrations:**
        - **Instant Visuals**: Just enter a prompt, and our AI generates artwork in seconds.
        - **Customizable Styles**: You can refine your designs with various style and mood choices, adjusting them as needed.
        - **Creative Freedom**: AI helps you bring your imagination to life, offering a wide array of visual results.

        #### **When AI Falls Short: Bridging the Gap with Human Expertise**
        While AI is an incredibly powerful tool, it’s not perfect. Sometimes, the output isn’t exactly what you had in mind — whether it’s a mismatch with your vision, missing details, or just a final piece that doesn’t feel “right.” That’s where **human experts** step in.

        Imagine you’re using the AI to create a logo, an advertisement, or a piece of concept art. While the AI provides you with a strong starting point, you might feel that the image needs refinement, additional details, or a more tailored approach. This is where **Ailustrations’s Expert Consultation** feature shines.

        #### **Direct Connection with Expert Designers**
        If you’re unsatisfied with the AI-generated image or if it’s not quite there yet, **Ailustrations** offers a **seamless integration** with **real human designers** who can step in to **refine and perfect your design**. This integration is designed to **optimize the creative process**, allowing you to iterate on the design with professional help.

        Here’s how the process works:
        1. **Generate the Image**: You start by using **AI** to generate your art. You can tweak the details and re-generate it until it’s somewhat close to what you want.
        2. **Provide Feedback**: If the AI fails to meet your expectations, you can **easily provide feedback** through our **chat-style interface**. Whether you need changes to the style, more detail, or a different color palette, our platform makes it easy to communicate your exact needs.
        3. **Consult a Human Expert**: If the AI still doesn’t get it right or if you need something more specific, you can **click “Consult an Expert”** directly from the image thread. This will open up a **real-time chat** with a human expert designer. These designers are skilled professionals with years of experience in various creative fields like graphic design, illustration, branding, and digital art.
        4. **Expert Refinement**: The human expert will **analyze your feedback** and work with you to refine the image. Whether it’s adjusting the design, adding fine details, or completely reworking the concept, they’ll guide you through the entire process.
        5. **Perfected Design**: After working with the expert, the final result will be **tailored to your exact vision**, ensuring that the AI-generated piece meets your needs and exceeds your expectations.

        #### **Why This Works**
        While AI is a fantastic tool for automating creative processes, there’s still a need for **human judgment, creativity, and refinement** in certain areas. The AI is great at providing ideas, inspiration, and fast results, but when it comes to **fine-tuning details** or **interpreting abstract concepts**, a **human designer** is better equipped to understand the nuances of a design.

        At **Ailustrations**, we’ve recognized that there’s **no one-size-fits-all solution** to creativity. The perfect blend of **AI speed and efficiency** with **human intuition and experience** is what makes our platform so powerful. Whether you’re using the AI to generate initial ideas or to create a polished final product, we ensure that you’ll always have access to **expert designers** who can help bring your vision to life.

        #### **Benefits of Combining AI and Human Expertise**
        - **Speed & Efficiency**: The AI helps you get started quickly and generates several options fast.
        - **Creativity & Innovation**: AI can produce a variety of unique results that you might not have thought of.
        - **Personalized Touch**: Human designers refine your art to add details that align with your specific goals and creative preferences.
        - **Expert Consultation**: If you’re feeling stuck or want professional input, you can always rely on our **expert designers** for help.

        #### **A Collaborative Approach**
        At Ailustrations, we believe in the power of **collaboration**. Our AI and human experts work together, offering a unique combination of **automation and artistry** to help you create the best visuals possible. Whether you’re designing for personal use or professional projects, **Ailustrations** ensures that you have the tools and expertise needed to bring your ideas to life.

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
        """, unsafe_allow_html=True)


    #     st.markdown("""
    #     Welcome to **Ailustrations** – your all-in-one AI-powered image generation platform!

    #     ---  
    #     ### 📌 What is Ailustrations?
    #     Ailustrations allows users to generate stunning visuals using cutting-edge AI, refine them through feedback, and even consult experts for perfection.

    #     - 🚀 Powered by `Stable Diffusion XL`
    #     - 🧠 Real-time feedback and image enhancement
    #     - 💬 Live chat support with experts
    #     - 💾 Download and save generated art

    #     ---

    #    ### ❓ Frequently Asked Questions

    #     ##### **Q. Do I need to log in?**  
    #     Yes, logging in is required to personalize your experience. It allows us to save your work, enable chat support, and offer tailored features such as saving your image history and preferences.

    #     ##### **Q. Can I download images?**  
    #     Absolutely! Once your image is generated, you'll find a download button that allows you to easily save your artwork. We ensure you have complete ownership of the creations you generate.

    #     ##### **Q. Can I give feedback and regenerate images?**  
    #     Definitely! After generating an image, you can provide feedback using our chat-style interface. Our AI will use your input to instantly regenerate and refine the image, helping you perfect your vision.

    #     ##### **Q. Can I talk to a human expert?**  
    #     Yes, you can! If you need expert guidance or have specific questions, click on the “Consult an Expert” button in the image thread. This will connect you with a professional via Tawk.to for real-time assistance.

    #     ##### **Q. Where are my images stored?**  
    #     Your generated images are temporarily stored within the platform. After generation, you can download them immediately. 

    #     ---

    #     ### 📬 Still have questions?
    #     Feel free to consult our expert from the image interface or reach out via [Linkedin](https://www.linkedin.com/in/somya-bhushan/)
    #     """)
