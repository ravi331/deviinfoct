import streamlit as st
import pandas as pd

def login_sidebar():
    st.sidebar.title("🔐 Login")

    mobile = st.sidebar.text_input("Mobile Number")
    password = st.sidebar.text_input("Password", type="password")
    login_btn = st.sidebar.button("Login")

    if login_btn:
        if mobile and password:
            try:
                df = pd.read_csv("allowed_users.csv")
                user = df[(df["mobile"] == mobile) & (df["password"] == password)]
                if not user.empty:
                    st.session_state["logged_in"] = True
                    st.session_state["mobile"] = mobile
                    st.session_state["role"] = user.iloc[0]["role"]
                    st.sidebar.success(f"✅ Logged in as {user.iloc[0]['role']}")
                else:
                    st.sidebar.error("❌ Invalid credentials")
            except Exception as e:
                st.sidebar.error("⚠️ Error loading user data")
        else:
            st.sidebar.warning("Please enter both mobile and password")
