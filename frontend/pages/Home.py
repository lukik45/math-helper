import streamlit as st
import requests
import os
import sys

# Add parent directory to path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.session import check_login_status, logout
from utils.api import API_URL

# Page config
st.set_page_config(
    page_title="AI Math Tutor - Home",
    page_icon="🏠",
    layout="wide"
)

# Initialize session state for persistent login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Check login status
if not check_login_status():
    st.warning("Please log in to access the application")
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                # Call login API
                response = requests.post(
                    f"{API_URL}/api/auth/login",
                    json={"username": username, "password": password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.user_id = data["user_id"]
                    st.session_state.token = data["access_token"]
                    st.session_state.logged_in = True
                    
                    # Get user info
                    user_response = requests.get(
                        f"{API_URL}/api/auth/user",
                        headers={"Authorization": f"Bearer {data['access_token']}"}
                    )
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        st.session_state.username = user_data["username"]
                        st.session_state.grade_level = user_data.get("grade_level")
                    
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Login failed. Please check your credentials.")
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Register")
            new_username = st.text_input("Username", key="reg_username")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Password", type="password", key="reg_password")
            grade_level = st.number_input("Grade Level (Optional)", min_value=1, max_value=12, value=7)
            
            submit_button = st.form_submit_button("Register")
            
            if submit_button:
                # Call registration API
                response = requests.post(
                    f"{API_URL}/api/auth/register",
                    json={
                        "username": new_username,
                        "email": new_email,
                        "password": new_password,
                        "grade_level": grade_level
                    }
                )
                
                if response.status_code == 200:
                    st.success("Registration successful! Please login.")
                else:
                    error_detail = "Registration failed."
                    if response.status_code == 400:
                        try:
                            error_detail = response.json().get("detail", "Registration failed.")
                        except:
                            pass
                    st.error(error_detail)
else:
    # Show home page content
    st.title("AI Math Tutor")
    st.markdown("### Welcome to your personalized math learning assistant!")
    
    # Get user stats
    try:
        progress_response = requests.get(
            f"{API_URL}/api/progress/{st.session_state.user_id}",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        
        if progress_response.status_code == 200:
            progress_data = progress_response.json()
            
            # Display user stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Goals", progress_data.get("total_goals", 0))
            
            with col2:
                st.metric("Mastered Goals", progress_data.get("mastered_goals", 0))
            
            with col3:
                st.metric("Struggling Goals", progress_data.get("struggling_goals", 0))
            
            with col4:
                average_mastery = progress_data.get("average_mastery", 0)
                st.metric("Average Mastery", f"{average_mastery:.1%}")
    except:
        st.info("No progress data available yet. Start solving problems to track your progress!")
    
    # Display quick access cards
    st.markdown("### Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Solve a Problem")
        st.write("Enter a math problem and get a step-by-step solution with curriculum connections.")
        if st.button("Solve Problem", key="solve_problem_btn", use_container_width=True):
            st.switch_page("pages/Problem_Solver.py")
    
    with col2:
        st.markdown("#### Check Your Progress")
        st.write("View your learning progress and see which areas need more practice.")
        if st.button("View Progress", key="view_progress_btn", use_container_width=True):
            st.switch_page("pages/Progress.py")
    
    # Recommended Problems
    st.markdown("### Recommended Problems")
    
    try:
        recommend_response = requests.get(
            f"{API_URL}/api/progress/recommend/{st.session_state.user_id}",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        
        if recommend_response.status_code == 200:
            problems = recommend_response.json()
            
            if problems:
                for problem in problems:
                    with st.expander(problem.get("text", "Problem")):
                        st.write(f"Subject Area: {problem.get('subject_area', 'Not specified')}")
                        st.write("Targeted Goals:")
                        for i, goal in enumerate(problem.get("goal_descriptions", [])):
                            st.write(f"  {i+1}. {goal}")
                        
                        if st.button("Solve This Problem", key=f"solve_{problem.get('id')}"):
                            st.session_state.selected_problem = problem.get("text")
                            st.switch_page("pages/Problem_Solver.py")
            else:
                st.info("No recommended problems available yet. Solve some problems to get personalized recommendations!")
    except:
        st.info("Solve some problems to get personalized recommendations!")
    
    # Logout button
    if st.button("Logout"):
        logout()
        st.rerun()