import streamlit as st
import time
from datetime import datetime, timedelta

def init_session():
    """Initialize session state variables if they don't exist"""
    if "init" not in st.session_state:
        st.session_state.init = True
        st.session_state.auth_time = time.time()
        
        # Authentication state
        if "user_authenticated" not in st.session_state:
            st.session_state.user_authenticated = False
        if "user_token" not in st.session_state:
            st.session_state.user_token = None
        if "user_id" not in st.session_state:
            st.session_state.user_id = None
        if "username" not in st.session_state:
            st.session_state.username = None
            
        # Problem solving state
        if "current_problem" not in st.session_state:
            st.session_state.current_problem = None
        if "current_solution" not in st.session_state:
            st.session_state.current_solution = None


def check_token_expiry():
    """Check if the authentication token has expired (30 minutes)"""
    if "auth_time" in st.session_state and st.session_state.user_authenticated:
        current_time = time.time()
        # If more than 30 minutes have passed, log the user out
        if current_time - st.session_state.auth_time > 30 * 60:
            logout()
            st.warning("Your session has expired. Please log in again.")
            return False
        # Refresh the auth time if still active
        st.session_state.auth_time = current_time
    return True


def logout():
    """Log out the current user"""
    st.session_state.user_authenticated = False
    st.session_state.user_token = None
    st.session_state.user_id = None
    st.session_state.username = None