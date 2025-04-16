# main.py
import streamlit as st  # type: ignore
from app.main_app import main_app
from auth.firebase_auth import login, signup

st.set_page_config(page_title="Imagino - Login", layout="centered")

def auth_ui():
    with st.container():
        st.markdown("<h2 style='text-align: center;'>🔐 Welcome to <span style='color:#6C63FF;'>Imagino</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:gray;'>Please log in or sign up to continue.</p>", unsafe_allow_html=True)
        st.write("---")

        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            mode = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

            # st.markdown("#### 📧 Email")
            email = st.text_input("Enter your email", placeholder="name@example.com")

            # st.markdown("#### 🔑 Password")
            password = st.text_input("Enter your password", placeholder="••••••••", type="password")

            if mode == "Login":
                if st.button("Log In"):
                    with st.spinner("Logging you in..."):
                        res = login(email, password)
                        if res.status_code == 200:
                            st.session_state['user'] = res.json()
                            st.success("✅ Logged in successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ {res.json()['error']['message']}")
            else:
                if st.button("📝 Sign Up"):
                    with st.spinner("Creating your account..."):
                        res = signup(email, password)
                        if res.status_code == 200:
                            st.success("🎉 Account created! You can log in now.")
                        else:
                            st.error(f"❌ {res.json()['error']['message']}")

def main():
    if "user" not in st.session_state:
        auth_ui()
    else:
        st.sidebar.markdown(f"👤 Logged in as: `{st.session_state['user']['email']}`")
        if st.sidebar.button("<-]   Logout"):
            st.session_state.clear()
            st.rerun()
        main_app()

if __name__ == "__main__":
    main()




# import streamlit as st # type: ignore
# from app.main_app import main_app
# from auth.firebase_auth import login, signup

# st.set_page_config(page_title="Imagino", layout="centered")

# def auth_ui():
#     st.title("🔐 Login / Sign Up")

#     mode = st.radio("Choose an option:", ["Login", "Sign Up"])
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")

#     if mode == "Login":
#         if st.button("Login"):
#             res = login(email, password)
#             if res.status_code == 200:
#                 st.session_state['user'] = res.json()
#                 st.success("Logged in successfully!")
#                 st.rerun()
#             else:
#                 st.error(res.json()["error"]["message"])

#     elif mode == "Sign Up":
#         if st.button("Sign Up"):
#             res = signup(email, password)
#             if res.status_code == 200:
#                 st.success("Account created! You can log in now.")
#             else:
#                 st.error(res.json()["error"]["message"])

# def main():
#     if "user" not in st.session_state:
#         auth_ui()
#     else:
#         st.sidebar.success(f"Logged in as: {st.session_state['user']['email']}")
#         if st.sidebar.button("Logout"):
#             st.session_state.clear()
#             st.rerun()
#         main_app()

# if __name__ == "__main__":
#     main()
