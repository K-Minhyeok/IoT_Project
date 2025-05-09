from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Valve import Valve
from flask_cors import CORS
import config  


app = Flask(__name__)
CORS(app)
app.secret_key = config.SECRET_KEY  

PASSWORD_HASH = config.PASSWORD_HASH 

valves = {i: Valve(i) for i in range(1, 6)}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    print(password,"를 입력했습니다.")

    if check_password_hash(PASSWORD_HASH, password):
        session['authenticated'] = True
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='비밀번호가 틀렸습니다.')

@app.route('/index') 
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/toggle', methods=['POST'])
def toggle_valve():
    if not session.get('authenticated'):
        return jsonify({'error': 'unauthorized'}), 403

    data = request.get_json()
    valve_number = int(data['valve'])
    side = data['side']

    valve = valves[valve_number]
    if side == 'left':
        valve.left = not valve.left
    elif side == 'right':
        valve.right = not valve.right

    #여기에 MQTT로 신호 보내는 게 필요할 것 같다.
    print(valve,"를 MQTT로 전송")
    return jsonify({
        'valve': valve_number,
        'left': valve.left,
        'right': valve.right
    })

if __name__ == '__main__':
    app.run(debug=True)
