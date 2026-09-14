"""
Automated Test Suite for Tanglish Compiler
"""
import io
import sys
import contextlib
from thanglish import execute_tanglish_code, translate_tanglish_to_python

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_test(name, code, expected_substring):
    output_buf = io.StringIO()
    with contextlib.redirect_stdout(output_buf):
        try:
            res = execute_tanglish_code(code)
            if res is not None:
                print(res)
        except Exception as e:
            print(f"Exception: {e}")
    output = output_buf.getvalue()
    passed = expected_substring in output
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status}: {name}")
    if not passed:
        print(f"   Expected substring: {expected_substring!r}")
        print(f"   Actual output: {output!r}")
        print(f"   Translated Python code:\n{translate_tanglish_to_python(code)}")
    return passed

def main():
    print("=" * 50)
    print("Running Tanglish Compiler Verification Tests")
    print("=" * 50)
    
    tests = [
        ("Hello World Print", 
         'eluthu("வணக்கம் உலகம்!")', 
         "வணக்கம் உலகம்!"),
         
        ("String Preservation (Keywords inside strings)",
         'eluthu("enna thambi neram nallama?")', 
         "enna thambi neram nallama?"),
         
        ("While Loop (neram keyword test)",
         '''
count = 0
neram count < 3:
    eluthu(f"count={count}")
    count = count + 1
''',
         "count=2"),
         
        ("For Loop (payan ... udaya test)",
         '''
payan i udaya range(3):
    eluthu(f"i={i}")
''',
         "i=2"),
         
        ("Conditionals (enna / illainu / illana)",
         '''
val = 15
enna val > 20:
    eluthu("greater")
illainu val == 15:
    eluthu("equal")
illana:
    eluthu("lesser")
''',
         "equal"),
         
        ("Functions & Returns (varu / mudivu)",
         '''
varu koottu(a, b):
    mudivu a + b
result = koottu(10, 20)
eluthu(f"result={result}")
''',
         "result=30"),
         
        ("Data Types (pattial / agarathi / neelamm)",
         '''
items = pattial([10, 20, 30])
eluthu(f"len={neelamm(items)}")
''',
         "len=3"),
         
        ("Math Functions (kanitham_sqrt)",
         '''
sq = kanitham_sqrt(16)
eluthu(f"sqrt={int(sq)}")
''',
         "sqrt=4")
    ]
    
    passed_count = 0
    for name, code, expected in tests:
        if run_test(name, code, expected):
            passed_count += 1
            
    print("=" * 50)
    print(f"Summary: {passed_count}/{len(tests)} tests passed.")
    print("=" * 50)
    return passed_count == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
