import os
import pandas as pd
from config import DATA_DIR

# ==========================
# Helper Function
# ==========================

def load_csv(filename):
    """
    Load a CSV file from the data directory.
    """
    path = os.path.join(DATA_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in {DATA_DIR}")

    return pd.read_csv(path)


# ==========================
# Load All Dataset Files
# ==========================

files = [
    "students.csv",
    "courses.csv",
    "assessments.csv",
    "attendance.csv",
    "mentors.csv"
]

for file in files:
    print(f"Loading {file}...")
    df = load_csv(file)
    print(f"[OK] {file}: {df.shape}")


students_df = load_csv("students.csv")
courses_df = load_csv("courses.csv")
assessments_df = load_csv("assessments.csv")
attendance_df = load_csv("attendance.csv")
mentors_df = load_csv("mentors.csv")