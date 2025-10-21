import streamlit as st
import pandas as pd
import os

def post_announcement():
    st.subheader("📢 Post a New Announcement")
    message = st.text_area("Announcement Message")
    if st.button("Post Announcement"):
        if message.strip():
            new_announcement = pd.DataFrame([{"message": message.strip()}])
            if os.path.exists("announcements.csv"):
                existing = pd.read_csv("announcements.csv")
                combined = pd.concat([existing, new_announcement], ignore_index=True)
            else:
                combined = new_announcement
            combined.to_csv("announcements.csv", index=False)
            st.success("✅ Announcement posted!")
        else:
            st.warning("Please enter a message before posting.")

def manage_announcements():
    st.subheader("🗑️ Delete Announcements")
    if os.path.exists("announcements.csv"):
        df = pd.read_csv("announcements.csv")
        if not df.empty:
            for i, row in df[::-1].iterrows():  # Show latest first
                st.info(f"📢 {row['message']}")
                if st.button(f"Delete", key=f"del_{i}"):
                    df.drop(index=i, inplace=True)
                    df.to_csv("announcements.csv", index=False)
                    st.success("✅ Announcement deleted")
                    st.experimental_rerun()
        else:
            st.info("No announcements yet.")
    else:
        st.info("No announcements file found.")
