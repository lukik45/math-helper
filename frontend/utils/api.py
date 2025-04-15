import streamlit as st
import requests
import json
import os

def get_api_url():
    """Get the API URL from environment variable or use default"""
    return os.environ.get("API_URL", "http://localhost:8000")

def get_auth_header():
    """Get the authorization header with the token"""
    if "user_token" in st.session_state and st.session_state.user_token:
        return {"Authorization": f"Bearer {st.session_state.user_token}"}
    return {}

def get_profile():
    """Get the user profile from the API"""
    try:
        response = requests.get(
            f"{get_api_url()}/api/auth/user",
            headers=get_auth_header()
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching profile: {str(e)}")
        return None

def api_post(endpoint, data):
    """Make a POST request to the API with authentication"""
    try:
        response = requests.post(
            f"{get_api_url()}{endpoint}",
            json=data,
            headers=get_auth_header()
        )
        return response.json(), response.status_code
    except Exception as e:
        st.error(f"API error: {str(e)}")
        return {"error": str(e)}, 500

def api_get(endpoint, params=None):
    """Make a GET request to the API with authentication"""
    try:
        response = requests.get(
            f"{get_api_url()}{endpoint}",
            params=params,
            headers=get_auth_header()
        )
        return response.json(), response.status_code
    except Exception as e:
        st.error(f"API error: {str(e)}")
        return {"error": str(e)}, 500