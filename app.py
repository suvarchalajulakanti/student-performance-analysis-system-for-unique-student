import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Student Performance Analysis", layout="wide")

st.title("🎓 Student Performance Analysis System")
st.write("Analyze student marks, attendance, grades, and overall performance.")

file_path = Path(__file__).parent / "student data.xlsx"

try:
    df = pd.read_excel(file_path)

    required_columns = [
        "name", "s1", "s2", "s3", "s4", "s5", "s6", "attendence"
    ]

    if not all(col in df.columns for col in required_columns):
        st.error("The Excel file is missing one or more required columns.")
        st.stop()

    pass_mark = st.number_input(
        "Minimum marks required in each subject",
        min_value=0, max_value=100, value=35
    )

    min_attendance = st.number_input(
        "Minimum attendance percentage",
        min_value=0.0, max_value=100.0, value=75.0
    )

    if st.button("Analyze Student Performance"):
        subject_cols = ["s1", "s2", "s3", "s4", "s5", "s6"]

        df["Average Marks"] = df[subject_cols].mean(axis=1)

        is_pass = (
            (df[subject_cols] >= pass_mark).all(axis=1)
            & (df["attendence"] >= min_attendance)
        )

        df["Result"] = np.where(is_pass, "pass", "fail")

        df["Grade"] = np.select(
            [
                df["Average Marks"] >= 90,
                df["Average Marks"] >= 80,
                df["Average Marks"] >= 70,
                df["Average Marks"] >= 60
            ],
            ["A", "B", "C", "D"],
            default="E"
        )

        df.loc[~is_pass, "Grade"] = "fail"

        st.subheader("Analysis Results")
        st.dataframe(df, use_container_width=True)

        top_idx = df["Average Marks"].idxmax()
        top_student = df.loc[top_idx]

        st.subheader("🏆 Top Performing Student")
        st.success(
            f"{top_student['name']} — "
            f"Average: {top_student['Average Marks']:.2f}%"
        )

        st.subheader("Student Performance Descriptions")

        for _, row in df.iterrows():
            failed = [
                sub.upper()
                for sub in subject_cols
                if row[sub] < pass_mark
            ]

            low_attendance = row["attendence"] < min_attendance

            if row["Result"] == "pass":
                description = (
                    f"{row['name']} passed with an average of "
                    f"{row['Average Marks']:.2f}% and grade "
                    f"{row['Grade']}. Attendance: {row['attendence']}%."
                )
            else:
                reasons = []
                if failed:
                    reasons.append("failed subjects: " + ", ".join(failed))
                if low_attendance:
                    reasons.append(
                        f"attendance shortage ({row['attendence']}%)"
                    )

                description = (
                    f"{row['name']} failed due to "
                    f"{' and '.join(reasons)}. "
                    f"Average: {row['Average Marks']:.2f}%."
                )

            st.write("- " + description)

except FileNotFoundError:
    st.error("Dataset not found. Ensure student data.xlsx is in the project folder.")
except Exception as e:
    st.error(f"Unable to analyze the dataset: {e}")
