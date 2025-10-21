import streamlit as st
import pandas as pd

def login_sidebar():
    st.sidebar.title("🔐 Login")

    mobile = st.sidebar.text_input("Mobile Number")
    login_btn = st.sidebar.button("Login")

    if login_btn:
        if mobile:
            try:
                df = pd.read_csv("allowed_users.csv")
                user = df[df["mobile"] == mobile]
                if not user.empty:
                    st.session_state["logged_in"] = True
                    st.session_state["mobile"] = mobile
                    st.session_state["role"] = user.iloc[0]["role"]
                    st.sidebar.success(f"✅ Logged in as {user.iloc[0]['role']}")
                else:
                    st.sidebar.error("❌ Mobile number not found")
            except Exception as e:
                st.sidebar.error("⚠️ Error loading user data")
        else:
            st.sidebar.warning("Please enter your mobile number")
