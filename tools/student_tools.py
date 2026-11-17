from utils.data_loader import (
    students_df,
    attendance_df,
    assessments_df
)


def get_student(student_id):

    student = students_df[
        students_df["student_id"] == student_id
    ]


    if student.empty:
        return "Student not found"
    attendance = attendance_df[
        attendance_df["student_id"] == student_id
    ]
    assessments = assessments_df[
        assessments_df["student_id"] == student_id
    ]
    return {
        "student": student.to_dict("records"),
        "attendance": attendance.to_dict("records"),
        "assessments": assessments.to_dict("records")
    }

if __name__ == "__main__":

    result = get_student("STU0001")

    print(result)