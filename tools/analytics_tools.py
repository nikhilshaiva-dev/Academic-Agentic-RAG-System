from utils.data_loader import (
    attendance_df,
    assessments_df
)


def calculate_attendance(student_id):

    data = attendance_df[
        attendance_df["student_id"] == student_id
    ]

    if data.empty:
        return "No attendance data found"


    total = len(data)

    present = len(
        data[data["status"] == "present"]
    )

    late = len(
        data[data["status"] == "late"]
    )

    absent = len(
        data[data["status"] == "absent"]
    )


    percentage = (present / total) * 100


    return {
        "total_sessions": total,
        "present": present,
        "late": late,
        "absent": absent,
        "attendance_percentage": round(percentage,2)
    }



def performance_summary(student_id):

    data = assessments_df[
        assessments_df["student_id"] == student_id
    ]


    if data.empty:
        return "No assessment data found"


    total_score = data["scored"].sum()

    max_score = data["max_score"].sum()


    percentage = (
        total_score / max_score
    ) * 100


    return {
        "total_assessments": len(data),
        "average_percentage": round(percentage,2)
    }



if __name__ == "__main__":

    print(
        calculate_attendance("STU0001")
    )

    print(
        performance_summary("STU0001")
    )