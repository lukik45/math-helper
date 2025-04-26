import streamlit as st
import requests
import os
import sys
import json

# Add parent directory to path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.session import check_login_status
from utils.api import API_URL

# Page config
st.set_page_config(
    page_title="AI Math Tutor - Problem Solver",
    page_icon="🧮",
    layout="wide"
)

# Initialize session state if needed
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Function to update step progress
def update_progress(problem_id, step_id, solved_with_hint):
    response = requests.post(
        f"{API_URL}/api/problems/{problem_id}/steps/{step_id}/progress",
        json={"solved_with_hint": solved_with_hint},
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    
    if response.status_code == 200:
        st.success("Progress updated!")
    else:
        st.error("Failed to update progress.")

# Check login status
if not check_login_status():
    st.warning("Please log in to access the problem solver.")
    if st.button("Go to Login"):
        st.switch_page("pages/Home.py")
else:
    st.title("Math Problem Solver")
    
    # Debug area (expandable)
    debug_expander = st.expander("Debug Information (Expand if you encounter problems)", expanded=False)
    
    # Input form for problem
    if "current_solution" not in st.session_state:
        with st.form("problem_form"):
            # If a problem was selected from recommendations
            initial_problem = st.session_state.get("selected_problem", "")
            if "selected_problem" in st.session_state:
                del st.session_state.selected_problem
                
            problem_text = st.text_area(
                "Enter your math problem:",
                value=initial_problem,
                height=150,
                placeholder="Example: Solve 2x + 5 = 13"
            )
            
            subject_area = st.selectbox(
                "Subject Area (optional)", 
                ["", "Algebra", "Geometry", "Arithmetic", "Statistics", "Trigonometry"]
            )
            
            submit_button = st.form_submit_button("Solve")
            
            if submit_button and problem_text:
                with st.spinner("Generating solution..."):
                    try:
                        # Prepare the request payload
                        payload = {
                            "problem_text": problem_text,
                            "subject_area": subject_area if subject_area else None,
                            "grade_level": st.session_state.get("grade_level")
                        }
                        
                        # Log request details
                        with debug_expander:
                            st.write("Request URL:", f"{API_URL}/api/problems/solve")
                            st.write("Request Payload:", payload)
                            st.write("Token (partial):", f"{st.session_state.token[:10]}..." if st.session_state.token else "None")
                        
                        # Make the API request
                        response = requests.post(
                            f"{API_URL}/api/problems/solve",
                            json=payload,
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        
                        # Log response details
                        with debug_expander:
                            st.write("Response Status:", response.status_code)
                            try:
                                st.write("Response Headers:", dict(response.headers))
                                st.write("Response Content (preview):", response.text[:500] + "..." if len(response.text) > 500 else response.text)
                            except:
                                st.write("Error processing response details")
                        
                        if response.status_code == 200:
                            st.session_state.current_solution = response.json()
                            st.rerun()
                        else:
                            error_message = "Error generating solution. Please try again."
                            try:
                                error_data = response.json()
                                if "detail" in error_data:
                                    error_message = f"Error: {error_data['detail']}"
                            except:
                                pass
                            
                            st.error(error_message)
                            with debug_expander:
                                st.error(f"Full error response: {response.text}")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        with debug_expander:
                            st.exception(e)
    else:
        # Display solution
        solution = st.session_state.current_solution
        
        st.markdown(f"### Problem: {solution['problem_text']}")
        
        if solution.get("subject_area"):
            st.markdown(f"*Subject Area: {solution['subject_area']}*")
        
        # New problem button
        if st.button("Solve Another Problem"):
            if "current_solution" in st.session_state:
                del st.session_state.current_solution
            st.rerun()
        
        # Display solution steps
        st.markdown("## Step-by-Step Solution")
        
        for i, step in enumerate(solution['solution_steps']):
            with st.expander(f"Step {i+1}: {step['description']}", expanded=True):
                tab1, tab2, tab3 = st.tabs(["Hint", "Solution", "Curriculum"])
                
                with tab1:
                    st.markdown(step['hint'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("I solved it with the hint", key=f"hint_{i}"):
                            update_progress(solution['problem_id'], step['id'], True)
                            
                    with col2:
                        if st.button("Show me the solution", key=f"show_{i}"):
                            st.session_state[f"show_solution_{i}"] = True
                            st.rerun()
                
                with tab2:
                    if st.session_state.get(f"show_solution_{i}", False):
                        st.markdown(step['solution'])
                        
                        if st.button("I understand now", key=f"understand_{i}"):
                            update_progress(solution['problem_id'], step['id'], False)
                    else:
                        st.info("Try using the hint first!")
                
                with tab3:
                    st.markdown("This step relates to these curriculum goals:")

                    if step.get('curriculum_goals'):
                        for idx, goal in enumerate(step['curriculum_goals']):
                            st.markdown(f"- **{goal['description']}**")
                            
                            if goal.get('requirements'):
                                show_reqs = st.checkbox(f"Show Related Requirements for Goal {idx+1}", key=f"req_toggle_{i}_{idx}")
                                if show_reqs:
                                    for req in goal['requirements']:
                                        st.markdown(f"    • {req['description']}")
                    else:
                        st.info("No curriculum goals linked to this step yet.")

                    
    # Navigation
    if st.button("Back to Home"):
        st.switch_page("pages/Home.py")