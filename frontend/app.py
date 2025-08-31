import streamlit as st
import requests
from components.article_card import render_article_card
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")  

st.title("📚 Reading Tracker")
url = st.text_input("Paste article URL")
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "dashboard"
if "current_article" not in st.session_state:
    st.session_state.current_article = None

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Submit"):
        with st.spinner("Processing..."):
            try:
                response = requests.post(f"{API_BASE}/submit", json={"user_id": "demo", "content": url})
                response.raise_for_status()
                content = response.json()
                st.session_state.current_article = content
                print(content)
                st.session_state.view_mode = "single"
            except requests.exceptions.RequestException as e:
                st.error(f"Ingestion failed: {e}")

if st.session_state.view_mode == "single":
    with col2:
        if st.button("← Back to Dashboard"):
            st.session_state.view_mode = "dashboard"

if st.session_state.view_mode == "dashboard":
    response = requests.get(f"{API_BASE}/retrieve")
    response.raise_for_status()
    retrieved = response.json()

    st.markdown("""
    <hr style='margin-top: 10px; margin-bottom: 20px;'>
    <h3 style='text-align: center;'>Recent Submissions</h3>
    """, unsafe_allow_html=True)


    articles_to_show = retrieved[:3]
    cols = st.columns(len(articles_to_show))

    for i, article in enumerate(articles_to_show):
        with cols[i]:
            render_article_card(article["metadata"], article["summary"], st.session_state.view_mode)


elif st.session_state.view_mode == "single":
    article = st.session_state.current_article
    render_article_card(article["metadata"], article["summary"], st.session_state.view_mode)
