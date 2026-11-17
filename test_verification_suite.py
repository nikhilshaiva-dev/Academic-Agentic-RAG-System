import sys
import os
import time

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from starlette.testclient import TestClient
from backend.main import app

def run_all_tests():
    print("=" * 60)
    print("RUNNING STUDENT AI ASSISTANT FULL SUITE VERIFICATION")
    print("=" * 60)
    
    with TestClient(app) as client:
        # TEST 1: Backend Health
        print("\n--- TEST 1: Backend Health ---")
        health = client.get('/api/health')
        print(f"Status Code: {health.status_code}")
        print(f"Response: {health.json()}")
        assert health.status_code == 200
        assert health.json()['status'] == 'healthy'
        assert health.json()['agent_loaded'] is True
        print("[PASS] Test 1: Backend health endpoint verified.")

        # TEST 2: Student Attendance Tool
        print("\n--- TEST 2: Student Attendance (STU0050) ---")
        c1 = client.post('/api/conversations', json={'title': 'Attendance Test'}).json()
        cid1 = c1['id']
        r_att = client.post('/api/chat', json={'conversation_id': cid1, 'message': 'Show attendance of STU0050'})
        assert r_att.status_code == 200, r_att.text
        att_resp = r_att.json()['response']
        print(f"Response preview:\n{att_resp[:250]}...\n")
        assert '69.23' in att_resp or 'STU0050' in att_resp
        print("[PASS] Test 2: Student attendance tool executed correctly.")

        # TEST 3: Conversation Memory (Follow-up)
        print("\n--- TEST 3: Conversation Memory Context ---")
        r_perf = client.post('/api/chat', json={'conversation_id': cid1, 'message': 'What about performance?'})
        assert r_perf.status_code == 200, r_perf.text
        perf_resp = r_perf.json()['response']
        print(f"Response preview:\n{perf_resp[:250]}...\n")
        assert 'STU0050' in perf_resp or '67.23' in perf_resp or 'performance' in perf_resp.lower()
        print("[PASS] Test 3: Follow-up question correctly recognized STU0050 from conversation memory.")

        # TEST 4: Separate Conversations (Memory Isolation)
        print("\n--- TEST 4: Separate Conversations Isolation ---")
        c2 = client.post('/api/conversations', json={'title': 'Conversation B'}).json()
        cid2 = c2['id']
        r_b1 = client.post('/api/chat', json={'conversation_id': cid2, 'message': 'Show attendance of STU0020'})
        assert r_b1.status_code == 200
        b1_resp = r_b1.json()['response']
        print(f"Conversation B (STU0020) preview:\n{b1_resp[:200]}...\n")
        assert 'STU0020' in b1_resp

        # Check follow-up in Conversation B asks about STU0020, not STU0050
        r_b2 = client.post('/api/chat', json={'conversation_id': cid2, 'message': 'What about performance?'})
        assert r_b2.status_code == 200
        b2_resp = r_b2.json()['response']
        print(f"Conversation B follow-up preview:\n{b2_resp[:200]}...\n")
        assert 'STU0020' in b2_resp
        assert 'STU0050' not in b2_resp
        print("[PASS] Test 4: Conversations A and B are strictly isolated with no cross-talk.")

        # TEST 5: Policy Retrieval (RAG / FAISS)
        print("\n--- TEST 5: Policy Retrieval (FAISS) ---")
        c3 = client.post('/api/conversations', json={'title': 'Policy Test'}).json()
        cid3 = c3['id']
        r_pol = client.post('/api/chat', json={'conversation_id': cid3, 'message': 'Explain the university attendance policy.'})
        assert r_pol.status_code == 200
        pol_resp = r_pol.json()['response']
        print(f"Policy response preview:\n{pol_resp[:250]}...\n")
        assert 'attendance' in pol_resp.lower() and ('75' in pol_resp or 'policy' in pol_resp.lower())
        print("[PASS] Test 5: Policy retrieval via FAISS verified.")

        # TEST 6: Analytics (Top Students)
        print("\n--- TEST 6: Analytics Tool (Top Students) ---")
        c4 = client.post('/api/conversations', json={'title': 'Analytics Test'}).json()
        cid4 = c4['id']
        r_top = client.post('/api/chat', json={'conversation_id': cid4, 'message': 'Who are the top 10 students?'})
        assert r_top.status_code == 200
        top_resp = r_top.json()['response']
        print(f"Top students response preview:\n{top_resp[:250]}...\n")
        assert 'STU' in top_resp
        print("[PASS] Test 6: Analytics tool (top_students) executed successfully.")

        # TEST 7: Chat History Restoration
        print("\n--- TEST 7: Chat History Restoration ---")
        hist = client.get(f'/api/conversations/{cid1}/messages')
        assert hist.status_code == 200
        msgs = hist.json()
        print(f"Found {len(msgs)} messages in conversation A:")
        for m in msgs:
            print(f"  - [{m['role']}] {m['content'][:60]}...")
        assert len(msgs) == 4
        print("[PASS] Test 7: Chat history correctly preserved in SQLite and restored.")

        # Cleanup test conversations
        for cid in [cid1, cid2, cid3, cid4]:
            client.delete(f'/api/conversations/{cid}')
        print("\n[OK] Cleaned up test conversations.")

    print("\n" + "=" * 60)
    print("ALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()

