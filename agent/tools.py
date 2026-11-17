from langchain_core.tools import tool
from tools.policy_search import search_policy
from tools.student_tools import get_student
from utils.data_loader import (
    students_df,
    attendance_df,
    assessments_df,
    mentors_df,
    courses_df
)
@tool
def policy_search(query: str):
    """Search university policies: attendance, grading, FAQ, alerts."""

    docs = search_policy(query)

    if not docs:
        return "No relevant policy found."

    answer = ""

    for doc in docs:
        answer += f"\nSource: {doc.metadata.get('source', 'Unknown')}\n"
        answer += doc.page_content
        answer += "\n"

    return answer

# -----------------------------
# Attendance Tool
# -----------------------------

@tool
def calculate_attendance(student_id: str):
    """Return attendance summary for a student. Input: student ID like STU0050."""

    df = attendance_df[
        attendance_df["student_id"] == student_id
    ]

    if df.empty:
        return {
            "error": "Student not found."
        }

    total = len(df)

    present = len(
        df[df["status"].str.lower() == "present"]
    )

    late = len(
        df[df["status"].str.lower() == "late"]
    )

    absent = len(
        df[df["status"].str.lower() == "absent"]
    )

    percentage = round(
        (present / total) * 100,
        2
    )

    return {
        "student_id": student_id,
        "total_sessions": total,
        "present": present,
        "late": late,
        "absent": absent,
        "attendance_percentage": percentage
    }


# -----------------------------
# Performance Tool
# -----------------------------

@tool
def performance_summary(student_id: str):
    """Return assessment performance and marks for a student."""

    df = assessments_df[
        assessments_df["student_id"] == student_id
    ].copy()

    if df.empty:
        return {
            "error": "Student not found."
        }

    df["percentage"] = (df["scored"] / df["max_score"]) * 100

    avg_percentage = round(
        (df["scored"].sum() / df["max_score"].sum()) * 100,
        2
    )

    highest = round(float(df["percentage"].max()), 2)

    lowest = round(float(df["percentage"].min()), 2)

    return {
        "student_id": student_id,
        "total_assessments": len(df),
        "average_percentage": avg_percentage,
        "highest_percentage": highest,
        "lowest_percentage": lowest
    }


# -----------------------------
# Student Details Tool
# -----------------------------

@tool
def student_details(student_id: str):
    """Return complete profile information for a student."""

    df = students_df[
        students_df["student_id"] == student_id
    ]

    if df.empty:
        return {
            "error": "Student not found."
        }

    return df.iloc[0].to_dict()


# -----------------------------
# Mentor Tool
# -----------------------------

@tool
def mentor_details(mentor_id: str):
    """Return mentor information by mentor ID."""

    df = mentors_df[
        mentors_df["mentor_id"] == mentor_id
    ]

    if df.empty:
        return {
            "error": "Mentor not found."
        }

    return df.iloc[0].to_dict()


# -----------------------------
# Course Tool
# -----------------------------

@tool
def course_details(course_id: str):
    """
    Returns course information.
    """

    df = courses_df[
        courses_df["course_id"] == course_id
    ]

    if df.empty:
        return {
            "error": "Course not found."
        }

    return df.iloc[0].to_dict()


# -----------------------------
# Average Attendance
# -----------------------------

@tool
def average_attendance(dummy: str = ""):
    """
    Returns average attendance of all students.
    """

    total_students = attendance_df["student_id"].unique()

    percentages = []

    for sid in total_students:

        df = attendance_df[
            attendance_df["student_id"] == sid
        ]

        total = len(df)

        present = len(
            df[df["status"].str.lower() == "present"]
        )

        percentages.append(
            (present / total) * 100
        )

    return {
        "average_attendance": round(
            sum(percentages) / len(percentages),
            2
        )
    }


# -----------------------------
# Top Students
# -----------------------------

@tool
def top_students(dummy: str = ""):
    """
    Returns Top 10 students by average marks.
    """

    grouped = (
        assessments_df
        .groupby("student_id")[["scored", "max_score"]]
        .sum()
    )

    grouped["average_percentage"] = (
        (grouped["scored"] / grouped["max_score"]) * 100
    ).round(2)

    top = (
        grouped["average_percentage"]
        .sort_values(ascending=False)
        .head(10)
    )

    return {k: float(v) for k, v in top.to_dict().items()}


# -----------------------------
# At Risk Students
# -----------------------------

@tool
def at_risk_students(dummy: str = ""):
    """
    Returns students with attendance below 75%.
    """

    risk = []

    for sid in attendance_df["student_id"].unique():

        df = attendance_df[
            attendance_df["student_id"] == sid
        ]

        total = len(df)

        present = len(
            df[df["status"].str.lower() == "present"]
        )

        percentage = round(
            (present / total) * 100,
            2
        )

        if percentage < 75:
            risk.append({
                "student_id": sid,
                "attendance": percentage
            })

    return risk


# -----------------------------
# Overall Risk Assessment
# -----------------------------

@tool
def overall_risk_assessment(dummy: str = ""):
    """
    Performs a comprehensive risk assessment for all students based on
    BOTH attendance percentage AND academic performance (marks).

    Risk classification rules:
    - HIGH risk   : Attendance < 75%  AND  Marks < 60%
    - HIGH risk   : Attendance < 60%  (attendance critically low regardless of marks)
    - HIGH risk   : Marks < 50%       (marks critically low regardless of attendance)
    - MEDIUM risk : Attendance < 75%  OR   Marks < 60%  (only one factor is concerning)
    - LOW risk    : Attendance >= 75% AND  Marks >= 60%

    Returns a list of only HIGH and MEDIUM risk students sorted by risk level
    and then by a combined risk score (worst first).
    """

    results = []

    all_student_ids = set(attendance_df["student_id"].unique()) | set(assessments_df["student_id"].unique())

    for sid in all_student_ids:

        # --- Attendance ---
        att_df = attendance_df[attendance_df["student_id"] == sid]
        if att_df.empty:
            attendance_pct = 0.0
        else:
            total_sessions = len(att_df)
            present = len(att_df[att_df["status"].str.lower() == "present"])
            attendance_pct = round((present / total_sessions) * 100, 2)

        # --- Marks ---
        marks_df = assessments_df[assessments_df["student_id"] == sid]
        if marks_df.empty:
            marks_pct = 0.0
        else:
            marks_pct = round(
                (marks_df["scored"].sum() / marks_df["max_score"].sum()) * 100,
                2
            )

        # --- Combined risk score (lower = worse) ---
        # Weighted: attendance 40%, marks 60%
        risk_score = round(0.4 * attendance_pct + 0.6 * marks_pct, 2)

        # --- Classify ---
        att_low  = attendance_pct < 75
        att_crit = attendance_pct < 60
        mrk_low  = marks_pct < 60
        mrk_crit = marks_pct < 50

        if att_crit or mrk_crit or (att_low and mrk_low):
            risk_level = "HIGH"
        elif att_low or mrk_low:
            risk_level = "MEDIUM"
        else:
            continue   # LOW risk — omit from output

        results.append({
            "student_id":          sid,
            "attendance_pct":      attendance_pct,
            "marks_pct":           marks_pct,
            "combined_risk_score": risk_score,
            "risk_level":          risk_level,
            "flags": {
                "low_attendance":      att_low,
                "critical_attendance": att_crit,
                "low_marks":           mrk_low,
                "critical_marks":      mrk_crit,
            }
        })

    # Sort: HIGH first, then by combined_risk_score ascending (worst first)
    priority = {"HIGH": 0, "MEDIUM": 1}
    results.sort(key=lambda x: (priority[x["risk_level"]], x["combined_risk_score"]))

    high_count   = sum(1 for r in results if r["risk_level"] == "HIGH")
    medium_count = sum(1 for r in results if r["risk_level"] == "MEDIUM")

    # Return a compact summary + top 20 worst students to stay within LLM token limits
    top_students_trimmed = []
    for r in results[:20]:
        top_students_trimmed.append({
            "student_id":          r["student_id"],
            "attendance_pct":      r["attendance_pct"],
            "marks_pct":           r["marks_pct"],
            "combined_risk_score": r["combined_risk_score"],
            "risk_level":          r["risk_level"],
            "critical_attendance": bool(r["flags"]["critical_attendance"]),
            "critical_marks":      bool(r["flags"]["critical_marks"]),
        })

    return {
        "summary": {
            "total_students_assessed": len(all_student_ids),
            "total_at_risk":           len(results),
            "high_risk_count":         high_count,
            "medium_risk_count":       medium_count,
        },
        "top_20_worst_students": top_students_trimmed,
        "note": (
            "Only the 20 highest-risk students are shown. "
            "HIGH risk = critically low attendance (<60%) OR critically low marks (<50%) "
            "OR both low attendance (<75%) and low marks (<60%). "
            "MEDIUM risk = one factor is concerning."
        )
    }


# -----------------------------
# Register Tools
# -----------------------------

tools = [
    calculate_attendance,
    performance_summary,
    student_details,
    mentor_details,
    course_details,
    average_attendance,
    top_students,
    at_risk_students,
    overall_risk_assessment,
    policy_search
]

# -----------------------------
# Plain-callable lookup (for direct/manual testing, e.g. test_tools.py
# and test_agent_tools.py). LangChain's @tool decorator wraps each
# function in a StructuredTool, so calling it directly (tool("x")) does
# not work the way a plain function does; `.func` unwraps it back to
# the original callable. get_student isn't part of the LangChain tool
# list above (student_details covers that role for the agent), but the
# tests expect it here, so it's pulled in directly from tools/student_tools.
# -----------------------------

available_tools = {
    "get_student": get_student,
    "calculate_attendance": calculate_attendance.func,
    "performance_summary": performance_summary.func,
    "student_details": student_details.func,
    "mentor_details": mentor_details.func,
    "course_details": course_details.func,
    "average_attendance": average_attendance.func,
    "top_students": top_students.func,
    "at_risk_students": at_risk_students.func,
    "overall_risk_assessment": overall_risk_assessment.func,
    "policy_search": policy_search.func,
}