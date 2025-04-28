#set_background.py
# This file can be used to set a background image for the Streamlit app.
import base64
import streamlit as st # type: ignore

def set_gradient_background():
    gradient_css = """
    <style>
    .stApp {
        background: linear-gradient(to right, #000000, #3533cd);
        background-attachment: fixed;
    }
    </style>
    """
    st.markdown(gradient_css, unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = f"""
    <style>
    .blurred-background {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: blur(5px);
        z-index: -1;
    }}
    .stApp {{
        background: transparent;
    }}
    </style>
    <div class="blurred-background"></div>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
