import streamlit as st

if st.button("Log in"):
    st.login("auth0")
if st.experimental_user.is_logged_in:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.experimental_user.name}!")