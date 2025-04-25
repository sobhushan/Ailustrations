# main.py
import streamlit as st  # type: ignore
from app.main_app import main_app
from auth.firebase_auth import login, signup, verify_id_token, refresh_id_token
from app import info_page
from datetime import datetime, timedelta

st.set_page_config(page_title="Imagino - Login", layout="centered")

def auth_ui():
    with st.container():
        st.markdown("<h2 style='text-align: center;'>🔐 Welcome to <span style='color:#6C63FF;'>Imagino</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color:gray;'>Please log in or sign up to continue.</p>", unsafe_allow_html=True)
        st.write("---")

        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            mode = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

            email = st.text_input("Enter your email", placeholder="name@example.com")

            password = st.text_input("Enter your password", placeholder="••••••••", type="password")

            if mode == "Login":
                if st.button("Log In"):
                    with st.spinner("Logging you in..."):
                        res = login(email, password)
                        if res.status_code == 200:
                            # st.session_state['user'] = res.json()
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

def main():
    # Get refresh_token from URL query parameters
    params = st.query_params
    refresh_token_param = params.get("refresh_token")

    # Attempt restoring session if refresh_token is present
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
                # st.query_params.clear()

    # Show login page if session not available
    if "user" not in st.session_state:
        auth_ui()
    else:
        # Refresh token if expired
        refresh_session_token()

        # Verify token
        user = st.session_state["user"]
        decoded_token = verify_id_token(user["idToken"])

        if not decoded_token:
            st.warning("Session expired or invalid. Please log in again.")
            st.session_state.clear()
            st.rerun()

        # Sidebar
        st.sidebar.markdown(f"👤 Logged in as: `{user['email']}`")
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📂 Navigation")

        nav_options = ["🏠 Main App", "ℹ️ About & Help", "❌ Logout"]
        nav_choice = st.sidebar.radio(
            "---",  
            options=nav_options,
            index=nav_options.index(st.session_state.get("page", "🏠 Main App")) if st.session_state.get("page") != "❌ Logout" else 0
        )

        if nav_choice == "❌ Logout":
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()
        else:
            st.session_state["page"] = nav_choice
            if nav_choice == "🏠 Main App":
                main_app()
            elif nav_choice == "ℹ️ About & Help":
                info_page.main()


        # main_app()

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