import streamlit as st
from frontend.components.authentication import require_auth
from frontend.utils.api import api_post, get_api_url
from frontend.utils.session import init_session, check_token_expiry
from frontend.components.problem_input import display_problem_form

# Set page config
st.set_page_config(
    page_title="Problem Solver - AI Math Tutor",
    page_icon="🧮",
    layout="wide"
)

# Initialize session and check authentication
init_session()
check_token_expiry()

# Authentication required for this page
require_auth()

# Page header
st.title("🧮 Problem Solver")
st.write("Submit a math problem and get a step-by-step solution")

# Problem input form
if "current_solution" not in st.session_state or st.session_state.current_solution is None:
    # Show problem input form when no solution is being displayed
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
            with st.spinner("Generating solution..."):
                # This would normally call the API
                st.info("In a production environment, this would call the FastAPI backend")
                st.session_state.current_problem = problem_text
                
                # For demo purposes, create a mock solution
                st.session_state.current_solution = {
                    "problem_id": "mock_id",
                    "problem_text": problem_text,
                    "subject_area": subject_area if subject_area else "General",
                    "solution_steps": [
                        {
                            "id": "step1",
                            "step_number": 1,
                            "description": "Understand what we're looking for",
                            "hint": "We need to isolate the variable x by moving all other terms to the right side",
                            "solution": "We have the equation 2x + 5 = 13 and need to solve for x.",
                            "curriculum_goals": [
                                {
                                    "id": "goal1",
                                    "description": "Solve linear equations in one variable",
                                    "requirements": [
                                        {"description": "Understand and apply properties of equality"}
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "step2",
                            "step_number": 2,
                            "description": "Subtract 5 from both sides",
                            "hint": "To isolate the x term, we need to get rid of the constant term by subtracting 5 from both sides",
                            "solution": "2x + 5 - 5 = 13 - 5\n2x = 8",
                            "curriculum_goals": [
                                {
                                    "id": "goal2",
                                    "description": "Apply operations on both sides of equations",
                                    "requirements": [
                                        {"description": "Use additive property of equality"}
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "step3",
                            "step_number": 3,
                            "description": "Divide both sides by 2",
                            "hint": "To find the value of x, divide both sides by the coefficient of x",
                            "solution": "2x ÷ 2 = 8 ÷ 2\nx = 4",
                            "curriculum_goals": [
                                {
                                    "id": "goal3",
                                    "description": "Use multiplication and division to solve equations",
                                    "requirements": [
                                        {"description": "Apply multiplicative property of equality"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
                st.success("Solution generated!")
                st.rerun()

# Display solution if available
if "current_solution" in st.session_state and st.session_state.current_solution:
    solution = st.session_state.current_solution
    
    # Button to start a new problem
    if st.button("Solve Another Problem"):
        st.session_state.current_solution = None
        st.rerun()
    
    # Display the problem
    st.header("Problem")
    st.write(solution["problem_text"])
    st.write(f"Subject: {solution['subject_area']}")
    
    # Display solution steps
    st.header("Step-by-Step Solution")
    
    for i, step in enumerate(solution["solution_steps"]):
        with st.expander(f"Step {i+1}: {step['description']}", expanded=True):
            tab1, tab2, tab3 = st.tabs(["Hint", "Solution", "Curriculum"])
            
            with tab1:
                st.write(step['hint'])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("I solved it with the hint", key=f"hint_{i}"):
                        st.success("Great job! Your progress has been updated.")
                        
                with col2:
                    if st.button("Show me the solution", key=f"show_{i}"):
                        st.session_state[f"show_solution_{i}"] = True
                        st.rerun()
            
            with tab2:
                if st.session_state.get(f"show_solution_{i}", False):
                    st.write(step['solution'])
                    
                    if st.button("I understand now", key=f"understand_{i}"):
                        st.success("Progress updated. Let's continue to the next step!")
                else:
                    st.info("Try using the hint first!")
            
            with tab3:
                st.write("This step relates to these curriculum goals:")
                for goal in step['curriculum_goals']:
                    st.write(f"- {goal['description']}")
                    with st.expander("Related Requirements"):
                        for req in goal['requirements']:
                            st.write(f"• {req['description']}")