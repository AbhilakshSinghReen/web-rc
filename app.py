from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

# OpenCV Video Capture
camera = cv2.VideoCapture(0)  # Adjust index for different webcams

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')  # Serve HTML page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
