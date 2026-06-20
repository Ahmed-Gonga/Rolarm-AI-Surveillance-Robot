import cv2, os, numpy as np, time
from pathlib import Path

class FaceRecognitionService:
    def __init__(self, cfg, db=None):
        self.cfg = cfg; self.db = db
        self.dataset_dir = Path(cfg['dataset_dir']); self.model_path = Path(cfg['models_dir'])/'lbph_face_model.yml'; self.labels_path = Path(cfg['models_dir'])/'labels.txt'
        self.confidence_limit = int(cfg.get('confidence_limit',65))
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = None; self.labels = {}; self.trained = False
        self._load_model()

    def _new_recognizer(self):
        if not hasattr(cv2, 'face'):
            raise RuntimeError('OpenCV contrib face module missing. Install opencv-contrib-python or python3-opencv with contrib support.')
        return cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)

    def _load_model(self):
        if self.model_path.exists() and self.labels_path.exists():
            try:
                self.recognizer = self._new_recognizer(); self.recognizer.read(str(self.model_path))
                self.labels = {}
                for line in self.labels_path.read_text().splitlines():
                    if ',' in line:
                        i,n = line.split(',',1); self.labels[int(i)] = n
                self.trained = True
            except Exception:
                self.trained = False

    def detect_faces(self, gray):
        return self.detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(70,70))

    def capture_face(self, frame, person_name):
        safe = ''.join(c for c in person_name.strip() if c.isalnum() or c in (' ','_','-')).strip() or 'Owner'
        folder = self.dataset_dir / safe; folder.mkdir(parents=True, exist_ok=True)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detect_faces(gray)
        saved=[]
        for x,y,w,h in faces:
            face = cv2.resize(gray[y:y+h,x:x+w], (200,200))
            path = folder / f'{int(time.time()*1000)}.jpg'
            cv2.imwrite(str(path), face); saved.append(str(path))
        if self.db: self.db.upsert_person(safe, len(list(folder.glob('*.jpg'))))
        return {'person': safe, 'saved_count': len(saved), 'files': saved}

    def train(self):
        images=[]; labels=[]; label_map={}; label_id=0
        for person_dir in sorted([p for p in self.dataset_dir.iterdir() if p.is_dir()]):
            files = list(person_dir.glob('*.jpg')) + list(person_dir.glob('*.png'))
            if len(files) < int(self.cfg.get('min_training_images',20)):
                continue
            label_map[label_id] = person_dir.name
            for f in files:
                img = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    images.append(cv2.resize(img,(200,200))); labels.append(label_id)
            if self.db: self.db.upsert_person(person_dir.name, len(files))
            label_id += 1
        if not images:
            raise RuntimeError('No enough training images. Capture at least min_training_images for one person.')
        self.recognizer = self._new_recognizer(); self.recognizer.train(images, np.array(labels))
        self.model_path.parent.mkdir(parents=True, exist_ok=True); self.recognizer.save(str(self.model_path))
        self.labels_path.write_text('\n'.join(f'{i},{n}' for i,n in label_map.items()))
        self.labels = label_map; self.trained=True
        return {'trained_people': list(label_map.values()), 'images': len(images)}

    def analyze(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY); results=[]; stranger=False
        for x,y,w,h in self.detect_faces(gray):
            label='STRANGER'; confidence=None; known=False
            if self.trained and self.recognizer:
                face = cv2.resize(gray[y:y+h,x:x+w], (200,200))
                pid, conf = self.recognizer.predict(face); confidence=float(conf)
                if conf < self.confidence_limit and pid in self.labels:
                    label = self.labels[pid]; known=True
                else: stranger=True
            else:
                label='FACE - MODEL NOT TRAINED'; stranger=True
            results.append({'box':[int(x),int(y),int(w),int(h)],'name':label,'known':known,'confidence':confidence})
        return results, stranger

    def draw(self, frame, results):
        for r in results:
            x,y,w,h = r['box']; known=r['known']; color=(0,200,0) if known else (0,0,255)
            text = ('EXIST: '+r['name']) if known else 'STRANGER'
            if r['confidence'] is not None: text += f' {r["confidence"]:.1f}'
            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2); cv2.putText(frame,text,(x,max(25,y-10)),cv2.FONT_HERSHEY_SIMPLEX,0.65,color,2)
        return frame
