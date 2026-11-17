import sys, os
sys.path.insert(0, r'C:\Users\nikhi\Agentic_rag_fixed\Agentic rag')
os.chdir(r'C:\Users\nikhi\Agentic_rag_fixed\Agentic rag')

from starlette.testclient import TestClient
from backend.main import app

with TestClient(app) as client:
    conv = client.post('/api/conversations', json={'title': 'Risk Test'}).json()
    cid = conv['id']

    r = client.post('/api/chat', json={
        'conversation_id': cid,
        'message': 'Show me students who are at overall risk based on both marks and attendance'
    })
    print('Status:', r.status_code)
    print(r.json()['response'][:800])
    client.delete(f'/api/conversations/{cid}')

