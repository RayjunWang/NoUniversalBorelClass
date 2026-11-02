"""Read the exact mission state without logging credentials."""
from pathlib import Path
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from prove2me_api import request

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / 'metadata'
META.mkdir(exist_ok=True)
def save(name, value):
    (META/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

proposal = request('mission-proposals/007144fb-a3d7-42ca-aa42-82a5990fb254')
save('proposal-current.json', proposal)
envs = request('environments')
save('environments-current.json', envs)
matches = request('theorems?q=NoBorelUpperBoundFSigma.theorem1&env=all&view=compact')
save('main-search-current.json', matches)
for key, path in {
    'main-current.json': 'theorems/56adfcf7-9df7-4730-b48d-1968cd83b344',
    'lemma2-current.json': 'theorems/40920824-81c1-4fcc-8ce2-9028e5727fd5',
    'context-current.json': 'definitions/57c447a3-87a3-4ca4-93e8-4a2437140158',
    'transfer-context-current.json': 'definitions/4d698a98-2bb3-4c61-b8e5-5b3b684fda72',
}.items():
    save(key, request(path))
print(json.dumps({'proposal_status': proposal['status'],
    'items': [{k: i.get(k) for k in ('id','kind','theorem_id','theorem_name','definition_name')} for i in proposal['items']],
    'matches': [{k: t.get(k) for k in ('theorem_id','theorem_name','status')} for t in matches['theorems']]}, ensure_ascii=False))
