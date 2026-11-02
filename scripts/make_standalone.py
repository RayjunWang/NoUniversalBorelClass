"""Combine whole source modules, preserving every declaration unchanged.

Only import lines are relocated. Each original module has one unclosed
`noncomputable section`; closing it at its original EOF preserves the source's
local scopes. No theorem body is cut or replaced by a placeholder.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'Solutions'
OUT.mkdir(exist_ok=True)
(ROOT/'metadata').mkdir(exist_ok=True)
TARGETS = {
    'Theorem1': ('NoBorelUpperBound.Main', 'main-current.json',
        'NoBorelUpperBoundFSigma.theorem1'),
    'CategoryTransfer': ('NoBorelUpperBound.CategoryTransferFinal', 'lemma2-current.json',
        'NoBorelUpperBoundFSigma.lemma2_category_transfer'),
}

def generate(label, root_module, metadata, name):
    seen, ordered, imports = set(), [], set()
    def visit(module):
        if module in seen:
            return
        seen.add(module)
        path = ROOT/Path(*module.split('.')).with_suffix('.lean')
        text = path.read_text(encoding='utf-8')
        for line in text.splitlines():
            if line.startswith('import '):
                dep = line.removeprefix('import ').strip()
                if dep.startswith('NoBorelUpperBound.'):
                    visit(dep)
                else:
                    imports.add(dep)
        assert text.splitlines().count('noncomputable section') == 1, path
        ordered.append((module, path, text))
    visit(root_module)
    target = json.loads((ROOT/'docs/published-targets.json').read_text(encoding='utf-8'))[label]
    statement = target['formal_statement'].strip()
    assert statement.startswith('theorem '+name+'\n')
    assert statement.endswith(':= by sorry')
    signature = statement[len('theorem '+name): -len(':= by sorry')]
    content = '\n'.join('import '+i for i in sorted(imports))
    content += '\n\nset_option autoImplicit false\n'
    records = []
    for module,path,text in ordered:
        body = '\n'.join(line for line in text.splitlines() if not line.startswith('import '))
        content += '\n-- BEGIN WHOLE MODULE '+module+'\n'+body+'\nend\n'
        content += '-- END WHOLE MODULE '+module+'\n'
        records.append({'module':module,'path':path.relative_to(ROOT).as_posix(),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    content += '\nuniverse u v w z t\n\ntheorem solution'+signature+':= by\n'
    proof = 'NoBorelUpperBoundFSigma.theorem1' if label == 'Theorem1' else 'NoBorelUpperBoundFSigma.category_transfer'
    if label == 'CategoryTransfer':
        content += ('  letI : MeasurableSpace G := borel G\n'
            '  letI : BorelSpace G := ⟨rfl⟩\n'
            '  letI : ∀ n, MeasurableSpace (A n) := fun n => borel (A n)\n'
            '  letI : ∀ n, BorelSpace (A n) := fun _ => ⟨rfl⟩\n'
            '  exact '+proof+' h h_joint h_cont z0 hz F hF h_bound\n')
    else:
        content += '  exact '+proof+'\n'
    path = OUT/f'{label}.lean'
    path.write_text(content, encoding='utf-8', newline='\n')
    report = {'target_id': target['theorem_id'], 'target_name': name,
        'mathlib_rev':target['mathlib_rev'], 'solution':path.relative_to(ROOT).as_posix(),
        'solution_sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'modules':records,
        'published_formal_statement':target['formal_statement'], 'published_preamble':target['preamble']}
    (ROOT/'metadata'/f'{label}-standalone.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'solution':label,'modules':len(records),'bytes':path.stat().st_size}))

if __name__=='__main__':
    for label,args in TARGETS.items():
        generate(label,*args)
