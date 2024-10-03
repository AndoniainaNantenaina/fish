import os
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
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

if __name__ == "__main__":
    coll = db.collection("fish")
    fish = coll.stream()

    for f in fish:
        d = f.to_dict()
        with st.container(border=True):
            st.header(f":material/pin_drop: {d["address"]}")
            st.write(str(d["date"] + " " + d["hour"]))
            st.image(d["photo"])
