import streamlit as st
from frontend.utils.api import api_post

def display_problem_form():
    """Display the problem input form"""
    with st.form("problem_form"):
        st.subheader("Enter your math problem")
        problem_text = st.text_area(
            "Type or paste your problem here:",
            height=100,
            placeholder="E.g., Solve for x: 2x + 5 = 13"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            subject_area = st.selectbox(
                "Subject Area (optional)",
                ["", "Algebra", "Geometry", "Arithmetic", "Statistics", "Trigonometry"]
            )
        with col2:
            grade_level = st.slider("Grade Level", 1, 12, 8)
        
        submitted = st.form_submit_button("Solve Problem")
        
        if submitted and problem_text:
            return {
                "problem_text": problem_text,
                "subject_area": subject_area if subject_area else None,
                "grade_level": grade_level
            }
        return None

def solve_problem(problem_data):
    """Call the API to solve the problem"""
    with st.spinner("Generating solution..."):
        response, status_code = api_post(
            "/api/problems/solve",
            problem_data
        )
        
        if status_code == 200:
            st.session_state.current_problem = problem_data["problem_text"]
            st.session_state.current_solution = response
            return True
        else:
            error_msg = response.get("detail", "Error generating solution")
            st.error(f"Error: {error_msg}")
            return False