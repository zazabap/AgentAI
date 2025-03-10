import streamlit as st
import requests

# Define API endpoints
RUN_TASK_URL = "http://localhost:8000/run-task"
VALIDATE_URL = "http://localhost:8000/validate-data"
CONVERSATIONS_URL = "http://localhost:8000/conversations"  # New endpoint for conversation logs

def get_task_response(task):
    try:
        with st.spinner("Processing your task..."):
            response = requests.get(RUN_TASK_URL, params={"task": task})
            response.raise_for_status()
            # Expecting the endpoint to return a dict with "result" key containing suggestion and result.
            data = response.json().get("result", {})
        return data
    except Exception as e:
        st.error(f"Error processing task: {e}")
        return None

def get_validation(file_path):
    try:
        with st.spinner("Validating file..."):
            response = requests.get(VALIDATE_URL, params={"file_path": file_path})
            response.raise_for_status()
            data = response.json().get("validation", {})
        return data
    except Exception as e:
        st.error(f"Error validating file: {e}")
        return None

def get_conversations():
    try:
        with st.spinner("Loading conversation logs..."):
            response = requests.get(CONVERSATIONS_URL)
            response.raise_for_status()
            data = response.json().get("conversations", [])
        return data
    except Exception as e:
        st.error(f"Error loading conversation logs: {e}")
        return []

st.title("AI Automation Agent")

# Create tabs for different functionalities
tabs = st.tabs(["Run Task", "Validate Data", "Conversation History"])

with tabs[0]:
    st.header("Task Automation")
    task_input = st.text_input("Enter a task (e.g., 'process my files')", key="task_input")
    if st.button("Run Task", key="run_task_button"):
        if task_input:
            result_data = get_task_response(task_input)
            if result_data:
                suggestion = result_data.get("suggestion", "No suggestion provided.")
                result_text = result_data.get("result", "No result provided.")
                st.subheader("Suggestion")
                st.text_area("Suggestion", suggestion, height=150)
                st.subheader("Result")
                st.text_area("Result", result_text, height=150)
        else:
            st.warning("Please enter a task.")

with tabs[1]:
    st.header("Data Validation")
    file_path = st.text_input("Enter file path to validate (e.g., '/app/data/input/sample.txt')", key="file_path_input")
    if st.button("Validate Data", key="validate_data_button"):
        if file_path:
            validation_data = get_validation(file_path)
            if validation_data:
                st.subheader("Validation Output")
                st.json(validation_data)
        else:
            st.warning("Please enter a file path.")

with tabs[2]:
    st.header("Conversation History")
    if st.button("Refresh Logs", key="refresh_logs"):
        conversations = get_conversations()
        if conversations:
            for convo in conversations:
                st.markdown(f"**Timestamp:** {convo.get('timestamp')}")
                st.markdown(f"**Task:** {convo.get('task')}")
                st.markdown(f"**Suggestion:** {convo.get('suggestion')}")
                st.markdown(f"**Result:** {convo.get('result')}")
                st.markdown("---")
        else:
            st.info("No conversation logs found.")
