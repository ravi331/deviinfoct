import streamlit as st
from utils import load_csv, safe_path
from datetime import datetime

# Admin password stored securely in .streamlit/secrets.toml
ADMIN_PASSWORD = st.secrets["admin"]["password"]

def admin_panel():
    ss = st.session_state
    st.header("Admin Panel")

    if not ss.get("admin_logged_in"):
        pw = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if pw == ADMIN_PASSWORD:
                ss.admin_logged_in = True
                st.success("✅ Admin Logged In")
            else:
                st.error("❌ Wrong Password")
    else:
        st.success("✅ You are logged in as Admin")
        if st.button("Logout Admin"):
            ss.admin_logged_in = False
            st.experimental_rerun()

def post_announcement():
    ss = st.session_state
    if ss.get("admin_logged_in"):
        st.subheader("Post Announcement (Admin Only)")
        title = st.text_input("Title")
        msg = st.text_area("Message")
        by = st.text_input("Posted By", "Admin")
        if st.button("Post Announcement"):
            df = load_csv(safe_path("notices.csv"), ["Timestamp", "Title", "Message", "PostedBy"])
            df.loc[len(df)] = [datetime.now(), title, msg, by]
            df.to_csv(safe_path("notices.csv"), index=False)
            st.success("✅ Announcement Posted")
            st.rerun()

