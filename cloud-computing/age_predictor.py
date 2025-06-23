#!/usr/bin/env python3
"""
age_estimator.py

Stima l'età da un'immagine di volto usando OpenCV DNN e un modello Caffe.

Usage (CLI):
    python age_estimator.py \
      --image /percorso/assoluto/o/relativo/foto.jpg \
      [--display-time 2000] \
      [--save-output /percorso/output.jpg]

Se `--display-time` > 0, la finestra si chiude dopo quel numero di millisecondi.
Se omesso o 0, attende un tasto (`waitKey(0)`).
"""
import cv2
import sys
import argparse
from pathlib import Path

# ─── CONFIG PATH ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR   = BASE_DIR.parent / '/Users/roberto/Desktop/age_predictor/data'
MODELS_DIR = BASE_DIR.parent / '/Users/roberto/Desktop/age_predictor/model'

FACE_CASCADE_PATH = DATA_DIR / 'haarcascade_frontalface_default.xml'
AGE_PROTO         = MODELS_DIR / 'deploy_age.prototxt'
AGE_MODEL         = MODELS_DIR / 'age_net.caffemodel'

AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
            '(25-32)', '(38-43)', '(48-53)', '(60-100)']
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# ─── MODELS ────────────────────────────────────────────────────────────────────
def load_models():
    if not FACE_CASCADE_PATH.exists():
        sys.exit(f"[ERRORE] Haarcascade non trovato: {FACE_CASCADE_PATH}")
    if not AGE_PROTO.exists() or not AGE_MODEL.exists():
        sys.exit(f"[ERRORE] Modello età non trovato in: {MODELS_DIR}")
    face_detector = cv2.CascadeClassifier(str(FACE_CASCADE_PATH))
    age_net = cv2.dnn.readNetFromCaffe(str(AGE_PROTO), str(AGE_MODEL))
    return face_detector, age_net

# ─── PREDICTION ────────────────────────────────────────────────────────────────
def predict_age_on_image(image_path: Path, face_detector, age_net):
    img = cv2.imread(str(image_path))
    if img is None:
        sys.exit(f"[ERRORE] Impossibile caricare immagine: {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.1, 5, minSize=(60,60))
    if len(faces) == 0:
        print("[INFO] Nessun volto rilevato.")
        return img
    for (x,y,w,h) in faces:
        face = img[y:y+h, x:x+w]
        blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        age_net.setInput(blob)
        preds = age_net.forward()
        i = preds[0].argmax()
        age, conf = AGE_LIST[i], preds[0][i]
        label = f"{age} {conf*100:.1f}%"
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(img, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    return img

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="Age Estimation da immagine volto")
    p.add_argument('-i','--image',    required=True, help="Path all'immagine")
    p.add_argument('-t','--display-time', type=int, default=0,
                   help="ms per mostrare la finestra (0=attende tasto)")
    p.add_argument('-s','--save-output', default=None,
                   help="Se indicato, salva l'immagine annotata qui")
    args = p.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        sys.exit(f"[ERRORE] Immagine non trovata: {img_path}")

    # Carica modelli
    face_detector, age_net = load_models()

    # Predice e annota
    out_img = predict_age_on_image(img_path, face_detector, age_net)

    # Salvataggio opzionale
    if args.save_output:
        out_path = Path(args.save_output)
        cv2.imwrite(str(out_path), out_img)
        print(f"[INFO] Output salvato in {out_path}")

    # Mostra a schermo
    winname = "Age Estimation"
    cv2.imshow(winname, out_img)
    if args.display_time > 0:
        cv2.waitKey(args.display_time)
    else:
        print("[INFO] Premi un tasto per chiudere…")
        cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
