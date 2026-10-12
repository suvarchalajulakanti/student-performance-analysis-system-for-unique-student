import pandas as pd
import numpy as np
df = pd.read_excel("/content/student data.xlsx")  # upload your file
print(df.to_string(index=False))
pass_mark = int(input("enter the pass marks for each subject: "))
min_attendence = float(input("enter the minimum attendence percent: "))
is_pass = (
    (df['s1'] >= pass_mark) &
    (df['s2'] >= pass_mark) &
    (df['s3'] >= pass_mark) &
    (df['s4'] >= pass_mark) &
    (df['s5'] >= pass_mark) &
    (df['s6'] >= pass_mark) &
    (df['attendence'] >= min_attendence)
)
# Use np.where to assign 'pass' if True, and 'fail' if False for each row
df['Result'] = np.where(is_pass, 'pass', 'fail')
# --- Calculate Average and define helper variables ---
subject_cols = ['s1', 's2', 's3', 's4', 's5', 's6']
attendance_col = 'attendence'
df['Average'] = df[subject_cols].mean(axis=1).round(2)

# 4. Generate the dynamic Description column
df['Description'] = df.apply(
    lambda row: f"{row['name']} obtained an average score of {row['Average']}% "
                f"across {len(subject_cols)} subjects with an attendance of {row[attendance_col]}%. "
                f"The student has {row['Result'].lower()} the requirements.",
    axis=1
)
# 5. Search for a specific student
print("\n" + "="*40)
student_name = input("Enter the name of the student to search: ").strip().lower()
matched_student = df[df['name'].str.strip().str.lower() == student_name]

# Display student details without description in the table view first
cols_to_show = [col for col in matched_student.columns if col != 'Description']
print(matched_student[cols_to_show].to_string(index=False))

# Print the description on a new line
if not matched_student.empty:
    print("\nDescription:")
    for desc in matched_student['Description']:
        print(desc)
