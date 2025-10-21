import streamlit as st
from utils import time_remaining, load_csv, safe_path
from auth import login_sidebar
from gallery import show_gallery
from admin import admin_panel, post_announcement
from registration import registration_form
from student import student_dashboard
from teacher import teacher_dashboard

# ==================== CONFIG ====================
st.set_page_config(page_title="SGS Annual Function 2025", layout="wide", page_icon="🎉")

# ==================== LOGIN ====================
login_sidebar()
ss = st.session_state
if not ss.get("logged_in"):
    st.stop()

# ==================== WELCOME ====================
if not ss.get("welcomed"):
    st.image("images/mascot.png", width=250)
    st.subheader(f"🎉 Welcome, {ss.mobile}!")
    ss.welcomed = True
    st.experimental_rerun()

# ==================== TABS ====================
tabs = ["Home", "Registration", "Gallery", "Announcements"]
if ss.get("role") == "admin":
    tabs.append("Admin")
elif ss.get("role") == "teacher":
    tabs.append("Teacher Dashboard")
elif ss.get("role") == "student":
    tabs.append("Student Dashboard")

tab_objs = st.tabs(tabs)

# -------------------- HOME --------------------
with tab_objs[0]:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("images/mascot.png", width=300)
    with col2:
        st.image("logo.png", width=450)
        st.markdown("### 45th Annual Day – Talent Meets Opportunity")
    notices = load_csv(safe_path("notices.csv"), ["Timestamp", "Title", "Message", "PostedBy"])
    if not notices.empty:
        latest = notices.iloc[-1]
        st.info(f"📢 **{latest['Title']}**\n{latest['Message']}")
    st.success(f"⏳ Countdown: {time_remaining()}")

# -------------------- REGISTRATION --------------------
with tab_objs[1]:
    registration_form()

# -------------------- GALLERY --------------------
with tab_objs[2]:
    show_gallery(admin=ss.get("admin_logged_in", False))

# -------------------- ANNOUNCEMENTS --------------------
with tab_objs[3]:
    st.header("Announcements")
    data = load_csv(safe_path("notices.csv"), ["Timestamp", "Title", "Message", "PostedBy"])
    if data.empty:
        st.info("No announcements yet.")
    else:
        for _, row in data.iterrows():
            st.write(f"### {row['Title']}\n{row['Message']}\n*— {row['PostedBy']} on {row['Timestamp']}*")
    post_announcement()

# -------------------- ADMIN --------------------
if ss.get("role") == "admin":
    with tab_objs[4]:
        admin_panel()

# -------------------- TEACHER --------------------
if ss.get("role") == "teacher":
    with tab_objs[4]:
        teacher_dashboard()

# -------------------- STUDENT --------------------
if ss.get("role") == "student":
    with tab_objs[4]:
        student_dashboard()
