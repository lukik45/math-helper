import streamlit as st
import requests
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent directory to path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.session import check_login_status
from utils.api import API_URL

# Page config
st.set_page_config(
    page_title="AI Math Tutor - Progress",
    page_icon="📊",
    layout="wide"
)

# Initialize session state if needed
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Format datetime
def format_datetime(dt_str):
    if not dt_str:
        return "Never"
    
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return dt_str

# Check login status
if not check_login_status():
    st.warning("Please log in to view your progress.")
    if st.button("Go to Login"):
        st.switch_page("pages/Home.py")
else:
    st.title("Your Learning Progress")
    
    # Get progress data
    with st.spinner("Loading your progress..."):
        try:
            response = requests.get(
                f"{API_URL}/api/progress/{st.session_state.user_id}",
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
            
            if response.status_code == 200:
                progress_data = response.json()
                
                # Display summary metrics
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
                
                # Create DataFrame for goals
                if progress_data.get("goal_progress"):
                    df = pd.DataFrame(progress_data["goal_progress"])
                    
                    # Add mastery level categories
                    def mastery_category(level):
                        if level >= 0.8:
                            return "Mastered"
                        elif level >= 0.5:
                            return "Developing"
                        else:
                            return "Struggling"
                    
                    df["mastery_category"] = df["mastery_level"].apply(mastery_category)
                    df["last_practiced_formatted"] = df["last_practiced"].apply(format_datetime)
                    
                    # Display goal progress table
                    st.markdown("### Goal Progress")
                    
                    # Mastery level chart
                    if not df.empty:
                        st.markdown("#### Mastery Level Distribution")
                        fig, ax = plt.subplots(figsize=(10, 5))
                        
                        # Count goals in each category
                        counts = df["mastery_category"].value_counts()
                        
                        # Create bar chart
                        ax.bar(
                            counts.index,
                            counts.values,
                            color=["#2ecc71", "#f39c12", "#e74c3c"]
                        )
                        
                        ax.set_ylabel("Number of Goals")
                        ax.set_title("Goal Mastery Distribution")
                        
                        # Display the chart
                        st.pyplot(fig)
                    
                    # Table with goal progress
                    st.markdown("#### Detailed Goal Progress")
                    
                    # Sort by mastery level
                    df_sorted = df.sort_values("mastery_level", ascending=False)
                    
                    # Display as table
                    st.dataframe(
                        df_sorted[["goal_description", "mastery_level", "attempts_count", 
                                "successful_attempts", "last_practiced_formatted", "mastery_category"]]
                        .rename(columns={
                            "goal_description": "Goal",
                            "mastery_level": "Mastery Level",
                            "attempts_count": "Attempts",
                            "successful_attempts": "Successful",
                            "last_practiced_formatted": "Last Practiced",
                            "mastery_category": "Status"
                        }),
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Recommended focus areas
                    st.markdown("### Recommended Focus Areas")
                    
                    struggling_goals = df[df["mastery_level"] < 0.5]
                    
                    if not struggling_goals.empty:
                        for _, goal in struggling_goals.iterrows():
                            st.markdown(f"- {goal['goal_description']} (Current mastery: {goal['mastery_level']:.1%})")
                    else:
                        st.success("Great job! You don't have any struggling areas right now.")
                    
                    # Recommended problems
                    st.markdown("### Recommended Practice Problems")
                    
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
                                st.info("No recommended problems available yet.")
                    except:
                        st.info("No recommended problems available yet.")
                else:
                    st.info("You haven't worked on any goals yet. Start solving problems to track your progress!")
            else:
                st.error("Failed to load progress data. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Start solving some problems to track your progress!")
    
    # Navigation
    if st.button("Back to Home"):
        st.switch_page("pages/Home.py")