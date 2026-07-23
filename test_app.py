import requests
import time
import subprocess
import pytest

@pytest.fixture(scope="module", autouse=True)
def start_server():
    # Start the Flask app in the background
    proc = subprocess.Popen(["python", "app.py"])
    time.sleep(2) # Wait for server to boot
    yield
    proc.terminate() # Shutdown after tests

def test_ui_over_http():
    base_url = "http://127.0.0.1:5000"
    
    # 1. Test Home Page loads correctly
    res = requests.get(base_url)
    assert res.status_code == 200
    assert "<form" in res.text
    
    # 2. Test Invalid Password (Too short) - Remains on home page
    res = requests.post(base_url, data={"password": "short"})
    assert "Password does not meet requirements" in res.text
    
    # 3. Test Invalid Password (In Top 1000 list) - Remains on home page
    res = requests.post(base_url, data={"password": "password"})
    assert "Password does not meet requirements" in res.text
    
    # 4. Test Valid Password - Redirects and displays password on welcome page
    session = requests.Session()
    res = session.post(base_url, data={"password": "ValidStrongPassword123!"}, allow_redirects=True)
    assert "Your password is: ValidStrongPassword123!" in res.text
    assert "Logout" in res.text