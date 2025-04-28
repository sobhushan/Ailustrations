# main.py
import streamlit as st  # type: ignore
from app.main_app import main_app
from auth.firebase_auth import login, signup, verify_id_token, refresh_id_token
from app import info_page
from datetime import datetime, timedelta
from set_background import set_gradient_background
import time

# Page config
st.set_page_config(page_title="Imagino", layout="wide")
set_gradient_background()

# --- Navbar ---
def navbar():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 3rem;
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

    nav_col1, nav_col2 = st.columns([8, 2])

    # with nav_col1:
    #     st.markdown("<h1 style='color: white; text-align: left; font-size: 70px;'>Welcome to <span style='color:#6C63FF;'>Imagino</span></h1>", unsafe_allow_html=True)

    with nav_col2:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", key="navbar_login"):
                st.session_state.show_login = True
                st.session_state.show_signup = False
                st.rerun()
        with col2:
            if st.button("Get Started", key="navbar_signup"):
                st.session_state.show_signup = True
                st.session_state.show_login = False
                st.rerun()

# --- Hero Section (only for not logged-in users) ---
def hero_section():
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<h1 style='color: white; text-align: left; font-size: 70px;'>Welcome to <span style='color:#6C63FF;'>Imagino</span></h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #FFD700;text-align: left;'>Turn your ideas into stunning AI-generated images instantly!</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style='color: #f0f0f0; font-size: 1.2rem; text-align: left;'>
            Imagino is your AI-powered tool to turn ideas into stunning visuals in just a few clicks. Whether you're a designer, marketer, or a creative mind, Imagino helps you unleash your imagination — with real-time expert consultation to refine and perfect your results.
            </p>
            <br>
            """,
            unsafe_allow_html=True
        )
        if st.button("Get Started", key="hero_get_started"):
            st.session_state.show_signup = True
            st.session_state.show_login = False
            st.session_state.trigger_scroll = True
            st.rerun()

        st.write("---")
        auth_ui()

    with col2:
        st.image("mascot.png", 
                 width=550)
                #  use_container_width=True)

# --- Authentication UI (merged clean version) ---
def auth_ui():
    if st.session_state.get('show_login', False):
        with st.form(key="login_form"):
            st.write("### Login")
            email = st.text_input("Enter your email", placeholder="name@example.com", key="login_email")
            password = st.text_input("Enter your password", placeholder="••••••••", type="password", key="login_password")
            login_submit = st.form_submit_button("Log In",use_container_width=True)
            if login_submit:
                with st.spinner("Logging you in..."):
                    res = login(email, password)
                    if res.status_code == 200:
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
                        st.rerun()
                    else:
                        st.error(f"❌ {res.json()['error']['message']}")

    if st.session_state.get('show_signup', False):
        with st.form(key="signup_form"):
            st.write("### Sign Up")
            email = st.text_input("Enter your email", placeholder="name@example.com", key="signup_email")
            password = st.text_input("Enter your password", placeholder="••••••••", type="password", key="signup_password")
            signup_submit = st.form_submit_button("Sign Up", use_container_width=True)
            if signup_submit:
                with st.spinner("Creating your account..."):
                    res = signup(email, password)
                    if res.status_code == 200:
                        st.success("🎉 Account created! Please log in now.")
                        st.session_state.show_signup = False
                        st.session_state.show_login = True
                    else:
                        st.error(f"❌ {res.json()['error']['message']}")

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
        }
        h1, h2 {
            color: white;
            font-size: 3em;
        }
        p {
            color: #f0f0f0;
            font-size: 1.2em;
        }
        .stForm {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 12px;
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
            st.markdown(f"👤 Logged in as: `{user['email']}`")
            # st.markdown("---")
            # st.markdown("### Navigation")
            nav_options = ["Main App", "About & Help", "Logout"]
            nav_choice = st.radio(
                "---",
                options=nav_options,
                index=nav_options.index(st.session_state.get("page", "Main App")) if st.session_state.get("page") != "Logout" else 0
            )

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



#------------------------------------------------------------------------
# # main.py
# import streamlit as st  # type: ignore
# from app.main_app import main_app
# from auth.firebase_auth import login, signup, verify_id_token, refresh_id_token
# from app import info_page
# from datetime import datetime, timedelta

# st.set_page_config(page_title="Imagino", layout="centered")

# def auth_ui():
#     with st.container():
#         st.markdown("<h2 style='text-align: center;'>🔐 Welcome to <span style='color:#6C63FF;'>Imagino</span></h2>", unsafe_allow_html=True)
#         st.markdown("<p style='text-align: center; color:gray;'>Please log in or sign up to continue.</p>", unsafe_allow_html=True)
#         st.write("---")

#         col1, col2, col3 = st.columns([1, 3, 1])
#         with col2:
#             mode = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

#             email = st.text_input("Enter your email", placeholder="name@example.com")

#             password = st.text_input("Enter your password", placeholder="••••••••", type="password")

#             if mode == "Login":
#                 if st.button("Log In"):
#                     with st.spinner("Logging you in..."):
#                         res = login(email, password)
#                         if res.status_code == 200:
#                             # st.session_state['user'] = res.json()
#                             data = res.json()
#                             refresh_token = data["refreshToken"]    
#                             st.session_state["user"] = {
#                                 "email": data["email"],
#                                 "idToken": data["idToken"],
#                                 "refreshToken": refresh_token,
#                                 "expiresAt": (datetime.now() + timedelta(seconds=int(data["expiresIn"]))).timestamp()
#                             }
#                             st.query_params.update({"refresh_token": refresh_token})
#                             st.success("✅ Logged in successfully!")
#                             st.rerun()
#                         else:
#                             st.error(f"❌ {res.json()['error']['message']}")
#             else:
#                 if st.button("📝 Sign Up"):
#                     with st.spinner("Creating your account..."):
#                         res = signup(email, password)
#                         if res.status_code == 200:
#                             st.success("🎉 Account created! You can log in now.")
#                         else:
#                             st.error(f"❌ {res.json()['error']['message']}")
# def refresh_session_token():
#     """Check token expiry and refresh if needed."""
#     user = st.session_state.get("user")
#     if not user:
#         return

#     expires_at = user.get("expiresAt", 0)
#     if datetime.now().timestamp() > expires_at:
#         refresh_token = user.get("refreshToken")
#         if refresh_token:
#             res = refresh_id_token(refresh_token)
#             if "id_token" in res:
#                 st.session_state["user"]["idToken"] = res["id_token"]
#                 st.session_state["user"]["expiresAt"] = (datetime.now() + timedelta(seconds=int(res["expires_in"]))).timestamp()
#                 st.session_state["user"]["refreshToken"] = res["refresh_token"]

# def main():
#     st.markdown("""
#         <style>
#             .stSidebar .stRadio p {
#                 color: white; 
#             }

#             .stSidebar .stRadio p:hover {
#                 color: #4B36F7; 
#             }
#             .stSidebar .stRadio p:active {
#                 background-color: #6C63FF;  /* Change background on click */
#                 color: white;
#             }

#             /* Change active button color */
#             .stSidebar .stRadio .st-aqAHzv label {
#                 background-color: #6C63FF;
#                 color: white;
#             }
#         </style>
#     """, unsafe_allow_html=True)

#     # Get refresh_token from URL query parameters
#     params = st.query_params
#     refresh_token_param = params.get("refresh_token")

#     # Attempt restoring session if refresh_token is present
#     if "user" not in st.session_state and refresh_token_param:
#             res = refresh_id_token(refresh_token_param)
#             if "id_token" in res:
#                 decoded = verify_id_token(res["id_token"])
#                 if decoded:
#                     st.session_state["user"] = {
#                         "email": decoded.get("email", "unknown"), 
#                         "idToken": res["id_token"],
#                         "refreshToken": res["refresh_token"],
#                         "expiresAt": (datetime.now() + timedelta(seconds=int(res["expires_in"]))).timestamp()
#                     }
#                 # st.query_params.clear()

#     # Show login page if session not available
#     if "user" not in st.session_state:
#         auth_ui()
#     else:
#         # Refresh token if expired
#         refresh_session_token()

#         # Verify token
#         user = st.session_state["user"]
#         decoded_token = verify_id_token(user["idToken"])

#         if not decoded_token:
#             st.warning("Session expired or invalid. Please log in again.")
#             st.session_state.clear()
#             st.rerun()

#         # Sidebar
#         st.sidebar.markdown(f"👤 Logged in as: `{user['email']}`")
#         st.sidebar.markdown("---")
#         st.sidebar.markdown("### 📂 Navigation")

#         nav_options = ["🏠 Main App", "ℹ️ About & Help", "❌ Logout"]
#         nav_choice = st.sidebar.radio(
#             "---",  
#             options=nav_options,
#             index=nav_options.index(st.session_state.get("page", "🏠 Main App")) if st.session_state.get("page") != "❌ Logout" else 0
#         )

#         if nav_choice == "❌ Logout":
#             st.session_state.clear()
#             st.query_params.clear()
#             st.rerun()
#         else:
#             st.session_state["page"] = nav_choice
#             if nav_choice == "🏠 Main App":
#                 main_app()
#             elif nav_choice == "ℹ️ About & Help":
#                 info_page.main()


#         # main_app()

# if __name__ == "__main__":
#     main()