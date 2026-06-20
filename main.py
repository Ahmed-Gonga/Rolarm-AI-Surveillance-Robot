import time, threading, cv2, os
from flask import Flask, Response, jsonify, render_template, request, session, redirect, send_file
from app.config_loader import load_config
from app.database import EventDatabase
from app.camera import Camera
from app.hardware import RobotHardware
from app.face_service import FaceRecognitionService
from app.alerts import AlertManager
from app.auth import require_login

cfg = load_config()
app = Flask(__name__)
app.secret_key = cfg.get('secret_key','change-me')
db = EventDatabase(cfg['db_path'])
camera = Camera(cfg)
hardware = RobotHardware(cfg, db)
faces = FaceRecognitionService(cfg, db)
alerts = AlertManager(cfg, db)
lock = threading.Lock()

state = {'alarm':False,'armed':True,'motion':'stop','speed':cfg.get('default_speed_percent',70),'last_faces':[], 'stranger':False,'gas':False,'fire':False,'pir_motion':False,'last_update':None,'camera_backend':None}

def evaluate_alarm(frame=None):
    sensors = hardware.read_sensors()
    state['gas']=sensors['gas']; state['fire']=sensors['fire']; state['pir_motion']=sensors.get('motion',False)
    danger = state['armed'] and ((cfg.get('alarm_on_stranger',True) and state['stranger']) or (cfg.get('alarm_on_fire_or_gas',True) and (state['gas'] or state['fire'])))
    state['alarm']=bool(danger); hardware.buzzer(state['alarm'])
    if danger:
        if state['stranger'] and frame is not None:
            cv2.imwrite(cfg['latest_intruder_image'], frame)
            alerts.send('stranger', 'STRANGER detected by Sleep Safe Robot. Open the app to check the live camera.', cfg['latest_intruder_image'])
        if state['gas']: alerts.send('gas', 'Gas/smoke sensor danger detected by Sleep Safe Robot.')
        if state['fire']: alerts.send('fire', 'Fire/flame sensor danger detected by Sleep Safe Robot.')

def gen_frames():
    while True:
        frame = camera.read()
        if frame is None:
            time.sleep(0.05); continue
        with lock:
            results, stranger = faces.analyze(frame)
            state['last_faces']=results; state['stranger']=stranger; state['last_update']=time.strftime('%Y-%m-%d %H:%M:%S'); state['camera_backend']=camera.backend
            evaluate_alarm(frame)
            out = faces.draw(frame.copy(), results)
            if state['alarm']:
                cv2.putText(out,'ALARM ACTIVE',(20,45),cv2.FONT_HERSHEY_SIMPLEX,1.1,(0,0,255),3)
            if state['armed']:
                cv2.putText(out,'ARMED',(20,out.shape[0]-20),cv2.FONT_HERSHEY_SIMPLEX,.8,(0,255,255),2)
            else:
                cv2.putText(out,'DISARMED',(20,out.shape[0]-20),cv2.FONT_HERSHEY_SIMPLEX,.8,(180,180,180),2)
        ok, buffer = cv2.imencode('.jpg', out)
        if ok:
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'
        time.sleep(1/max(1,int(cfg.get('camera_fps',15))))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        pin = request.form.get('pin') or (request.json or {}).get('pin') if request.is_json else request.form.get('pin')
        if pin == str(cfg.get('pin_code','1234')):
            session['logged_in']=True; return redirect('/')
        return render_template('login.html', error='Wrong PIN')
    return render_template('login.html')

@app.route('/logout')
def logout(): session.clear(); return redirect('/login')
@app.route('/')
@require_login
def index(): return render_template('index.html', project_name=cfg.get('project_name','Sleep Safe Robot'))
@app.route('/video_feed')
@require_login
def video_feed(): return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/api/status')
@require_login
def api_status():
    with lock: evaluate_alarm()
    return jsonify({'ok':True,'state':state,'trained':faces.trained,'people':db.people(),'mock_hardware':hardware.mock,'mock_camera':camera.mock})
@app.route('/api/events')
@require_login
def api_events(): return jsonify({'ok':True,'events':db.recent_events(int(request.args.get('limit',50)))})
@app.route('/api/move/<direction>', methods=['POST'])
@require_login
def api_move(direction):
    state['motion']=hardware.move(direction); return jsonify({'ok':True,'motion':state['motion']})
@app.route('/api/speed', methods=['POST'])
@require_login
def api_speed():
    val=(request.json or {}).get('speed',70); state['speed']=hardware.set_speed(val); return jsonify({'ok':True,'speed':state['speed']})
@app.route('/api/alarm/<mode>', methods=['POST'])
@require_login
def api_alarm(mode):
    on=mode=='on'; state['alarm']=on; hardware.buzzer(on); db.log('manual_alarm','warning',f'Manual alarm {mode}'); return jsonify({'ok':True,'alarm':on})
@app.route('/api/arm/<mode>', methods=['POST'])
@require_login
def api_arm(mode):
    state['armed']=(mode=='on'); db.log('arm','info',f"System {'armed' if state['armed'] else 'disarmed'}"); return jsonify({'ok':True,'armed':state['armed']})
@app.route('/api/capture', methods=['POST'])
@require_login
def api_capture():
    name=(request.json or {}).get('name',cfg.get('owner_name','Owner'))
    frame=camera.read()
    res=faces.capture_face(frame,name); db.log('capture','info',f"Captured {res['saved_count']} face image(s) for {name}",res); return jsonify({'ok':True,**res})
@app.route('/api/train', methods=['POST'])
@require_login
def api_train():
    try:
        res=faces.train(); db.log('train','info','Face model trained',res); return jsonify({'ok':True,**res})
    except Exception as e: return jsonify({'ok':False,'error':str(e)}),400
@app.route('/api/snapshot')
@require_login
def api_snapshot():
    frame=camera.read(); path=os.path.join(cfg['static_folder'] if 'static_folder' in cfg else 'static','snapshot.jpg')
    path=os.path.join(cfg['root_dir'],'static','snapshot.jpg'); cv2.imwrite(path, frame); return send_file(path, mimetype='image/jpeg')

if __name__ == '__main__':
    try: app.run(host='0.0.0.0', port=5000, threaded=True)
    finally: camera.release(); hardware.cleanup()
