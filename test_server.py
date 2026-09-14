"""
Automated Backend & Server Tests for Tanglish IDE
"""
import sys
from server import app

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_endpoints():
    print("=" * 50)
    print("Testing Flask Server Endpoints")
    print("=" * 50)
    
    client = app.test_client()
    
    # Test 1: Root route loads index.html
    res_index = client.get('/')
    assert res_index.status_code == 200, f"Expected 200, got {res_index.status_code}"
    assert "Tanglish Programming IDE" in res_index.get_data(as_text=True), "index.html content missing"
    print("[PASS]: GET / successfully serves index.html")
    
    # Test 2: /run endpoint with Tanglish code
    tanglish_sample = 'eluthu("வணக்கம்")\ncount = 0\nneram count < 2:\n    eluthu(count)\n    count = count + 1'
    res_run = client.post('/run', json={'code': tanglish_sample})
    assert res_run.status_code == 200, f"Expected 200, got {res_run.status_code}"
    json_data = res_run.get_json()
    assert 'output' in json_data, "No output in response"
    output = json_data['output']
    assert "வணக்கம்" in output, "Expected Tamil output missing"
    assert "1" in output, "Expected loop output missing"
    print("[PASS]: POST /run executes Tanglish code and returns output")
    
    print("=" * 50)
    print("All Server Tests Passed Successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_endpoints()
