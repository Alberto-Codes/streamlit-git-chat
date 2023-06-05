# Import required libraries
import streamlit as st
import requests

# Set the title of the application
st.title('GitHub Repository Status Checker')

# Get URL input from user
url = st.text_input('Enter a GitHub repository URL or a `gh repo clone` command to check:', '')

# Function to convert SSH URLs to HTTPS
def ssh_to_https(ssh_url):
    prefix = "https://"
    service = "github.com/"
    ssh_url = ssh_url.replace("git@github.com:", service)
    return prefix + ssh_url

# Function to convert 'gh repo clone' command to HTTPS
def gh_command_to_https(gh_command):
    parts = gh_command.split()
    if len(parts) != 4 or parts[0] != 'gh' or parts[1] != 'repo' or parts[2] != 'clone':
        return None
    return f'https://github.com/{parts[3]}'

# Check status of URL
if st.button('Check URL Status'):
    if url != '':
        if url.startswith('gh repo clone'):
            url = gh_command_to_https(url)
            if url is None:
                st.write('Invalid `gh repo clone` command. Please enter a valid command.')
            else:
                try:
                    response = requests.get(url)
                    st.write('Status Code:', response.status_code)
                except Exception as e:
                    st.write(f'Error: {e}')
        elif url.startswith('git@'):
            url = ssh_to_https(url)
            try:
                response = requests.get(url)
                st.write('Status Code:', response.status_code)
            except Exception as e:
                st.write(f'Error: {e}')
        elif 'github.com' in url:
            try:
                response = requests.get(url)
                st.write('Status Code:', response.status_code)
            except Exception as e:
                st.write(f'Error: {e}')
        else:
            st.write('Invalid GitHub URL. Please enter a valid GitHub repository URL.')
    else:
        st.write('Please enter a URL or a `gh repo clone` command to check.')
