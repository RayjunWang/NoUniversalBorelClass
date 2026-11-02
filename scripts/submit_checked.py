"""Idempotent submission of a locally compiled exact standalone proof."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import subprocess
import sys
from prove2me_api import request, submit_proof

ROOT = Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding='utf-8')
def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('label', choices=['Theorem1','CategoryTransfer'])
    ap.add_argument('--poll', action='store_true')
    args=ap.parse_args()
    stem=ROOT/'metadata'/args.label
    receipt=stem.with_suffix('.submission.json')
    if receipt.exists():
        previous=json.loads(receipt.read_text(encoding='utf-8'))
        result=request('verify?submission_id='+previous['submission_id'])
        save(stem.with_suffix('.verdict.json'),result)
        print(json.dumps(result,ensure_ascii=False),flush=True)
        if result['status']=='ACCEPTED':
            save(stem.with_suffix('.proved-target.json'),request('theorems/'+result['theorem_id']))
        return
    assert not args.poll, 'No submission recorded'
    report=json.loads((ROOT/'metadata'/f'{args.label}-standalone.json').read_text(encoding='utf-8'))
    path=ROOT/report['solution']
    proof=path.read_text(encoding='utf-8')
    assert hashlib.sha256(path.read_bytes()).hexdigest()==report['solution_sha256']
    assert not re.search(r'\bsorry\b|\bsorryAx\b|\bnative_decide\b|^\s*(axiom|constant|unsafe)\b',proof,re.M)
    assert re.search(r'^theorem solution\b',proof,re.M)
    assert 'Theorems.Thm_'+report['target_name'].replace('.','_') not in proof
    target=request('theorems/'+report['target_id'])
    assert target['formal_statement']==report['published_formal_statement']
    assert target['preamble']==report['published_preamble']
    assert target['mathlib_rev']==report['mathlib_rev']=='c5ea00351c28e24afc9f0f84379aa41082b1188f'
    checked=subprocess.run(['lake','env','lean',str(path)],cwd=ROOT,capture_output=True,
        text=True,encoding='utf-8',errors='replace')
    stem.with_suffix('.local-build.log').write_text(checked.stdout+checked.stderr,encoding='utf-8')
    assert checked.returncode==0, 'Local standalone compilation failed; see build log'
    save(stem.with_suffix('.local-check.json'),{'passed':True,'solution_sha256':report['solution_sha256'],
        'target_id':report['target_id'],'checked_at':datetime.now(timezone.utc).isoformat()})
    attempt=stem.with_suffix('.attempt.json')
    assert not attempt.exists(), 'An earlier upload has unknown outcome: reconcile before retry'
    explanation=(ROOT/'docs'/f'{args.label}-explanation.md').read_text(encoding='utf-8')
    save(attempt,{'target_id':report['target_id'],'solution_sha256':report['solution_sha256'],
        'started_at':datetime.now(timezone.utc).isoformat(),'status':'pending: reconcile if no receipt'})
    result=submit_proof(report['target_id'],proof,explanation)
    save(receipt,result)
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__': main()
