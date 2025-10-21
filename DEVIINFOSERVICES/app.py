import streamlit as st
import pandas as pd
import os
from auth import login_sidebar
from registration import register_student

st.set_page_config(page_title="Annual Day Registration", layout="wide")
login_sidebar()

ss = st.session_state

if ss.get("logged_in"):
    st.title("🎉 Annual Day Registration Portal")

    register_student()

    st.header("📋 Registered Students")

    if os.path.exists("registrations.csv"):
        df = pd.read_csv("registrations.csv")
        if not df.empty:
            st.dataframe(df)
            # Optional: Admin-only download
            if ss.get("role") == "admin":
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", data=csv_data, file_name="registrations.csv")
        else:
            st.info("No registrations yet.")
    else:
        st.info("No registrations found.")
else:
    st.warning("🔒 Please log in to access registration.")
