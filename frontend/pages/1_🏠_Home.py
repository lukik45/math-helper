import streamlit as st
import requests
import os

# Session state handling for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "token" not in st.session_state:
    st.session_state.token = None

# Set page config
st.set_page_config(
    page_title="AI Math Tutor",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Login page
def login_page():
    st.title("Math Tutor Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                try:
                    response = requests.post(
                        f"{API_URL}/api/auth/login",
                        json={"username": username, "password": password}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.user_id = data["user_id"]
                        st.session_state.token = data["access_token"]
                        st.session_state.logged_in = True
                        st.experimental_rerun()
                    else:
                        st.error("Login failed. Please check your credentials.")
                except Exception as e:
                    st.error(f"Error connecting to the server: {str(e)}")
    
    with tab2:
        with st.form("register_form"):
            username = st.text_input("Username", key="register_username")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            grade_level = st.slider("Grade Level", 1, 12, 8)
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                try:
                    response = requests.post(
                        f"{API_URL}/api/auth/register",
                        json={
                            "username": username, 
                            "email": email, 
                            "password": password,
                            "grade_level": grade_level
                        }
                    )
                    
                    if response.status_code == 201:
                        st.success("Registration successful! Please log in.")
                    else:
                        st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error connecting to the server: {str(e)}")

# Home page for logged-in users
def home_page():
    st.title("Welcome to AI Math Tutor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("How it works")
        st.write("""
        1. **Enter your math problem** on the Problem Solver page
        2. **Get step-by-step guidance** with hints before solutions
        3. **Track your progress** and see which areas need more practice
        4. **Receive personalized recommendations** based on your performance
        """)
        
        st.button("Start Solving Problems", on_click=lambda: st.switch_page("pages/2_🧮_Problem_Solver.py"))
    
    with col2:
        st.header("Your Learning Stats")
        st.info("Connect to see your learning statistics here!")
        
        # Placeholder for future stats
        st.metric(label="Problems Solved", value="0")
        st.metric(label="Mastery Level", value="0%")
    
    st.header("Sample Problems")
    with st.expander("Find the value of x: 2x + 5 = 15"):
        st.write("Try solving this linear equation on the Problem Solver page!")
    
    with st.expander("Calculate the area of a circle with radius 4cm"):
        st.write("Test your geometry knowledge with this problem!")

# Display appropriate page based on login status
if st.session_state.logged_in:
    home_page()
else:
    login_page()

# Simple sidebar for navigation
with st.sidebar:
    st.title("AI Math Tutor")
    
    if st.session_state.logged_in:
        st.success("Logged in")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.token = None
            st.experimental_rerun()
    else:
        st.info("Please log in to continue")