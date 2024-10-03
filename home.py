import os
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv

load_dotenv()

try:
    app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    app = firebase_admin.initialize_app(
        cred, options={"storageBucket": "fish-project-2k24.appspot.com"}
    )

db = firestore.client()
bucket = storage.bucket()

if __name__ == "__main__":
    with st.form("upload_form", clear_on_submit=True):
        file = st.file_uploader("Upload file", type=["jpg", "jpeg", "png"])
        address = st.text_input(label="Place", placeholder="Somewhere..")
        date = st.date_input(label="Date")
        hour = st.time_input(label="Hour")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            with st.spinner("Uploading file..."):
                if file:
                    blob = bucket.blob(file.name)
                    blob.upload_from_file(file)
                    blob.make_public()
                    url = blob.public_url
                else:
                    st.warning("No file uploaded")

            with st.spinner("Uploading data..."):
                data = {
                    "address": address,
                    "photo": url,
                    "date": date.strftime("%d/%m/%Y"),
                    "hour": hour.strftime("%H:%M"),
                }
                db.collection("fish").add(data)
