import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Valve import Valve
from flask_cors import CORS
import config  
from datetime import datetime 
import paho.mqtt.client as paho 
from paho import mqtt 

#To-do 비밀번호와 broker 접속에 대한 정보를 바깥에 빼야 한다. 
def on_connect(client, userdata,flags, rc, properties=None):
    print("CONACK received with code %s"% rc )

def on_publish(client, userdata, mid, properties=None):
    print("mid: "+str(mid)) 

def on_subscribe(client, userdata,mid, granted_qos,properties=None):
    print("Subscribed: ",str(mid) + " " + str(granted_qos)) 

def on_message(client, userdata, msg): 
    print(msg.topic + " " +str(msg.qos) + " " +str(msg.payload)) 



app = Flask(__name__)
CORS(app)
app.secret_key = config.SECRET_KEY  

PASSWORD_HASH = config.PASSWORD_HASH 

JSON_FILE = 'valves.json'
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("north_pohang", "pohang123POHANG!@#")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.connect("e94e4245a7a44cf9a744f49b1072c3f2.s1.eu.hivemq.cloud", 8883)
client.loop_start()

def initialize_json():
    if not os.path.exists(JSON_FILE) or os.path.getsize(JSON_FILE) == 0:
        with open(JSON_FILE, 'w') as f:
            json.dump({i: {
                "valve_number": i,
                "left": False,
                "right": False,
                "left_change_time": None,
                "right_change_time": None
            } for i in range(1, 6)}, f, indent=4)

initialize_json()

valves = {i: Valve(i) for i in range(1, 6)}

with open(JSON_FILE, 'r') as f:
    try:
        data = json.load(f)
        valves = {int(k): Valve.from_dict(v) for k, v in data.items()}
    except json.JSONDecodeError:
        print("JSON 파일이 손상되었습니다. 기본값으로 초기화합니다.")
        initialize_json()  

def save_to_json():
    with open(JSON_FILE, 'w') as f:
        json.dump({k: v.to_dict() for k, v in valves.items()}, f, indent=4)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    if check_password_hash(PASSWORD_HASH, password):
        session['authenticated'] = True
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='비밀번호가 틀렸습니다.')

@app.route('/index')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login_page'))

    global valves
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            valves = {int(k): Valve.from_dict(v) for k, v in data.items()}

    return render_template('index.html', valves=valves)

@app.route('/toggle', methods=['POST'])
def toggle_valve():
    if not session.get('authenticated'):
        return jsonify({'error': 'unauthorized'}), 403

    data = request.get_json()
    valve_number = int(data['valve'])
    side = data['side']

    valve = valves[valve_number]
    if side == 'left':
        valve.toggle_left()
        left_payload = "init"
        if(valve.left == True):
            left_payload ="1 on"
        else:
            left_payload ="1 off"

        
        pload = "valve "+left_payload
        print(pload)

        client.publish(f"handong/node{valve_number}",payload =pload ,qos = 2) 
        print(f"sent to handong/node{valve_number}")
    
    elif side == 'right':
        valve.toggle_right()
        right_payload = "init"
        if(valve.right == True):
            right_payload ="2 on"
        else:
            right_payload ="2 off"

        pload = "valve "+right_payload
        print(pload)
        
        client.publish(f"handong/node{valve_number}",payload =pload ,qos = 2) 
        print(f"sent to handong/node{valve_number}")


    save_to_json()
    print(valve.valve_number,"||",valve.left,"||",valve.right)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        'valve': valve_number,
        'left': valve.left,
        'right': valve.right,
        'left_change_time': valve.left_change_time,
        'right_change_time': valve.right_change_time,
        'current_time': current_time  
    })


@app.route('/save')
def save_state():
    save_to_json()
    return jsonify({'message': '현재 상태가 JSON 파일에 저장되었습니다.'})

@app.route('/load')
def load_state():
    global valves
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
            valves = {int(k): Valve.from_dict(v) for k, v in data.items()}
        return jsonify({'message': 'JSON 파일에서 상태가 불러와졌습니다.', 'valves': data})
    else:
        return jsonify({'error': 'JSON 파일이 존재하지 않습니다.'})
    
if __name__ == '__main__':
    app.run(debug=True)
