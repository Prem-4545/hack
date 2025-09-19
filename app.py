from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import numpy as np
from PIL import Image
import io
import base64
from facenet_pytorch import InceptionResnetV1, MTCNN
import torch
from user_data.db_utils import get_db_connection, init_db
import cv2
import dlib
from scipy.spatial import distance as dist
import json

app = Flask(__name__)
app.secret_key = "super-secret-key"

USER_DATA_DIR = "user_data"
os.makedirs(USER_DATA_DIR, exist_ok=True)
init_db()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
facenet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
mtcnn = MTCNN(keep_all=True, device=device)

# Dlib's facial landmark predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# The 68-point facial landmark detector data file needs to be downloaded from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear

def username_to_filename(username):
    return username.strip().lower().replace(' ', '_')

def get_face_embedding(img_bytes, check_liveness=False):
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    
    # Check for face spoofing (basic contrast check)
    img_np = np.array(img) / 255.0
    mean = img_np.mean(axis=(0, 1))
    std = img_np.std()
    if std < 0.08 or mean[2] > 0.45 or mean[0] < 0.25:
        return None, "Access denied: Face image appears to be from a phone or screen. Please use your real face."

    # Liveness check: detect eye blinking
    if check_liveness:
        img_cv = cv2.imdecode(np.frombuffer(io.BytesIO(img_bytes).read(), np.uint8), 1)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        rects = dlib.get_frontal_face_detector()(gray, 1)

        if len(rects) == 0:
            return None, "No face detected for liveness check."

        shape = predictor(gray, rects[0])
        shape = np.array([(shape.part(i).x, shape.part(i).y) for i in range(68)])

        # get eye coordinates from landmarks
        leftEye = shape[36:42]
        rightEye = shape[42:48]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio for both eyes
        ear = (leftEAR + rightEAR) / 2.0
        
        # A low EAR value indicates a blink. This threshold might need tuning.
        if ear > 0.2: 
            return None, "Blinking not detected. Please try again."

    boxes, _ = mtcnn.detect(img)
    if boxes is None or len(boxes) != 1:
        return None, f"Expected 1 face, found {0 if boxes is None else len(boxes)}. Please ensure only your face is visible."
    
    face = img.crop(boxes[0])
    face = face.resize((160, 160))
    img_np = np.array(face) / 255.0

    img_tensor = torch.tensor(img_np).permute(2, 0, 1).unsqueeze(0).float().to(device)
    with torch.no_grad():
        emb = facenet(img_tensor)
    return emb.cpu().numpy()[0], None

def compare_embeddings(emb1, emb2, threshold=0.8):
    dist = np.linalg.norm(emb1 - emb2)
    return dist < threshold

def save_user_embedding(username, embedding):
    filename = username_to_filename(username)
    path = os.path.join(USER_DATA_DIR, f"{filename}.npy")
    np.save(path, embedding)
    return path

def find_username_by_embedding(embedding, threshold=0.8):
    for fname in os.listdir(USER_DATA_DIR):
        if fname.endswith('.npy'):
            user_emb = np.load(os.path.join(USER_DATA_DIR, fname))
            if compare_embeddings(embedding, user_emb, threshold=threshold):
                return fname[:-4]
    return None

def load_user_embedding(username):
    filename = username_to_filename(username)
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (filename,)).fetchone()
    conn.close()
    if user and os.path.exists(user['embedding_path']):
        return np.load(user['embedding_path'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    img_b64 = request.form['image']
    captcha = request.form.get('captcha', '')
    try:
        captcha_val = int(captcha)
    except Exception:
        return jsonify({'status': 'fail', 'message': 'Captcha incorrect.'})
    if captcha_val < 2 or captcha_val > 20:
        return jsonify({'status': 'fail', 'message': 'Captcha incorrect.'})
    img_bytes = base64.b64decode(img_b64.split(',')[1])
    filename = username_to_filename(username)
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (filename,)).fetchone()
    if user:
        conn.close()
        return jsonify({'status': 'exists', 'message': '😮 User already exists!'})
    emb, err = get_face_embedding(img_bytes)
    if err:
        conn.close()
        return jsonify({'status': 'fail', 'message': err})
    matched_username = find_username_by_embedding(emb)
    if matched_username and matched_username != filename:
        conn.close()
        return jsonify({'status': 'fail', 'message': f'❌ This face is already registered with username: {matched_username}.'})
    emb_path = save_user_embedding(username, emb)
    conn.execute('INSERT INTO users (username, embedding_path) VALUES (?, ?)', (filename, emb_path))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': '🎉 Signup successful! You can now login.'})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    img_b64 = request.form['image']
    captcha = request.form.get('captcha', '')
    try:
        captcha_val = int(captcha)
    except Exception:
        return jsonify({'status': 'fail', 'message': 'Captcha incorrect.'})
    if captcha_val < 2 or captcha_val > 20:
        return jsonify({'status': 'fail', 'message': 'Captcha incorrect.'})
    img_bytes = base64.b64decode(img_b64.split(',')[1])
    
    # Liveness check is enabled for login
    emb, err = get_face_embedding(img_bytes, check_liveness=True)
    if err:
        return jsonify({'status': 'fail', 'message': err})

    registered_emb = load_user_embedding(username)
    if registered_emb is None:
        return jsonify({'status': 'fail', 'message': '❌ User not found. Please sign up first.'})
    if compare_embeddings(emb, registered_emb):
        session['user'] = username
        return jsonify({'status': 'success', 'message': f'✅ Welcome back, {username}!'} )
    else:
        return jsonify({'status': 'fail', 'message': '😮 Face does not match. Try again!'})

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('profile.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)