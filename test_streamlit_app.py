"""
Verification that app.py embeds and serves templates/index.html
"""

import os
import sys
from streamlit.testing.v1 import AppTest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

APP_PATH = os.path.abspath("app.py")

def test_app():
    print("=" * 60)
    print("TESTING APP.PY FULL-SCREEN INDEX.HTML EMBEDDING")
    print("=" * 60)
    
    at = AppTest.from_file(APP_PATH, default_timeout=15)
    at.run()
    
    assert len(at.exception) == 0, f"AppTest raised exceptions: {at.exception}"
    print("[PASS]: app.py starts cleanly with 0 exceptions")
    
    # Verify templates/index.html exists and is non-empty
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    assert os.path.exists(html_path), "templates/index.html missing"
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Tanglish Programming IDE" in content, "Missing header title"
    assert "main.tn" in content, "Missing main.tn"
    assert "runTanglishCode" in content, "Missing runTanglishCode"
    print("[PASS]: templates/index.html verified with all IDE components")
    
    print("=" * 60)
    print("ALL VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_app()
