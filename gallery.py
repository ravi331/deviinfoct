import streamlit as st
from utils import list_gallery_images, ensure_gallery, GALLERY_DIR
import os

def show_gallery(admin=False):
    st.header("Gallery")
    ensure_gallery()
    images = list_gallery_images()

    if not images:
        st.error("📁 No images found in the gallery folder.")
    else:
        cols = st.columns(3)
        for idx, img in enumerate(images):
            try:
                cols[idx % 3].image(img, use_container_width=True)
            except:
                cols[idx % 3].warning(f"⚠ Could not load: {img}")

    if admin:
        st.subheader("Admin: Upload to Gallery")
        file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif", "webp"])
        if file:
            path = os.path.join(GALLERY_DIR, file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            st.success(f"✅ Uploaded {file.name}")
            st.experimental_rerun()
