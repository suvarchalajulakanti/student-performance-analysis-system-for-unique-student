import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Performance Analysis System")
st.write("Analyze student results and search for individual student details.")

# Load the Excel dataset from the project folder
file_path = Path(__file__).parent / "student data.xlsx"

try:
    df = pd.read_excel(file_path)

    subject_cols = ["s1", "s2", "s3", "s4", "s5", "s6"]
    attendance_col = "attendence"

    required_cols = ["name"] + subject_cols + [attendance_col]

    if not all(col in df.columns for col in required_cols):
        st.error("The Excel file is missing required columns.")
        st.stop()

    # Display the original dataset
    st.subheader("Student Dataset")
    st.dataframe(df, use_container_width=True)

    # User inputs
    st.subheader("Analysis Settings")

    col1, col2 = st.columns(2)

    with col1:
        pass_mark = st.number_input(
            "Pass marks required in each subject",
            min_value=0,
            max_value=100,
            value=35,
            step=1
        )

    with col2:
        min_attendance = st.number_input(
            "Minimum attendance percentage",
            min_value=0.0,
            max_value=100.0,
            value=75.0,
            step=1.0
        )

    # Apply the original analysis logic
    is_pass = (
        (df[subject_cols] >= pass_mark).all(axis=1)
        & (df[attendance_col] >= min_attendance)
    )

    df["Result"] = np.where(is_pass, "pass", "fail")
    df["Average"] = df[subject_cols].mean(axis=1).round(2)

    df["Description"] = df.apply(
        lambda row: (
            f"{row['name']} obtained an average score of "
            f"{row['Average']}% across {len(subject_cols)} subjects "
            f"with an attendance of {row[attendance_col]}%. "
            f"The student has {row['Result']} the requirements."
        ),
        axis=1
    )

    # Display complete results
    st.subheader("Student Performance Results")
    st.dataframe(df, use_container_width=True)

    # Search for a student
    st.subheader("🔍 Search for a Student")

    student_name = st.text_input(
        "Enter the student's name"
    ).strip().lower()

    if student_name:
        matched = df[
            df["name"].astype(str).str.strip().str.lower()
            == student_name
        ]

        if not matched.empty:
            for _, student in matched.iterrows():
                st.subheader(f"Student: {student['name']}")

                details = matched.drop(columns=["Description"])
                st.dataframe(details, use_container_width=True)

                st.markdown("**Performance Description**")
                st.info(student["Description"])
        else:
            st.warning("No student found with that name.")

    # Download analyzed results
    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Student Results (CSV)",
        data=csv_data,
        file_name="student_performance_results.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error("Dataset not found. Keep 'student data.xlsx' in the project folder.")
except Exception as e:
    st.error(f"An error occurred while processing the dataset: {e}")
