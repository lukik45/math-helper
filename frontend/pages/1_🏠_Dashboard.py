import streamlit as st
from frontend.components.authentication import require_auth
from frontend.utils.api import get_profile
from frontend.utils.session import init_session, check_token_expiry

# Set page configuration
st.set_page_config(
    page_title="AI Math Tutor - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session and check authentication
init_session()
check_token_expiry()

# Authentication required for this page
require_auth()

# Display title
st.title("🏠 Home Page")
st.write("Welcome to your personalized learning dashboard")

# Get user profile
profile = get_profile()

# Display user information
if profile:
    st.header(f"Hello, {profile['username']}!")
    
    # Display dashboard stats (these would come from the API in a real implementation)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Problems Solved", value="12")
    with col2:
        st.metric(label="Mastery Level", value="68%")
    with col3:
        st.metric(label="Streak", value="3 days")
    
    # Recent activity
    st.subheader("Recent Activity")
    st.write("Here's what you've been working on:")
    
    # Sample activity data (would come from the API)
    activity_data = [
        {"type": "Problem", "name": "Solve for x: 2x + 5 = 13", "date": "Today", "result": "Completed"},
        {"type": "Concept", "name": "Linear Equations", "date": "Yesterday", "result": "70% Mastery"},
        {"type": "Problem", "name": "Find the area of a circle with radius 4", "date": "2 days ago", "result": "Completed"}
    ]
    
    for item in activity_data:
        st.write(f"**{item['type']}**: {item['name']} - {item['date']} - {item['result']}")
    
    # Recommended practice
    st.subheader("Recommended Practice")
    st.write("Based on your progress, here are some recommended problems:")
    
    # Sample recommendations (would come from the API)
    recommendations = [
        "Practice more problems with linear equations",
        "Review basic geometry concepts",
        "Try some word problems with algebraic expressions"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Solve a New Problem"):
            st.switch_page("pages/2_🧮_Problem_Solver.py")
    with col2:
        if st.button("View Detailed Progress"):
            st.switch_page("pages/3_📊_Progress.py")
else:
    st.error("Could not retrieve user profile. Please try logging in again.")