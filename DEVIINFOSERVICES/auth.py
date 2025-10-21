import streamlit as st
import random
from utils import load_csv, normalize_number, safe_path

def login_sidebar():
    ss = st.session_state
    allowed_df = load_csv(safe_path("allowed_users.csv"), ["mobile_number", "name", "role"])
    allowed_df["mobile_number"] = normalize_number(allowed_df["mobile_number"])

    st.sidebar.title("Login")
    if not ss.get("logged_in"):
        mobile = st.sidebar.text_input("Enter 10-digit mobile number").strip()[-10:]
        if st.sidebar.button("Send OTP"):
            if mobile in allowed_df["mobile_number"].values:
                ss.otp = str(random.randint(100000, 999999))
                ss.mobile = mobile
                ss.role = allowed_df.loc[allowed_df["mobile_number"] == mobile, "role"].values[0]
                st.sidebar.success(f"OTP (Test Mode): {ss.otp}")
            else:
                st.sidebar.error("❌ Number not registered")
        if ss.get("otp"):
            otp_entered = st.sidebar.text_input("Enter OTP")
            if st.sidebar.button("Verify OTP"):
                if otp_entered == ss.otp:
                    ss.logged_in = True
                    st.sidebar.success("✅ Login successful!")
                else:
                    st.sidebar.error("❌ Incorrect OTP")
    else:
        st.sidebar.success(f"Logged in as: {ss.mobile} ({ss.role})")
        if st.sidebar.button("Logout"):
            for k in ["logged_in", "mobile", "otp", "welcomed", "admin_logged_in", "role"]:
                ss.pop(k, None)
            st.experimental_rerun()
