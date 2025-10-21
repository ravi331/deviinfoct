import os
import pandas as pd
from datetime import datetime

# Base directory
BASE_DIR = os.getcwd()
GALLERY_DIR = os.path.join(BASE_DIR, "gallery")
EVENT_DATETIME = datetime(2025, 12, 20, 0, 0, 0)

def safe_path(filename: str) -> str:
    return os.path.join(BASE_DIR, filename)

def load_csv(file, columns):
    try:
        return pd.read_csv(file)
    except:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file, index=False)
        return df

def normalize_number(series):
    return (
        series.astype(str)
        .str.replace(r"\D", "", regex=True)  # removes all non-digits
        .str[-10:]
    )


def ensure_gallery():
    if not os.path.exists(GALLERY_DIR):
        os.makedirs(GALLERY_DIR)

def list_gallery_images():
    ensure_gallery()
    return [
        os.path.join(GALLERY_DIR, f)
        for f in os.listdir(GALLERY_DIR)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
    ]

def time_remaining():
    diff = EVENT_DATETIME - datetime.now()
    if diff.total_seconds() <= 0:
        return "🎉 Today is the Annual Function!"
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    mins, secs = divmod(rem, 60)
    return f"{days} days, {hours} hrs, {mins} mins, {secs} secs"

