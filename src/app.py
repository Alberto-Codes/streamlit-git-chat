# Import required libraries
import requests
import streamlit as st

# Set the title of the application
st.title("URL Status Checker")

# Get URL input from user
url = st.text_input("Enter a URL to check:", "")

# Check status of URL
if st.button("Check URL Status"):
    if url != "":
        try:
            response = requests.get(url)
            st.write("Status Code:", response.status_code)
        except Exception as e:
            st.write(f"Error: {e}")
    else:
        st.write("Please enter a URL to check.")
