import streamlit as st
from frontend.components.authentication import init_auth_state, login_form
from frontend.utils.api import get_profile

# Set page configuration
st.set_page_config(
    page_title="AI Math Tutor - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication state
init_auth_state()

# Display title
st.title("🧮 AI Math Tutor")
st.write("An intelligent learning platform for mathematics")

# Sidebar with authentication
with st.sidebar:
    st.header("User Account")
    is_authenticated = login_form()
    
    if is_authenticated:
        st.success("✅ Logged in successfully")
        
        # Get user profile
        profile = get_profile()
        if profile:
            st.write(f"👋 Welcome back, **{profile['username']}**!")
            if profile.get('grade_level'):
                st.write(f"📚 Grade level: {profile['grade_level']}")

# Main page content
if st.session_state.get("user_authenticated", False):
    st.header("Welcome to the AI Math Tutor")
    
    st.markdown("""
    This application helps you solve math problems and learn by connecting solutions to curriculum requirements.
    
    ### Features:
    - Submit math problems and get step-by-step solutions
    - Track your progress and identify knowledge gaps
    - Get personalized problem recommendations
    - Learn math concepts aligned with the curriculum
    
    ### Get Started:
    1. Go to the **Problem Solver** page to solve a math problem
    2. Check your **Progress** to see your learning statistics
    3. Explore recommended problems based on your areas of need
    """)
    
    # Quick access buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧮 Solve a Problem"):
            st.switch_page("pages/2_🧮_Problem_Solver.py")
    with col2:
        if st.button("📊 View Progress"):
            st.switch_page("pages/3_📊_Progress.py")
    with col3:
        if st.button("⚙️ Settings"):
            st.switch_page("pages/4_⚙️_Settings.py")
    
else:
    st.info("👆 Please log in or register to use the AI Math Tutor")
    
    # Introduction for non-logged in users
    st.markdown("""
    ## What is AI Math Tutor?
    
    AI Math Tutor is an intelligent learning platform designed specifically for students struggling with mathematics. 
    The application connects problem-solving steps with curriculum requirements, helping students identify and 
    address knowledge gaps through personalized learning.
    
    ### Core Value Proposition:
    - **Step-by-step guided learning** with hints before solutions
    - **Curriculum-aligned explanations** mapped to the educational curriculum
    - **Knowledge gap identification** through interactive problem-solving
    - **Personalized learning experience** that adapts to student difficulties
    
    Register now to get started on your math learning journey!
    """)