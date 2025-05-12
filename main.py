# main.py
import streamlit as st  # type: ignore
from app.main_app import main_app
from auth.firebase_auth import login, signup, verify_id_token, refresh_id_token, send_password_reset_email
from app import info_page
from datetime import datetime, timedelta
from set_background import set_gradient_background
import time
import streamlit.components.v1 as components # type: ignore

# Page config
st.set_page_config(page_title="Ailustrations", 
                   layout="wide",
                   page_icon="favicon.png",)

components.html("""
  <head>
    <title>Ailustrations – AI Image Generator with Human Touch</title>
    <meta name="description" content="Generate stunning AI images and refine them with expert feedback. Ailustrations blends AI with human creativity." />
    <meta name="keywords" content="AI image generator, AI art, custom images, image refinement, generative AI, human feedback" />
    <meta name="robots" content="index, follow" />
  </head>
""", height=0)

if st.session_state.get("show_info_page"):
    info_page.main() 
    st.stop()

set_gradient_background()
# --- Navbar ---
def navbar():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 0rem;
        }
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: transparent;
        }
        .nav-left {
            font-size: 1.8rem;
            font-weight: bold;
            color: white;
        }
        .nav-buttons {
            display: flex;
            gap: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    nav_col1, nav_col2 = st.columns([8, 3])

    with nav_col2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <style>
                .about-link a {
                    color: white;
                    text-decoration: none;
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                    font-weight: 500;
                    transition: background-color 0.3s ease, text-decoration 0.3s ease;
                    display: inline-block;
                    width: 100%;
                    height: 50px;
                    line-height: 50px;
                    text-align: center;
                }
                .about-link a:hover,
                .about-link a:active {
                    background: linear-gradient(135deg, #6C63FF 0%, #9C88FF 100%);
                    color: #f0f0f0;
                    text-decoration: none;
                }
                </style>
                <div class="about-link">
                    <a href="?about_us=true">About Us</a>
                </div>
            """, unsafe_allow_html=True)

        # Check query parameter using new API
        params = st.query_params
        if "about_us" in params:
            st.session_state.show_info_page = True
            st.rerun()

        with col2:
            if st.button("Login", key="navbar_login"):
                st.session_state.show_login = True
                st.session_state.show_signup = False
                st.session_state.scroll_to = "login"
                st.rerun()
        with col3:
            if st.button("Signup", key="navbar_signup"):
                st.session_state.show_signup = True
                st.session_state.show_login = False
                st.session_state.scroll_to = "sign-up"
                st.rerun()

# --- Hero Section (only for not logged-in users) ---
def hero_section():
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<h1 style='color: white; text-align: left; font-size: 50px;'>Welcome to <span style='color:#6C63FF; font-size: 60px;'>Ailustrations</span></h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #FFD700;text-align: left;'>Turn your ideas into stunning AI-generated images instantly!</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='color: #f0f0f0; font-size: 1.2rem; text-align: left;'>
            Ailustrations is your AI-powered tool to turn ideas into stunning visuals in just a few clicks. Whether you're a designer, marketer, or a creative mind, Ailustrations helps you unleash your imagination — with real-time expert consultation to refine and perfect your results.
            </p>
            <br>
            """,
            unsafe_allow_html=True
        )
        if st.button("Get Started", key="hero_get_started"):
            st.session_state.show_signup = True
            st.session_state.show_login = False
            st.session_state.scroll_to = "sign-up"
            st.rerun()

        st.write("---")
        auth_ui()

    with col2:
        st.image("mascot.png", 
                 width=550)

# --- Authentication UI (merged clean version) ---
def auth_ui():
    if st.session_state.get("signup_success", False):
        st.success("🎉 Account created! Redirecting to login...")
        time.sleep(2)
        st.session_state.signup_success = False
        st.session_state.signup_confirmed = True
        st.rerun()

    if st.session_state.get("signup_confirmed", False):
        # Now show login form after seeing the message
        st.session_state.signup_confirmed = False
        st.session_state.show_login = True
        st.rerun()
    
    if st.session_state.get('show_login', False):
        st.components.v1.html('<div id="login" style="height:0;"></div>', height=0)
        # st.markdown('<div id="login" style="height:0;"></div>', unsafe_allow_html=True)
        with st.form(key="login_form"):
            st.write("### Login")
            email = st.text_input("Enter your email", placeholder="name@example.com", key="login_email", value=st.session_state.get("signup_email_store", ""))
            password = st.text_input("Enter your password", placeholder="••••••••", type="password", key="login_password")
            login_submit = st.form_submit_button("Log In",use_container_width=True)
            if login_submit:
                with st.spinner("Logging you in..."):
                    res = login(email, password)
                    if isinstance(res, dict) and "error" in res:
                        st.error(res["error"])
                    elif hasattr(res, "status_code") and res.status_code == 200:
                        data = res.json()
                        refresh_token = data["refreshToken"]
                        st.session_state["user"] = {
                            "email": data["email"],
                            "idToken": data["idToken"],
                            "refreshToken": refresh_token,
                            "expiresAt": (datetime.now() + timedelta(seconds=int(data["expiresIn"]))).timestamp()
                        }
                        st.query_params.update({"refresh_token": refresh_token})
                        st.success("✅ Logged in successfully!")
                        st.session_state.show_login = False
                        st.session_state.show_signup = False
                        st.session_state.show_loading = True
                        st.session_state.user_email = data["email"]  
                        st.rerun()
                    else:
                        st.error(f"❌ {res.json()['error']['message']}")
        forgot_password_ui()

    if st.session_state.get('show_signup', False):
        st.markdown('<div id="sign-up" style="height:0;"></div>', unsafe_allow_html=True)
        with st.form(key="signup_form"):
            st.write("### Sign Up")
            email = st.text_input("Enter your email", placeholder="name@example.com", key="signup_email")
            password = st.text_input("Enter your password", placeholder="••••••••", type="password", key="signup_password")
            signup_submit = st.form_submit_button("Sign Up", use_container_width=True)
            if signup_submit:
                with st.spinner("Creating your account..."):
                    res = signup(email, password)
                    if res.status_code == 200:
                        st.session_state.signup_success = True
                        st.session_state.show_signup = False
                        st.session_state.signup_email_store = email
                        st.rerun()
                        # st.success("🎉 Account created! Please log in now.")
                        # st.session_state.show_signup = False
                        # st.session_state.show_login = True
                        # st.rerun()
                    else:
                        st.error(f"❌ {res.json()['error']['message']}")
        

def forgot_password_ui():
    st.markdown("""
        <style>
        .stExpander label {
            color: white !important;
        }
        @media (prefers-color-scheme: light) {
                [data-testid="stExpander"] {
                    border: 1px solid #F0F2F6;   
                    border-radius: 10px;
                    padding: 5px;
                    margin-top: 10px;
                }
        </style>
    """, unsafe_allow_html=True)

    with st.expander("Forgot Password? Click to reset your password"):
        email = st.text_input("Enter your email", key="forgot_email", placeholder="Enter your email")
        if st.button("Send Password Reset Email"):
            if email:
                res = send_password_reset_email(email)
                if res.status_code == 200:
                    st.success("✅ If your email is registered, a password reset link will be sent. Please check your inbox.")
                else:
                    st.error(f"❌ Failed: {res.json().get('error', {}).get('message', 'Unknown error')}")
            else:
                st.warning("⚠️ Please enter your email.")

# Trigger scroll after rerun
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

# --- Handle Session ---
if "show_login" not in st.session_state:
    st.session_state.show_login = False
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# --- Refresh Token Logic ---
def refresh_session_token():
    """Check token expiry and refresh if needed."""
    user = st.session_state.get("user")
    if not user:
        return

    expires_at = user.get("expiresAt", 0)
    if datetime.now().timestamp() > expires_at:
        refresh_token = user.get("refreshToken")
        if refresh_token:
            res = refresh_id_token(refresh_token)
            if "id_token" in res:
                st.session_state["user"]["idToken"] = res["id_token"]
                st.session_state["user"]["expiresAt"] = (datetime.now() + timedelta(seconds=int(res["expires_in"]))).timestamp()
                st.session_state["user"]["refreshToken"] = res["refresh_token"]

# --- Main App Logic ---
def main():
    st.markdown(
        """
        <style>
        .stButton > button {
            width: 100%;
            height: 50px;
            font-size: 18px;
            background: linear-gradient(135deg, #6C63FF 0%, #9C88FF 100%);
            color: white;
            border: none;
            border-radius: 8px;
            transition: background 0.3s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #4B36F7 0%, #6C63FF 100%);
            color: #f0f0f0;
        }
        .stButton > button:focus,
        .stButton > button:active {
            background: linear-gradient(135deg, #4B36F7 0%, #6C63FF 100%);
            color: #f0f0f0 !important;
        }
        h1, h2 {
            color: white;
            font-size: 3em;
        }
        # p {
        #     color: white;
        # }
        .stForm {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 12px;
        }
        .stForm button p {
            color: black; /* Default for light mode */
        }

        @media (prefers-color-scheme: dark) {
            .stForm button p {
                color: white;
            }
        }

        .stForm p, .stForm h3 {
            color : white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Get refresh_token from URL query parameters
    params = st.query_params
    refresh_token_param = params.get("refresh_token")

    # Restore session if possible
    if "user" not in st.session_state and refresh_token_param:
        res = refresh_id_token(refresh_token_param)
        if "id_token" in res:
            decoded = verify_id_token(res["id_token"])
            if decoded:
                st.session_state["user"] = {
                    "email": decoded.get("email", "unknown"),
                    "idToken": res["id_token"],
                    "refreshToken": res["refresh_token"],
                    "expiresAt": (datetime.now() + timedelta(seconds=int(res["expires_in"]))).timestamp()
                }
     # Handle Loading Screen
    if st.session_state.get("show_loading", False):
        with st.spinner('Setting up your main page... '):
            time.sleep(2)  # simulate loading for 2 seconds
        st.session_state.show_loading = False
        st.rerun()

    # If no user session, show auth UI
    if "user" not in st.session_state:
        navbar()
        hero_section()
    else:
        refresh_session_token()
        user = st.session_state["user"]
        decoded_token = verify_id_token(user["idToken"])

        if not decoded_token:
            st.warning("Session expired or invalid. Please log in again.")
            st.session_state.clear()
            st.rerun()

        # Sidebar
        with st.sidebar:
            st.markdown(f"👤 Logged in as: ")
            st.markdown(
            f"""
            <div style="
                background-color: #1a1c24;
                color: green;
                padding: 8px 12px;
                border-radius: 8px;
                display: inline-block;
                font-size: 14px;
            ">
                {user['email']}
            </div>
            """,
            unsafe_allow_html=True
            )
            nav_options = ["Main App", "About & Help", "Logout"]
            nav_choice = st.radio(
                "---",
                options=nav_options,
                index=nav_options.index(st.session_state.get("page", "Main App")) if st.session_state.get("page") != "Logout" else 0
            )
        st.sidebar.markdown("---")
        # Navigation Handling
        if nav_choice == "Logout":
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()
        else:
            st.session_state["page"] = nav_choice
            if nav_choice == "Main App":
                main_app()
            elif nav_choice == "About & Help":
                info_page.main()

if __name__ == "__main__":
    main()