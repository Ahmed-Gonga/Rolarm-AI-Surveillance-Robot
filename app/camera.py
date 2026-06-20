import cv2, time, numpy as np

class Camera:
    def __init__(self, cfg):
        self.cfg = cfg
        self.mock = cfg.get('mock_camera', False)
        self.width = int(cfg.get('camera_width', 640)); self.height = int(cfg.get('camera_height', 480))
        self.last_frame = None
        self.backend = None
        self.picam2 = None
        self.cap = None
        if not self.mock:
            try:
                from picamera2 import Picamera2
                self.picam2 = Picamera2()
                self.picam2.configure(self.picam2.create_preview_configuration(main={'format':'RGB888','size':(self.width,self.height)}))
                self.picam2.start(); self.backend = 'picamera2'
            except Exception:
                self.cap = cv2.VideoCapture(0)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width); self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                if self.cap.isOpened(): self.backend = 'opencv_usb'
                else: self.mock = True; self.backend = 'mock'
        else:
            self.backend = 'mock'

    def read(self):
        if self.mock:
            frame = np.zeros((self.height,self.width,3), dtype=np.uint8)
            cv2.putText(frame, 'Sleep Safe Robot - MOCK CAMERA', (30,60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            cv2.putText(frame, time.strftime('%Y-%m-%d %H:%M:%S'), (30,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
            self.last_frame = frame; return frame
        if self.picam2 is not None:
            frame = self.picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        else:
            ok, frame = self.cap.read()
            if not ok: return self.last_frame
        self.last_frame = frame
        return frame

    def jpeg(self, frame=None):
        frame = frame if frame is not None else self.read()
        ok, buf = cv2.imencode('.jpg', frame)
        return buf.tobytes() if ok else None

    def release(self):
        if self.picam2: self.picam2.stop()
        if self.cap: self.cap.release()
