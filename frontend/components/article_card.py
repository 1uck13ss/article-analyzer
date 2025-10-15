
import streamlit as st

def render_article_card(metadata, summary, mode):
    if mode == 'dashboard':
        summary = summary[:300]
        if len(summary) <= 300:
            summary += "..."
    with st.container():
        st.markdown(f"### {metadata['title']}")
        st.markdown(summary)    