# Import required libraries
import os
import subprocess

import requests
import streamlit as st


def clone_repo(repo_url, clone_dir):
    """
    Clones a Git repository into a specific directory.

    Parameters:
    repo_url (str): The URL of the Git repository.
    clone_dir (str): The path to the directory where the repository should be cloned.

    Returns:
    None
    """
    # Extract the repository name from the URL
    repo_name = repo_url.split("/")[-1].split(".")[0]

    # Form the full path to the clone directory
    full_clone_dir = os.path.join(clone_dir, repo_name)

    # Clone the repository
    subprocess.run(["git", "clone", repo_url, full_clone_dir])


# Set the title of the application
st.title("GitHub Repository Status Checker")

# Get URL input from user
url = st.text_input(
    "Enter a GitHub repository URL or a `gh repo clone` command to check:", ""
)


# Function to convert SSH URLs to HTTPS
def ssh_to_https(ssh_url):
    prefix = "https://"
    service = "github.com/"
    ssh_url = ssh_url.replace("git@github.com:", service)
    return prefix + ssh_url


# Function to convert 'gh repo clone' command to HTTPS
def gh_command_to_https(gh_command):
    parts = gh_command.split()
    if len(parts) != 4 or parts[0] != "gh" or parts[1] != "repo" or parts[2] != "clone":
        return None
    return f"https://github.com/{parts[3]}"


# Function to make HTTP request and return status code
def check_url_status(url):
    try:
        response = requests.get(url)
        st.write("Status Code:", response.status_code)
        return response.status_code
    except Exception as e:
        st.write(f"Error: {e}")
        return None


# Check status of URL
if st.button("Check URL Status"):
    if url != "":
        if url.startswith("gh repo clone"):
            url = gh_command_to_https(url)
            if url is None:
                st.write(
                    "Invalid `gh repo clone` command. Please enter a valid command."
                )
            else:
                status_code = check_url_status(url)
        elif url.startswith("git@"):
            url = ssh_to_https(url)
            status_code = check_url_status(url)
        elif "github.com" in url:
            status_code = check_url_status(url)
        else:
            st.write("Invalid GitHub URL. Please enter a valid GitHub repository URL.")

        if status_code == 200:
            clone_dir = "./data/"
            clone_repo(url, clone_dir)
    else:
        st.write("Please enter a URL or a `gh repo clone` command to check.")
