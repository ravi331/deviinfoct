import streamlit as st
from utils import load_csv, safe_path

def teacher_dashboard():
    st.header("👩‍🏫 Teacher Dashboard")

    st.subheader("All Student Registrations")
    df = load_csv(
        safe_path("registrations.csv"),
        ["Timestamp", "Name", "Class", "Section", "Item", "Address", "Bus", "Contact", "Status"]
    )
    st.dataframe(df, use_container_width=True)

    st.subheader("Filter by Class")
    class_filter = st.text_input("Enter Class (e.g., 10, 11, 12)")
    if class_filter:
        filtered = df[df["Class"].astype(str).str.contains(class_filter)]
        st.dataframe(filtered, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download All Registrations", csv_data, "all_registrations.csv", "text/csv")
