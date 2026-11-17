import sys, os
sys.path.insert(0, r'C:\Users\nikhi\Agentic_rag_fixed\Agentic rag')
os.chdir(r'C:\Users\nikhi\Agentic_rag_fixed\Agentic rag')

from agent.tools import overall_risk_assessment

results = overall_risk_assessment.invoke({})
high   = [r for r in results if r['risk_level'] == 'HIGH']
medium = [r for r in results if r['risk_level'] == 'MEDIUM']

print(f'Total at-risk students : {len(results)}')
print(f'  HIGH  risk           : {len(high)}')
print(f'  MEDIUM risk          : {len(medium)}')
print()
print('--- Top 5 HIGH risk students ---')
for s in high[:5]:
    print(f"  {s['student_id']}  Attendance={s['attendance_pct']}%  Marks={s['marks_pct']}%  Score={s['combined_risk_score']}  Flags={s['flags']}")
print()
print('--- Top 5 MEDIUM risk students ---')
for s in medium[:5]:
    print(f"  {s['student_id']}  Attendance={s['attendance_pct']}%  Marks={s['marks_pct']}%  Score={s['combined_risk_score']}")

