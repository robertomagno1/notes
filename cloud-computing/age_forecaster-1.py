# for other env sys just change the setting in 
# the main ambu


#!/usr/bin/env python3
"""
age_estimator_regression.py

Stima continua dell'età da un'immagine di volto usando il modello Caffe di OpenCV.
Calcola il valore atteso sulle fasce d'età per ottenere un'età in anni.
"""

import cv2
import sys
import argparse
from pathlib import Path
import numpy as np

# ─── CONFIG PATH ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR   = BASE_DIR.parent / '/Users/roberto/Desktop/age_predictor/data'
MODELS_DIR = BASE_DIR.parent / '/Users/roberto/Desktop/age_predictor/model'

FACE_CASCADE_PATH = DATA_DIR / 'haarcascade_frontalface_default.xml'
AGE_PROTO         = MODELS_DIR / 'deploy_age.prototxt'
AGE_MODEL         = MODELS_DIR / 'age_net.caffemodel'

# Fasce d'età e loro punti medi
AGE_BUCKETS   = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
                 '(25-32)', '(38-43)', '(48-53)', '(60-100)']
AGE_MIDPOINTS = np.array([ (0+2)/2, (4+6)/2, (8+12)/2, (15+20)/2,
                           (25+32)/2, (38+43)/2, (48+53)/2, (60+100)/2 ], dtype=np.float32)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# ─── CARICA I MODELLI ──────────────────────────────────────────────────────────
def load_models():
    if not FACE_CASCADE_PATH.exists():
        sys.exit(f"[ERRORE] Haarcascade non trovato: {FACE_CASCADE_PATH}")
    if not AGE_PROTO.exists() or not AGE_MODEL.exists():
        sys.exit(f"[ERRORE] Modello età non trovato in: {MODELS_DIR}")
    face_detector = cv2.CascadeClassifier(str(FACE_CASCADE_PATH))
    age_net = cv2.dnn.readNetFromCaffe(str(AGE_PROTO), str(AGE_MODEL))
    return face_detector, age_net

# ─── PREDIZIONE ETÀ CONTINUA ────────────────────────────────────────────────────
def predict_age_continuous(image_path: Path, face_detector, age_net):
    img = cv2.imread(str(image_path))
    if img is None:
        sys.exit(f"[ERRORE] Impossibile caricare immagine: {image_path}")

    h_img, w_img = img.shape[:2]
    min_face_area = (w_img * h_img) * 0.01  # filtra riquadri <1% area immagine

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )
    # filtra per dimensione
    faces = [r for r in faces if r[2]*r[3] >= min_face_area]
    if not faces:
        print("[INFO] Nessun volto valido rilevato.")
        return img

    # prendi il volto più grande
    x, y, w, h = max(faces, key=lambda r: r[2]*r[3])
    face = img[y:y+h, x:x+w]

    # preprocessing e forward
    blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
    age_net.setInput(blob)
    preds = age_net.forward().flatten()  # vettore di probabilità

    # calcola età continua come valore atteso
    expected_age = float(np.dot(preds, AGE_MIDPOINTS))
    conf = float(preds.max())  # confidenza della bucket più probabile

    # annotazione
    label = f"{expected_age:.1f} yrs ({conf*100:.1f}% max)"
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img, label, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return img

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Stima continua dell'età da un volto")
    p.add_argument('-i','--image',       required=True, help="Path all'immagine")
    p.add_argument('-t','--display-time',type=int, default=0,
                   help="ms per mostrare la finestra (0=attende tasto)")
    p.add_argument('-s','--save-output', default=None,
                   help="Se indicato, salva l'immagine annotata qui")
    args = p.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        sys.exit(f"[ERRORE] Immagine non trovata: {img_path}")

    # carica modelli
    face_detector, age_net = load_models()

    # predice e annota
    out_img = predict_age_continuous(img_path, face_detector, age_net)

    # salva opzionale
    if args.save_output:
        out_path = Path(args.save_output)
        cv2.imwrite(str(out_path), out_img)
        print(f"[INFO] Output salvato in {out_path}")

    # mostra
    win = "Age Estimation"
    cv2.imshow(win, out_img)
    if args.display_time > 0:
        cv2.waitKey(args.display_time)
    else:
        print("[INFO] Premi un tasto per chiudere…")
        cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
