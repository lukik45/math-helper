import streamlit as st
import requests
import json
from datetime import datetime, timedelta

from frontend.utils.api import get_api_url

def init_auth_state():
    """Initialize authentication state if not already present"""
    if "user_authenticated" not in st.session_state:
        st.session_state.user_authenticated = False
    if "user_token" not in st.session_state:
        st.session_state.user_token = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None

def login_form():
    """Display login form and handle authentication"""
    init_auth_state()
    
    # If user is already logged in, show logout option
    if st.session_state.user_authenticated:
        st.write(f"Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            logout()
        return True

    # Display login/register tabs
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                success, message = authenticate_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Register")
            new_username = st.text_input("Username")
            email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            grade_level = st.number_input("Grade Level", min_value=1, max_value=12, value=8)
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if new_password != confirm_password:
                    st.error("Passwords don't match")
                elif not new_username or not email or not new_password:
                    st.error("All fields are required")
                else:
                    success, message = register_user(new_username, email, new_password, grade_level)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    return st.session_state.user_authenticated

def authenticate_user(username, password):
    """Authenticate user with the API"""
    try:
        response = requests.post(
            f"{get_api_url()}/api/auth/login-json",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.user_token = data["access_token"]
            st.session_state.user_id = data["user_id"]
            st.session_state.username = username
            st.session_state.user_authenticated = True
            return True, "Login successful!"
        else:
            error_msg = response.json().get("detail", "Login failed")
            return False, f"Error: {error_msg}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def register_user(username, email, password, grade_level):
    """Register a new user with the API"""
    try:
        response = requests.post(
            f"{get_api_url()}/api/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password,
                "grade_level": grade_level
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.user_token = data["access_token"]
            st.session_state.user_id = data["user_id"]
            st.session_state.username = username
            st.session_state.user_authenticated = True
            return True, "Registration successful!"
        else:
            error_msg = response.json().get("detail", "Registration failed")
            return False, f"Error: {error_msg}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def logout():
    """Log out the current user"""
    st.session_state.user_authenticated = False
    st.session_state.user_token = None
    st.session_state.user_id = None
    st.session_state.username = None
    st.success("Logged out successfully")

def require_auth():
    """Require authentication to access a page"""
    init_auth_state()
    if not st.session_state.user_authenticated:
        st.warning("Please log in to access this page")
        login_form()
        st.stop()  # Stop execution if not authenticated