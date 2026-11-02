"""Create a GitHub-ready archive containing code and public proof receipts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile
from audit import check_sources

ROOT = Path(__file__).resolve().parents[1]

def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    assert not check_sources(), 'Source integrity checks failed'
    receipts=[]
    for label in ('Theorem1','CategoryTransfer'):
        stem=ROOT/'metadata'/label
        submission=json.loads(stem.with_suffix('.submission.json').read_text(encoding='utf-8'))
        verdict=json.loads(stem.with_suffix('.verdict.json').read_text(encoding='utf-8'))
        checked=json.loads(stem.with_suffix('.local-check.json').read_text(encoding='utf-8'))
        source=ROOT/'Solutions'/f'{label}.lean'
        assert verdict['status']=='ACCEPTED' and verdict['id']==submission['submission_id']
        assert checked['passed'] and checked['solution_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
        target=json.loads(stem.with_suffix('.proved-target.json').read_text(encoding='utf-8'))
        assert target['status']=='Proved' and target['theorem_id']==verdict['theorem_id']
        receipts.append({'theorem_name':target['theorem_name'],'theorem_id':target['theorem_id'],
            'theorem_status':target['status'],'submission_id':verdict['id'],'verification_status':verdict['status'],
            'solution':source.relative_to(ROOT).as_posix(),'solution_sha256':checked['solution_sha256'],
            'mathlib_rev':target['mathlib_rev'],'local_compile_passed':True})
    save(ROOT/'docs/platform-verification.json', {'checked_at':datetime.now(timezone.utc).isoformat(),
        'proofs':receipts, 'proposal_id':'007144fb-a3d7-42ca-aa42-82a5990fb254',
        'mission_moderation':'In review at last inspection; theorem acceptance is verified separately'})
    fixed=['.gitignore','LICENSE','README.md','lakefile.lean','lake-manifest.json','lean-toolchain','NoBorelUpperBound.lean']
    files=[ROOT/p for p in fixed]
    for folder in ('Definitions','NoBorelUpperBound','Solutions','scripts','docs','.github'):
        files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    files=sorted(set(files))
    assert not any(p.name=='credentials.json' or 'metadata' in p.relative_to(ROOT).parts for p in files)
    entries={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    manifest=ROOT/'release-manifest.json'
    save(manifest,{'files_sha256':entries,'mathlib_rev':'c5ea00351c28e24afc9f0f84379aa41082b1188f',
        'lean_toolchain':'leanprover/lean4:v4.30.0'})
    files.append(manifest)
    archive=ROOT.parent/'borel-upper-bound-lean-github.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
    print(json.dumps({'archive':str(archive),'files':len(files),'bytes':archive.stat().st_size,
        'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}))

if __name__=='__main__': main()
