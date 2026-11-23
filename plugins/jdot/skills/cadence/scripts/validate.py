from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
required = ['SKILL.md','README.md','references/meeko.md','references/cadence.md','references/quality.md','tests/cases.md','integration/JDOT.md','tests/results.md','CHANGELOG.md']
for name in required:
    assert (root/name).is_file() and (root/name).read_text().strip(), name
    print('PASS file:', name)
s = (root/'SKILL.md').read_text()
assert re.match(r'\A---\nname: cadence\ndescription: [^\n]+\n---\n',s)
print('PASS metadata shape')
for name in re.findall(r'(?:references|integration)/[\w.-]+\.md',s):
    assert (root/name).is_file(), name
    print('PASS reference:',name)
print('Structural checks complete; behavioral compliance not established.')
