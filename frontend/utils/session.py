import streamlit as st

def check_login_status():
    """
    Check if the user is logged in.
    Returns True if logged in, False otherwise.
    """
    # Ensure we have consistent session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        
    # If token exists but logged_in flag is False, correct it
    if "token" in st.session_state and not st.session_state.logged_in:
        st.session_state.logged_in = True
        
    return st.session_state.get("logged_in", False)

def logout():
    """
    Log out the user by clearing session state.
    """
    for key in ["user_id", "token", "logged_in", "username", "grade_level", 
                "current_solution", "selected_problem"]:
        if key in st.session_state:
            del st.session_state[key]