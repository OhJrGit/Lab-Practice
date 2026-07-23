from flask import Flask, request, render_template_string, redirect, url_for, session
import urllib.request

app = Flask(__name__)
app.secret_key = 'super_secret_dev_key'

# Fetch common passwords list on startup
URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/xato-net-10-million-passwords-1000.txt"
try:
    response = urllib.request.urlopen(URL)
    COMMON_PASSWORDS = set(response.read().decode('utf-8').splitlines())
except Exception:
    COMMON_PASSWORDS = set()

def validate_password(pwd):
    # OWASP Level 1: Min 8, Max 64 characters, and not in breached list
    if not pwd or len(pwd) < 8 or len(pwd) > 64:
        return False
    if pwd in COMMON_PASSWORDS:
        return False
    return True

HOME_HTML = '''
<h2>Login</h2>
<form method="POST">
  <input type="password" name="password" placeholder="Enter Password" required>
  <button type="submit">Login</button>
</form>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
'''

WELCOME_HTML = '''
<h2>Welcome</h2>
<p>Your password is: {{ password }}</p>
<form action="/logout" method="POST">
  <button type="submit">Logout</button>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pwd = request.form.get('password')
        if validate_password(pwd):
            session['password'] = pwd
            return redirect(url_for('welcome'))
        return render_template_string(HOME_HTML, error="Password does not meet requirements.")
    return render_template_string(HOME_HTML)

@app.route('/welcome')
def welcome():
    if 'password' not in session:
        return redirect(url_for('home'))
    return render_template_string(WELCOME_HTML, password=session['password'])

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('password', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)