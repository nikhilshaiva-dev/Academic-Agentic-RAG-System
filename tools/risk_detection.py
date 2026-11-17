from utils.data_loader import (
    students_df,
    attendance_df,
    assessments_df
)


def find_risk_students():

    risky_students = []


    for student_id in students_df["student_id"]:

        # Attendance calculation

        attendance = attendance_df[
            attendance_df["student_id"] == student_id
        ]

        if len(attendance) == 0:
            continue


        present = len(
            attendance[
                attendance["status"] == "present"
            ]
        )

        attendance_percentage = (
            present / len(attendance)
        ) * 100


        # Performance calculation

        assessments = assessments_df[
            assessments_df["student_id"] == student_id
        ]

        if len(assessments) == 0:
            continue


        score_percentage = (
            assessments["scored"].sum()
            /
            assessments["max_score"].sum()
        ) * 100


        # Risk rules

        risk = "LOW"


        if attendance_percentage < 75:
            risk = "HIGH"


        elif score_percentage < 50:
            risk = "MEDIUM"



        if risk != "LOW":

            risky_students.append(
                {
                    "student_id": student_id,
                    "attendance": round(
                        attendance_percentage,2
                    ),
                    "score": round(
                        score_percentage,2
                    ),
                    "risk": risk
                }
            )


    return risky_students



if __name__ == "__main__":

    result = find_risk_students()

    print("Risk Students:", len(result))

    for student in result[:10]:
        print(student)