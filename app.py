import streamlit as st

st.set_page_config(
    page_title="Aura AI",
    page_icon="🤖"
)

st.title("Aura AI 🤖")
st.write("Public test version (max 5 users)")

user_input = st.text_input("Yahan likho jo Aura se poochna hai:")

if user_input:
    st.write("Aura ka jawab:")
    st.write("AI next step mein connect hogi 😎")
