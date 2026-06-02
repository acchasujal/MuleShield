import py_compile
import warnings

files_to_check = [
    'frontend/app.py', 
    'backend/app.py', 
    'backend/database.py',
    'backend/routers/ml_predict.py',
    'backend/routers/i4c_webhook.py',
    'backend/routers/analyze.py'
]
banned = ['Bank of India', 'IIT Hyderabad', 'Hackathon', 'PS-2', 'utcnow(']

print('=== HACKATHON PURGE CHECK ===')
all_clean = True
for fp in files_to_check:
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    file_clean = True
    for i, line in enumerate(lines, 1):
        for pat in banned:
            if pat in line:
                print(f'  REMAINING [{fp}:{i}] {pat!r}')
                file_clean = False
                all_clean = False
    if file_clean:
        print(f'  CLEAN: {fp}')

print()
print('=== SYNTAX CHECK ===')
for fp in files_to_check:
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings('error', category=SyntaxWarning)
            py_compile.compile(fp, doraise=True)
        print(f'  SYNTAX OK: {fp}')
    except Exception as e:
        print(f'  SYNTAX FAIL: {fp} -> {e}')
        all_clean = False

print()
print('=== PYVIS BUG FIX CHECK ===')
with open('frontend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_id = 'ACC052000001200'
new_id = 'ACC0520000001200'
if old_id not in content:
    print('  PASS: old truncated ID ACC052000001200 is gone')
else:
    print('  FAIL: old truncated ID still present')
    all_clean = False
if new_id in content:
    print('  PASS: correct ID ACC0520000001200 is present')

print()
if all_clean:
    print('ALL CHECKS PASSED - Production hardening complete.')
else:
    print('SOME CHECKS FAILED - Review above.')
